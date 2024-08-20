from docker.models.images import Image
from loguru import logger
import docker


class Snapshot:
    _image: Image

    def __init__(self, image: Image):
        self._image = image

    @property
    def attrs(self):
        return self._image.attrs

    @property
    def name(self):
        return f"{self._image.tags[0]}"

    def remove(self):
        logger.debug(f"Removing Docker image {self}")
        self._image.remove(force=True)
