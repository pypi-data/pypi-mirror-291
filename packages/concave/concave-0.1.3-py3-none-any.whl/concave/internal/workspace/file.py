from docker.models.containers import Container


class File:
    def __init__(self, container: Container, path: str):
        self._container = container
        self.path = path

    def read(self, binary=False) -> str:
        _, output = self._container.exec_run(cmd=["cat", self.path])
        if binary:
            return output
        return str(output, encoding='utf-8')

    def write(self, content: str) -> int:
        exit_code, _ = self._container.exec_run(cmd=f"sh -c 'cat << EOF > {self.path}\n{content}\nEOF'")
        return exit_code

    def append(self, content: str) -> int:
        exit_code, _ = self._container.exec_run(cmd=f"sh -c 'cat << EOF >> {self.path}\n{content}'")
        return exit_code
