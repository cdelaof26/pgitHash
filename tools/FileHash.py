# Object to save hash and path

class FileHash:
    def __init__(self, file_path, file_hash):
        self.file_path = file_path
        self.file_hash = file_hash

    def get_file_path(self):
        return self.file_path

    def get_hash(self):
        return self.file_hash
