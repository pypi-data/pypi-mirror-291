import logging
import pathlib


class FileProcessor:
    def __init__(self, link_fixer):
        self.link_fixer = link_fixer
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_path):
        path = pathlib.Path(file_path)
        self.logger.info(f"Processing file: {path}")

        if not self._read_and_process_file(path):
            return

        self.logger.info(f"Processed {path}")

    def _read_and_process_file(self, path):
        try:
            content = path.read_text()
        except IOError as e:
            self.logger.error(f"Error reading {path}: {e}")
            return False

        fixed_content = self.link_fixer.fix_markdown_links(content)
        if fixed_content == content:
            return True

        try:
            path.write_text(fixed_content)
        except IOError as e:
            self.logger.error(f"Error writing to {path}: {e}")
            return False

        return True
