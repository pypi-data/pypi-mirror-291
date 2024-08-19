from typing import List
import os.path
import tempfile

import docker
from loguru import logger

import jinja2

from concave.internal.snapshot.snapshot import Snapshot
from concave.internal.workspace.config import Config
from concave.internal.workspace.workspace import Workspace


class WorkspaceManager:
    def __init__(self):
        try:
            self.docker = docker.DockerClient.from_env()
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            raise e

    def create(self, config: Config) -> Workspace:
        assert config.language in ['python'], f"Unsupported language: {config.language}"
        repo, commit = parse_codebase(config.codebase)

        temp_dir = tempfile.mkdtemp("concave")
        logger.debug(f"Workspace temp dir: {temp_dir}")

        with open(f"{os.path.dirname(__file__)}/Dockerfile.j2") as f:
            dockerfile = jinja2.Template(f.read()).render(
                IMAGE_NAME=config.language,
                IMAGE_TAG=config.version,
                GIT_REPO=repo,
                GIT_COMMIT=commit,
                PROJECT_SETUP="RUN " + " && ".join(config.project_setup),
            )

        with open(f"{temp_dir}/Dockerfile", "w") as f:
            logger.debug(f"Generated Dockerfile: ===\n{dockerfile}\n===")
            f.write(dockerfile)

        snapshot = Snapshot(config.name)
        snapshot.build(self.docker, temp_dir, repo, commit, config.platform)

        return self.run(snapshot, config.platform)



    def run(self, snapshot: Snapshot, platform) -> Workspace:
        container = self.docker.containers.run(
            str(snapshot),
            platform=platform,
            detach=True,
        )
        return Workspace(container)

    def list(self) -> List[Workspace]:
        containers = self.docker.containers.list(all=True)
        return [Workspace(container) for container in containers]

    def get(self, workspace: str) -> Workspace:
        return Workspace(self.docker.containers.get(workspace))


def parse_codebase(codebase: str):
    parts = codebase.split('/')
    if len(parts) == 3:
        return codebase, None
    elif len(parts) == 5:
        return '/'.join(parts[:3]), parts[-1]

    raise ValueError("Invalid codebase: %s, excepted github.com/{repo}/{org}?(/commit/{commit})" % codebase)
