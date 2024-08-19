import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

import docker

from concave.internal.snapshot.snapshot import Snapshot
from internal.snapshot.manager import SnapshotManager
from internal.workspace.config import Config


def build_base_images(
        configs: list[Config],
        force_rebuild: bool = False
):
    """
    Builds the base images required for the dataset if they do not already exist.

    Args:
        client (docker.DockerClient): Docker client to use for building the images
        dataset (list): List of test specs or dataset to build images for
        force_rebuild (bool): Whether to force rebuild the images even if they already exist
    """
    snapshot_manager = SnapshotManager()
    base_images = {
        x.base_image_key: (x.base_dockerfile, x.platform) for x in configs
    }

    # Build the base images
    for image_name, (dockerfile, platform) in base_images.items():
        try:
            # Check if the base image already exists
            snapshot = snapshot_manager.get(image_name)
            if force_rebuild:
                # Remove the base image if it exists and force rebuild is enabled
                snapshot.remove()
            else:
                print(f"Base image {image_name} already exists, skipping build.")
                continue
        except docker.errors.ImageNotFound:
            pass
        # Build the base image (if it does not exist or force rebuild is enabled)
        temp_dir = tempfile.mkdtemp("concave")
        print(f"Building base image ({image_name})")
        snapshot_manager.build(
            image_name=image_name,
            build_dir=temp_dir,
            setup_scripts={},
            dockerfile=dockerfile,
            platform=platform,
            labels={},
        )
    print("Base images built successfully.")


def get_env_images_to_build(
        configs: list[Config]
):
    """
    Returns a dictionary of image names to build scripts and dockerfiles for environment images.
    Returns only the environment images that need to be built.

    Args:
        client (docker.DockerClient): Docker client to use for building the images
        dataset (list): List of test specs or dataset to build images for
    """
    snapshot_manager = SnapshotManager()
    image_to_build = dict()
    base_images = dict()

    for config in configs:
        # Check if the base image exists
        try:
            if config.base_image_key not in base_images:
                base_images[config.base_image_key] = snapshot_manager.get(
                    config.base_image_key
                )
            base_image = base_images[config.base_image_key]
        except docker.errors.ImageNotFound:
            raise Exception(
                f"Base image {config.base_image_key} not found for env image {config.env_image_key}\n."
                "Please build the base images first."
            )

        # Check if the environment image exists
        image_exists = False
        try:
            env_image = snapshot_manager.get(config.env_image_key)
            image_exists = True

            if env_image.attrs["Created"] < base_image.attrs["Created"]:
                # Remove the environment image if it was built after the base_image
                # for dep in find_dependent_images(client, test_spec.env_image_key):
                #     # Remove instance images that depend on this environment image
                #     remove_image(client, dep.image_id, "quiet")
                env_image.remove()
                image_exists = False
            else:
                print(f"Environment image {config.env_image_key} already exists, skipping build.")
        except docker.errors.ImageNotFound:
            pass
        if not image_exists:
            # Add the environment image to the list of images to build
            image_to_build[config.env_image_key] = {
                "setup_script": config.setup_env_script,
                "dockerfile": config.env_dockerfile,
                "platform": config.platform,
            }
    return image_to_build


def build_env_images(
        configs: list[Config],
        force_rebuild: bool = False,
        max_workers: int = 4
):
    """
    Builds the environment images required for the dataset if they do not already exist.

    Args:
        client (docker.DockerClient): Docker client to use for building the images
        dataset (list): List of test specs or dataset to build images for
        force_rebuild (bool): Whether to force rebuild the images even if they already exist
        max_workers (int): Maximum number of workers to use for building images
    """
    snapshot_manager = SnapshotManager()
    if force_rebuild:
        env_image_keys = {x.env_image_key for x in configs}
        for env_image_name in env_image_keys:
            try:
                image = snapshot_manager.get(env_image_name)
                image.remove()
            except docker.errors.ImageNotFound:
                pass

    build_base_images(configs, force_rebuild)
    images_to_build = get_env_images_to_build(configs)
    if len(images_to_build) == 0:
        print("No environment images need to be built.")
        return [], []
    print(f"Total environment images to build: {len(images_to_build)}")

    # Build the environment images
    successful, failed = list(), list()
    with tqdm(
            total=len(images_to_build), smoothing=0, desc="Building environment images"
    ) as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a future for each image to build
            futures = {
                executor.submit(
                    snapshot_manager.build,
                    image_name,
                    tempfile.mkdtemp("concave"),
                    {"setup_env.sh": config["setup_script"]},
                    config["dockerfile"],
                    config["platform"],
                    {},
                    False,
                ): image_name
                for image_name, config in images_to_build.items()
            }

            # Wait for each future to complete
            for future in as_completed(futures):
                pbar.update(1)
                try:
                    # Update progress bar, check if image built successfully
                    future.result()
                    successful.append(futures[future])
                except Exception as e:
                    print(f"Error building image")
                    traceback.print_exc()
                    failed.append(futures[future])
                    continue

    # Show how many images failed to build
    if len(failed) == 0:
        print("All environment images built successfully.")
    else:
        print(f"{len(failed)} environment images failed to build.")

    # Return the list of (un)successfully built images
    return successful, failed

