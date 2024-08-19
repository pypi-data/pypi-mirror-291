from pathlib import Path
from typing import List
import os.path
import tempfile

import docker
from loguru import logger

import jinja2

from concave.internal.snapshot.snapshot import Snapshot
from concave.internal.workspace.config import Config
from concave.internal.workspace.workspace import Workspace
from internal.snapshot.manager import SnapshotManager


class WorkspaceManager:
    def __init__(self):
        try:
            self.docker = docker.DockerClient.from_env()
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            raise e

    def create(self, config: Config) -> Workspace:
        snapshot_manager = SnapshotManager()
        assert config.language in ['python'], f"Unsupported language: {config.language}"

        workspace_snapshot = build_workspace_image(snapshot_manager, config)
        return self.run(workspace_snapshot, config.platform)

    def run(self, snapshot: Snapshot, platform) -> Workspace:
        container = self.docker.containers.run(
            snapshot.name,
            platform=platform,
            detach=True,
        )
        return Workspace(container)

    def list(self) -> List[Workspace]:
        containers = self.docker.containers.list(all=True)
        return [Workspace(container) for container in containers]

    def get(self, workspace: str) -> Workspace:
        return Workspace(self.docker.containers.get(workspace))


def build_workspace_image(
        snapshot_manager: SnapshotManager,
        config: Config,
        nocache=False) -> Snapshot:
    build_dir = tempfile.mkdtemp("concave")
    image_name = config.workspace_image_key
    dockerfile = config.workspace_dockerfile
    env_image_name = config.env_image_key

    # Check that the env. image the instance image is based on exists
    try:
        env_image = snapshot_manager.get(env_image_name)
    except docker.errors.ImageNotFound as e:
        env_image = build_env_image(snapshot_manager, config)

    # Check if the instance image already exists
    try:
        workspace_image = snapshot_manager.get(image_name)
        if workspace_image.attrs["Created"] < env_image.attrs["Created"]:
            # the environment image is newer than the instance image, meaning the instance image may be outdated
            workspace_image.remove()
        else:
            print(f"Image {image_name} already exists, skipping build.")
            return workspace_image
    except docker.errors.ImageNotFound:
        pass

    print(
        # f"Environment image {env_image_name} found for {config.name}\n"
        f"Building workspace image {image_name} for {config.name}"
    )
    # Build the instance image
    return snapshot_manager.build(
        image_name=image_name,
        setup_scripts={
            "setup_workspace.sh": config.install_repo_script,
        },
        dockerfile=dockerfile,
        platform=config.platform,
        build_dir=build_dir,
        nocache=nocache,
        labels={
            "concave.space.repo": config.git_repo,
            "concave.space.commit": config.git_commit,
        },
    )


def build_env_image(snapshot_manager: SnapshotManager,config: Config,nocache=False) -> Snapshot:
    build_dir = tempfile.mkdtemp("concave")
    image_name = config.env_image_key
    dockerfile = config.env_dockerfile

    try:
        base_image = snapshot_manager.get(config.base_image_key)
    except docker.errors.ImageNotFound as e:
        base_image = build_base_image(snapshot_manager, config, nocache)

    try:
        env_image = snapshot_manager.get(image_name)
        if env_image.attrs["Created"] < base_image.attrs["Created"]:
            env_image.remove()
        else:
            print(f"Environment image {image_name} already exists, skipping build.")
            return env_image
    except docker.errors.ImageNotFound:
        pass

    print(f"Building environment image {image_name} for {config.name}")
    return snapshot_manager.build(
        image_name=image_name,
        setup_scripts={
            "setup_env.sh": config.setup_env_script,
        },
        dockerfile=dockerfile,
        platform=config.platform,
        build_dir=build_dir,
        nocache=nocache,
        labels={},
    )

def build_base_image(snapshot_manager: SnapshotManager,config: Config,nocache=False) -> Snapshot:
    build_dir = tempfile.mkdtemp("concave")
    image_name = config.base_image_key
    dockerfile = config.base_dockerfile

    print(f"Building base image {image_name}")
    return snapshot_manager.build(
        image_name=image_name,
        setup_scripts={},
        dockerfile=dockerfile,
        platform=config.platform,
        build_dir=build_dir,
        nocache=nocache,
        labels={},
    )
