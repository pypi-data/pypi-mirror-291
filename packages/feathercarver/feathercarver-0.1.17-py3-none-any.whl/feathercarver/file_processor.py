import logging
import pathlib


class FileProcessor:
    def __init__(self, link_fixer):
        self.link_fixer = link_fixer
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_path):
        path = pathlib.Path(file_path)
        self._log_processing(path)
        if self._read_process_write(path):
            self._log_processed(path)

    def _log_processing(self, path):
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(f"Processing file: {path}")

    def _log_processed(self, path):
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(f"Processed {path}")

    def _read_process_write(self, path):
        content = self._read_file(path)
        if content is None:
            return False

        fixed_content = self._fix_content(content)
        if fixed_content == content:
            return True

        return self._write_file(path, fixed_content)

    def _read_file(self, path):
        try:
            return path.read_text()
        except IOError as e:
            self._log_error("reading", path, e)
            return None

    def _fix_content(self, content):
        return self.link_fixer.fix_markdown_links(content)

    def _write_file(self, path, content):
        try:
            path.write_text(content)
            return True
        except IOError as e:
            self._log_error("writing to", path, e)
            return False

    def _log_error(self, action, path, error):
        self.logger.error(f"Error {action} {path}: {error}")
