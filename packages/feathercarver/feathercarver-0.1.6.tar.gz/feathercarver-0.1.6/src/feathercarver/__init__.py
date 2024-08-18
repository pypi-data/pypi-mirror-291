__project_name__ = "feathercarver"

from . import argument_parser, file_processor, link_fixer


def main() -> int:
    parser = argument_parser.ArgumentParser()
    file_paths = parser.parse_arguments()

    lf = link_fixer.LinkFixer()
    fp = file_processor.FileProcessor(lf)

    for file_path in file_paths:
        fp.process_file(file_path)

    return 0


__all__ = ["main"]
