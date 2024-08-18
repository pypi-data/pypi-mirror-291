import re
import os

from wppcpy import constraints, filesystem, exceptions


class HeaderRequirementConstraint(constraints.base.Constraint):
    DOC_BLOCK_PATTERN = r'/\*(.*?)\*/'

    def __init__(self, path: str, requirement: str, main_file_name: str | list[str] = None):
        main_file_name = os.path.join(path, os.path.basename(path) + ".php") \
            if main_file_name is None else main_file_name

        if isinstance(main_file_name, str):
            main_file_name = [main_file_name]

        main_file_name = [os.path.join(path, _) for _ in main_file_name]

        self._paths = main_file_name
        self._requirement: str = requirement

    def validate(self) -> bool:
        for php_file in self._paths:
            try:
                content = filesystem.File(php_file).read()
            except exceptions.PcpyException:
                return False

            match = re.search(
                self.DOC_BLOCK_PATTERN,
                content,
                re.DOTALL
            )

            if match:
                doc_block = match.group(1)

                if self._requirement in doc_block:
                    return True

        return False


class PluginName(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Plugin Name: ", main_file_name=main_file_name)


class PluginURI(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Plugin URI: ", main_file_name=main_file_name)


class Description(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Description: ", main_file_name=main_file_name)


class Version(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Version: ", main_file_name=main_file_name)


class RequiresAtLeast(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Requires at least: ", main_file_name=main_file_name)


class RequiresPHP(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Requires PHP: ", main_file_name=main_file_name)


class Author(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Author: ", main_file_name=main_file_name)


class AuthorURI(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Author URI: ", main_file_name=main_file_name)


class License(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="License: ", main_file_name=main_file_name)


class LicenseURI(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="License URI: ", main_file_name=main_file_name)


class TextDomain(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Text Domain: ", main_file_name=main_file_name)


class DomainPath(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Domain Path: ", main_file_name=main_file_name)


class Network(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Network: ", main_file_name=main_file_name)


class UpdateURI(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Update URI: ", main_file_name=main_file_name)


class RequiresPlugins(HeaderRequirementConstraint):
    def __init__(self, path: str, main_file_name: str | list[str] = None):
        super().__init__(path, requirement="Requires Plugins: ", main_file_name=main_file_name)
