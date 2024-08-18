import os

from wppcpy import constraints


class FileConstraint(constraints.base.Constraint):
    def __init__(self, path):
        self._path = path

    def validate(self) -> bool:
        return os.path.exists(self._path)


class Readme(FileConstraint):
    def __init__(self, path: str):
        super().__init__(os.path.join(path, 'readme.txt'))


class MainFile(FileConstraint):
    def __init__(self, path: str, files: str | list[str] = None):
        super().__init__(path)

        files = os.path.join(self._path, os.path.basename(self._path) + ".php") \
               if files is None else files

        if isinstance(files, str):
            files = [files]

        files = [os.path.join(path, _) for _ in files]

        self._constraints = [FileConstraint(path) for path in files]

    def validate(self) -> bool:
        return all(constraint.validate() for constraint in self._constraints)


class UninstallPHP(FileConstraint):
    def __init__(self, path: str):
        super().__init__(os.path.join(path, 'uninstall.php'))


class InstallPHP(FileConstraint):
    def __init__(self, path: str):
        super().__init__(os.path.join(path, 'install.php'))
