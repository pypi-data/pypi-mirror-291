__project_name__ = "feathercarver"

from . import argument_parser, directory_processor, file_processor, link_fixer, logger


def main() -> int:
    parser = argument_parser.ArgumentParser()
    args = parser.parse_arguments()

    logger.setup_logger(args.verbose)

    lf = link_fixer.LinkFixer()
    fp = file_processor.FileProcessor(lf)
    dp = directory_processor.DirectoryProcessor(fp)

    if args.subcommand == "processfiles":
        for file_path in args.files:
            fp.process_file(file_path)
    elif args.subcommand == "processdirs":
        dp.process_directories(args.directories, args.ext)

    return 0


__all__ = ["main"]
