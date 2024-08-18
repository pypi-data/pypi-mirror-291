from wppcpy import exceptions


class File:
    def __init__(self, path: str):
        self._path = path

    def read(self):
        try:
            with open(self._path, 'r') as f:
                return f.read()

        except Exception as e:
            raise exceptions.file.FileReadException(f"An error occurred while reading the '{self._path}': {e}")
