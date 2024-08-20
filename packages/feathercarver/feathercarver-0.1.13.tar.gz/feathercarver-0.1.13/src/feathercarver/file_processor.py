import logging
import pathlib


class FileProcessor:
    def __init__(self, link_fixer):
        self.link_fixer = link_fixer
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_path):
        path = pathlib.Path(file_path)
        self.logger.info(f"Processing file: {path}")
        try:
            content = path.read_text()
            fixed_content = self.link_fixer.fix_markdown_links(content)
            path.write_text(fixed_content)
            self.logger.info(f"Processed {path}")
        except IOError as e:
            self.logger.error(f"Error processing {path}: {e}")
