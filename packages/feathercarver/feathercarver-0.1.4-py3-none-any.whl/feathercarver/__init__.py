__project_name__ = "feathercarver"
from .argument_parser import ArgumentParser
from .file_processor import FileProcessor
from .link_fixer import LinkFixer


def main() -> int:
    parser = ArgumentParser()
    file_paths = parser.parse_arguments()

    link_fixer = LinkFixer()
    file_processor = FileProcessor(link_fixer)

    for file_path in file_paths:
        file_processor.process_file(file_path)

    return 0


__all__ = ["main"]
