from io import StringIO
from pathlib import Path


class DataBackend:
    class DummyContextManager:
        def __init__(self, data):
            self.data = data

        def __enter__(self):
            return StringIO(self.data)

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def get(self, path) -> str:
        raise NotImplementedError

    def open(self, path):
        data = self.get(path)
        return DataBackend.DummyContextManager(data)

    def put(self, path, data: str):
        raise NotImplementedError

    def delete(self, path):
        raise NotImplementedError


class FilesystemBackend(DataBackend):
    """Backend for reading from the filesystem.

    Warnings
    --------
    This class is not secure. It is possible to read/write files outside
    of the specified root folder.
    """

    def __init__(self, root: str):
        self.root = Path(root)

    def get(self, path):
        with open(self.root / path, "r") as f:
            return f.read()

    def put(self, path, data: str):
        with open(self.root / path, "w") as f:
            f.write(data)

    def open(self, path):
        return open(self.root / path, "r")

    def delete(self, path):
        file = self.root / path
        file.unlink()
