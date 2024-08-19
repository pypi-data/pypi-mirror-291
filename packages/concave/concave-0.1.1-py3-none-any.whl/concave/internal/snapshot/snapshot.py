from loguru import logger
import docker


class Snapshot:

    def __init__(self, tag: str):
        self.repository = 'concave-space'
        self.tag = tag

    def __str__(self):
        return f"{self.repository}:{self.tag}"

    def build(self, docker_client: docker.DockerClient,
              dockerfile_path: str,
              repo: str, commit: str, platform):
        logger.debug("Building Docker image")

        image, logs = docker_client.images.build(
            path=dockerfile_path,
            platform=platform,
            tag=f"{self.repository}:{self.tag}",
            labels={
                "concave.space.uuid": self.tag,
                "concave.space.repo": repo,
                "concave.space.commit": commit,
            },
            rm=True,
        )
        logger.debug(f"build image: {image}, logs: {logs}")
        logger.debug(f"Docker image built: {self}")
