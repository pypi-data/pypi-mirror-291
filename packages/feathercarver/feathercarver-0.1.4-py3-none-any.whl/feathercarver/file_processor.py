import sys


class FileProcessor:
    def __init__(self, link_fixer):
        self.link_fixer = link_fixer

    def process_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            fixed_content = self.link_fixer.fix_markdown_links(content)

            with open(file_path, "w") as file:
                file.write(fixed_content)
            print(f"Processed {file_path}")
        except IOError as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
