from pathlib import Path

import docker
from loguru import logger

from internal.snapshot.snapshot import Snapshot


class SnapshotManager:
    def __init__(self):
        try:
            self.docker = docker.DockerClient.from_env()
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            raise e

    def get(self, name: str) -> Snapshot:
        return Snapshot(self.docker.images.get(name))

    def build(self,
              image_name: str,
              build_dir: str,
              setup_scripts: dict,
              dockerfile: str,
              platform: str,
              labels: dict,
              nocache: bool = False) -> Snapshot:
        logger.debug(f"Start to build docker image: {image_name} in {build_dir} with platform {platform}")

        for setup_script_name, setup_script in setup_scripts.items():
            logger.info(f"[SETUP SCRIPT] {setup_script_name}:\n{setup_script}")

        # Write the setup scripts to the build directory
        for setup_script_name, setup_script in setup_scripts.items():
            setup_script_path = f"{build_dir}/{setup_script_name}"
            with open(setup_script_path, "w") as f:
                f.write(setup_script)
            if setup_script_name not in dockerfile:
                logger.warning(
                    f"Setup script {setup_script_name} may not be used in Dockerfile"
                )

        # Write the dockerfile to the build directory
        dockerfile_path = f"{build_dir}/Dockerfile"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile)

        image, logs = self.docker.images.build(
            path=build_dir,
            platform=platform,
            tag=image_name,
            labels=labels,
            rm=True,
            nocache=nocache,
        )
        for log in logs:
            print(log)
        logger.debug(f"build image: {image_name}, logs: {logs}")
        return Snapshot(image)
