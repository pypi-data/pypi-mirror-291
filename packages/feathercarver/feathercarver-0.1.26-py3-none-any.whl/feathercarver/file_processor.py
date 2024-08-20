import logging
import pathlib


class FileProcessor:
    def __init__(self, link_fixer):
        self.link_fixer = link_fixer
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_path):
        path = pathlib.Path(file_path)
        self.logger.debug(f"Processing file: {path}")

        try:
            content = path.read_text()
        except IOError as e:
            self.logger.error(f"Error reading {path}: {e}")
            return

        fixed_content = self.link_fixer.fix_markdown_links(content)

        if fixed_content != content:
            try:
                self.logger.info(f"Updating {path}")
                path.write_text(fixed_content)
            except IOError as e:
                self.logger.error(f"Error writing to {path}: {e}")
        else:
            self.logger.debug(f"No changes needed for {path}")
