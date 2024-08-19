import pathlib
import typing


class DirectoryProcessor:
    def __init__(self, file_processor):
        self.file_processor = file_processor

    def process_directories(
        self, directories: typing.List[str], extensions: typing.List[str]
    ):
        for directory in directories:
            self.process_directory(directory, extensions)

    def process_directory(self, directory: str, extensions: typing.List[str]):
        dir_path = pathlib.Path(directory)
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and file_path.suffix[1:] in extensions:
                self.file_processor.process_file(str(file_path))
