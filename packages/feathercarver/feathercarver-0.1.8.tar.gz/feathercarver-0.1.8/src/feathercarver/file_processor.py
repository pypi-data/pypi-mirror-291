import pathlib
import sys


class FileProcessor:
    def __init__(self, link_fixer):
        self.link_fixer = link_fixer

    def process_file(self, file_path):
        path = pathlib.Path(file_path)
        try:
            content = path.read_text()
            fixed_content = self.link_fixer.fix_markdown_links(content)
            path.write_text(fixed_content)
            print(f"Processed {path}")
        except IOError as e:
            print(f"Error processing {path}: {e}", file=sys.stderr)
