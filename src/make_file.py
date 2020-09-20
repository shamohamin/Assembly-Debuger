import os
import pathlib
import glob
import shutil
import time
from src.errors import (AsmFileNotExists, MakeFileAlreadyExists,
                        TempDirectoryAlreadyExists, ErrorCopingFiles)


class MakeFile(object):
    MAKE_FILE = "makefile"
    extension_support = [".asm", ".c"]
    GCC_OPTION = '-m32 '
    EXECUTABLE_FILE = "a.out "
    ASM_COMPILE = "nasm -f elf {}"
    C_COMPILE = "gcc {} -c {}"

    def __init__(self, asm_src="asm_src"):
        self.src = os.path.join(pathlib.Path(
            __file__).parent.absolute(), asm_src)
        self.src_files = []
        self.__check_file_exists()

    def __check_file_exists(self):
        if not os.path.exists(self.src):
            raise FileNotFoundError(f"directory {self.src} is not exists.")

    def __find_files(self):
        try:
            self.src_files = glob.glob(os.path.join(self.src, '*'))
            if len(self.src_files) == 0:
                raise AsmFileNotExists(
                    msg=f'asm files or c files did not exists in {self.src} folder')
        except AsmFileNotExists as ex:
            print(ex.args[0])

    def __generate_make_files_from_files(self):
        try:
            if os.path.exists(os.path.join(self.src, MakeFile.MAKE_FILE)):
                raise MakeFileAlreadyExists

            files = []
            for file in self.src_files:
                temp_file = pathlib.Path(file).name
                file_name, file_ext = os.path.splitext(temp_file)
                if file_ext in MakeFile.extension_support:
                    files.append({
                        'object_file': file_name + '.o',
                        'main_file': temp_file
                    })

            def make_runnable_file():
                root_execution = "{} : ".format(MakeFile.EXECUTABLE_FILE)
                joined_files = ' '.join(
                    [object_file['object_file'] for object_file in files])
                return root_execution + joined_files + '\n'

            def generate():
                with open(os.path.join(self.src, MakeFile.MAKE_FILE), 'w') as makeFile:
                    makeFile.write(make_runnable_file())
                    makeFile.write('\t' + 'gcc ' + MakeFile.GCC_OPTION +
                                   ' '.join([object_file['object_file'] for object_file in files]) + '\n\n')
                    for file in files:
                        makeFile.write(file['object_file'] +
                                       ' : ' + file['main_file'] + '\n')
                        makeFile.write('\t')
                        if file['main_file'] == 'asm_io.asm':
                            makeFile.write(
                                'nasm -f elf -d ELF_TYPE asm_io.asm')
                        elif os.path.splitext(file['main_file'])[1] == '.asm':
                            makeFile.write(
                                MakeFile.ASM_COMPILE.format(file['main_file']))
                        else:
                            makeFile.write(MakeFile.C_COMPILE.format(
                                MakeFile.GCC_OPTION, file['main_file']))
                        makeFile.write('\n\n')

                    makeFile.write('run: \n\t./a.out < input.txt \n\n')
                    makeFile.write('clean: \n\trm -rf *.out *.o \n\n')

            generate()
            print('make file ok')

        except (Exception, MakeFileAlreadyExists) as ex:
            print(ex.args[0])

    def __make_temp_file(self, asm_files: list):
        try:
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            if os.path.exists(temp_dir):
                raise TempDirectoryAlreadyExists()

            os.mkdir(temp_dir)
            for file in asm_files:
                file_name = os.path.splitext(pathlib.Path(file).name)[0]
                dir_name = os.path.join(
                    os.path.dirname(__file__), 'temp', file_name)
                os.mkdir(dir_name)
                for item in [*self.src_files, os.path.join(self.src, MakeFile.MAKE_FILE)]:
                    shutil.copy(item, dir_name)

        except (Exception, TempDirectoryAlreadyExists) as ex:
            print(ex.args[0])

    def execute(self):
        """
        make MakeFile from src folder and return assembly files
        """
        self.__find_files()
        self.__generate_make_files_from_files()
        print('helloooooo')

        asm_files = []

        for file in self.src_files:
            temp_file = pathlib.Path(file).name
            if os.path.splitext(temp_file)[1] == MakeFile.extension_support[0] and temp_file != 'asm_io.asm':
                asm_files.append(file)

        self.__make_temp_file(asm_files)

        return asm_files
