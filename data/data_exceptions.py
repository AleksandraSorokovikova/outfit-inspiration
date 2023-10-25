class ConnectionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UploadingException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketSizeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketOverflowException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FilesKeysExceptions(Exception):
    def __init__(self, message):
        super().__init__(message)


class GetFileExceptions(Exception):
    def __init__(self, message):
        super().__init__(message)


class GetSaveFileExceptions(Exception):
    def __init__(self, message):
        super().__init__(message)
