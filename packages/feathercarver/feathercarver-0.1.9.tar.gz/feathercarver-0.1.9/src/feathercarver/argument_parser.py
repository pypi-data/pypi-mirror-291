import argparse


class ArgumentParser:
    def parse_arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Fix broken Markdown links in files."
        )
        subparsers = parser.add_subparsers(dest="subcommand", required=True)

        process_files = subparsers.add_parser(
            "processfiles", help="Process individual files"
        )
        process_files.add_argument(
            "files", nargs="+", help="One or more files to process"
        )

        process_dir = subparsers.add_parser(
            "processdirs", help="Process files in directories"
        )
        process_dir.add_argument(
            "directories", nargs="+", help="Directories to process"
        )
        process_dir.add_argument(
            "--ext", nargs="+", default=["md"], help="File extensions to process"
        )

        return parser.parse_args()
