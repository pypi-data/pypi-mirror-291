import uuid

from docker.models.containers import Container

from concave.internal.snapshot.snapshot import Snapshot
from concave.internal.workspace.file import File


class Workspace:
    _container: Container

    def __init__(self, container: Container):
        self._container = container

    def id(self):
        return self._container.id

    def commit(self) -> Snapshot:
        snapshot = Snapshot(str(uuid.uuid4()))
        self._container.commit(repository=snapshot.repository, tag=snapshot.tag)
        return snapshot

    def execute(self, cmd: list[str], **kwargs) -> (int, str):
        exit_code, out = self._container.exec_run(cmd=cmd, **kwargs)
        return exit_code, out.decode("utf-8")

    def exec(self, cmd: list[str], **kwargs) -> (int, str):
        return self.execute(cmd=cmd, **kwargs)

    def ls(self, path: str) -> list[str]:
        _, output = self._container.exec_run(cmd=["ls", path])
        return [line for line in str(output, encoding='utf-8').split("\n") if line]

    def open(self, path: str) -> File:
        return File(self._container, path)

    def quit(self):
        self._container.remove(force=True)

    def remove(self):
        self._container.remove(force=True)
