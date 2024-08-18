from wppcpy import exceptions


class FileReadException(exceptions.base.PcpyException):
    def __init__(self, message:str="An error occurred while reading the file."):
        super().__init__(message)