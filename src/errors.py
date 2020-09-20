class AsmFileNotExists(Exception):
    def __init__(self, msg="Asm file did not exixts in asm_src folder!!!!"):
        super().__init__(msg)


class MakeFileAlreadyExists(Exception):
    def __init__(self, msg="MakeFile Already Exists"):
        super().__init__(msg)


class ErrorCopingFiles(Exception):
    def __init__(self, msg="Cant copy files to Temp Directory"):
        super().__init__(msg)


class TempDirectoryAlreadyExists(Exception):
    def __init__(self, msg="Temp Directory Already Exists"):
        super().__init__(msg)
