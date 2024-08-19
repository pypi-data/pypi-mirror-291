import logging
import pathlib
import typing


class DirectoryProcessor:
    def __init__(self, file_processor):
        self.file_processor = file_processor
        self.logger = logging.getLogger(__name__)

    def process_directories(
        self, directories: typing.List[str], extensions: typing.List[str]
    ):
        for directory in directories:
            self.process_directory(directory, extensions)

    def process_directory(self, directory: str, extensions: typing.List[str]):
        dir_path = pathlib.Path(directory)
        self.logger.info(f"Processing directory: {dir_path}")
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and file_path.suffix[1:] in extensions:
                self.logger.debug(f"Found file: {file_path}")
                self.file_processor.process_file(str(file_path))