# def build_workspace_images(
#         configs: list,
#         force_rebuild: bool = False,
#         max_workers: int = 4
#     ):
#     """
#     Builds the instance images required for the dataset if they do not already exist.
#
#     Args:
#         dataset (list): List of test specs or dataset to build images for
#         client (docker.DockerClient): Docker client to use for building the images
#         force_rebuild (bool): Whether to force rebuild the images even if they already exist
#         max_workers (int): Maximum number of workers to use for building images
#     """
#     snapshot_manager = SnapshotManager()
#     if force_rebuild:
#         for config in configs:
#             try:
#                 image = snapshot_manager.get(config.workspace_image_key)
#                 image.remove()
#             except docker.errors.ImageNotFound:
#                 pass
#     _, env_failed = build_env_images(configs, force_rebuild, max_workers)
#
#     if len(env_failed) > 0:
#         # Don't build images for instances that depend on failed-to-build env images
#         dont_run_specs = [spec for spec in configs if spec.env_image_key in env_failed]
#         configs = [spec for spec in configs if spec.env_image_key not in env_failed]
#         print(f"Skipping {len(dont_run_specs)} instances - due to failed env image builds")
#     print(f"Building instance images for {len(configs)} instances")
#     successful, failed = list(), list()
#
#     # Build the instance images
#     with tqdm(
#         total=len(configs), smoothing=0, desc="Building instance images"
#     ) as pbar:
#         with ThreadPoolExecutor(max_workers=max_workers) as executor:
#             # Create a future for each image to build
#             futures = {
#                 executor.submit(
#                     build_workspace_image,
#                     config,
#                     False,
#                 ): config
#                 for config in configs
#             }
#
#             # Wait for each future to complete
#             for future in as_completed(futures):
#                 pbar.update(1)
#                 try:
#                     # Update progress bar, check if image built successfully
#                     future.result()
#                     successful.append(futures[future])
#                 except Exception as e:
#                     print(f"Error building image")
#                     traceback.print_exc()
#                     failed.append(futures[future])
#                     continue
#
#     # Show how many images failed to build
#     if len(failed) == 0:
#         print("All workspace images built successfully.")
#     else:
#         print(f"{len(failed)} workspace images failed to build.")
#
#     # Return the list of (un)successfully built images
#     return successful, failed


# def build_workspace_image(
#         config: Config,
#         nocache: bool,
#     ):
#     """
#     Builds the instance image for the given test spec if it does not already exist.
#
#     Args:
#         test_spec (TestSpec): Test spec to build the instance image for
#         client (docker.DockerClient): Docker client to use for building the image
#         logger (logging.Logger): Logger to use for logging the build process
#         nocache (bool): Whether to use the cache when building
#     """
#     snapshot_manager = SnapshotManager()
#     # Set up logging for the build process
#     build_dir = Path(tempfile.mkdtemp("concave"))
#
#     # Get the image names and dockerfile for the instance image
#     image_name = config.workspace_image_key
#     dockerfile = config.workspace_dockerfile
#     env_image_name = config.env_image_key
#
#     # Check that the env. image the instance image is based on exists
#     try:
#         env_image = snapshot_manager.get(env_image_name)
#     except docker.errors.ImageNotFound as e:
#         raise Exception(
#             config.name,
#             f"Environment image {env_image_name} not found for {config.name}",
#         ) from e
#     print(
#         f"Environment image {env_image_name} found for {config.name}\n"
#         f"Building instance image {image_name} for {config.name}"
#     )
#
#     # Check if the instance image already exists
#     image_exists = False
#     try:
#         workspace_image = snapshot_manager.get(image_name)
#         if workspace_image.attrs["Created"] < env_image.attrs["Created"]:
#             # the environment image is newer than the instance image, meaning the instance image may be outdated
#             workspace_image.remove()
#             image_exists = False
#         else:
#             image_exists = True
#     except docker.errors.ImageNotFound:
#         pass
#
#     # Build the instance image
#     if not image_exists:
#         snapshot_manager.build(
#             image_name=image_name,
#             setup_scripts={
#                 "setup_workspace.sh": config.install_repo_script,
#             },
#             dockerfile=dockerfile,
#             platform=config.platform,
#             build_dir=build_dir,
#             nocache=nocache,
#             labels={
#                 # "concave.space.uuid": self.tag,
#                 "concave.space.repo": config.git_repo,
#                 "concave.space.commit": config.git_commit,
#             },
#         )
#     else:
#         print(f"Image {image_name} already exists, skipping build.")
