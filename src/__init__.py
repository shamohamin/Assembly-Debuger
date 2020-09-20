from src.make_file import MakeFile
from src.debug_files import Debug
import os


class Runner:
    def run(self):
        log_dir_path = os.path.join(os.path.dirname(__file__), 'log')
        if not os.path.exists(log_dir_path):
            os.mkdir(log_dir_path, 0o777)

        MakeFile().execute()
