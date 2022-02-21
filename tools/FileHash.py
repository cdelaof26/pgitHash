# Object to save hash and path

FILE_MOVED = "Moved"
FILE_CREATED = "Created"
FILE_DELETED = "Deleted"
FILE_RENAMED = "Renamed"
FILE_MODIFIED = "Modified"
FILE_RENAMED_AND_MOVED = "RenamedAndMoved"
FILE_MODIFIED_AND_MOVED = "ModifiedAndMoved"


class FileHash:
    def __init__(self, file_path, file_hash, file_stat=None):
        self.file_path = file_path
        self.file_hash = file_hash
        self.file_stat = file_stat

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_file_hash(self) -> str:
        return self.file_hash

    def set_file_stat(self, file_stat):
        self.file_stat = file_stat

    def get_file_stat(self) -> str:
        return self.file_stat
