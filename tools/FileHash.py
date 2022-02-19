# Object to save hash and path

STATS = ["Created", "Deleted", "Renamed", "Modified", "Moved", "RenamedAndMoved", "ModifiedAndMoved"]


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
