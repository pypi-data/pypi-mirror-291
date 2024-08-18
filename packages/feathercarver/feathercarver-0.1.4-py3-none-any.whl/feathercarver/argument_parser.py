import argparse
import typing


class ArgumentParser:
    def parse_arguments(self) -> typing.List[str]:
        parser = argparse.ArgumentParser(
            description="Fix broken Markdown links in files."
        )
        parser.add_argument(
            "files", nargs="+", help="One or more Markdown files to process"
        )
        args = parser.parse_args()
        return list(dict.fromkeys(args.files))
