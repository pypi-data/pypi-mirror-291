import logging
import re


class LinkFixer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pattern = re.compile(
            r"""
      (?<!\[)             # Negative lookbehind for [
      \[                  # Opening square bracket
      (?P<text>           # Named capturing group for link text
          (?:             # Non-capturing group
              [^\[\]]     # Any character except [ or ]
              |           # OR
              \[(?!])     # [ not followed by ]
          )*              # Zero or more times
      )                   # End named capturing group for link text
      \]                  # Closing square bracket
      (?=\s*\()           # Positive lookahead for optional whitespace and (
      \s*\(               # Optional whitespace and opening parenthesis
      \s*                 # Optional whitespace
      (?P<url>            # Named capturing group for URL
          (?:             # Non-capturing group
              [^()\s]+    # One or more non-space, non-parenthesis characters
              (?:         # Non-capturing group
                  \([^()]*\)  # Parentheses and their contents
                  [^()\s]*   # Followed by zero or more non-space, non-parenthesis characters
              )*          # Zero or more times
          )               # End non-capturing group
      )                   # End named capturing group for URL
      (?:                 # Non-capturing group for optional title
          \s+             # Required whitespace before title
          (?P<title>      # Named capturing group for title
              ["']        # Opening quote (single or double)
              (?:         # Non-capturing group
                  [^"'\\]|\\.|["'](?!\))  # Any char except quotes or backslash, or escaped char, or quote not followed by )
              )*          # Zero or more times
              ["']        # Closing quote (single or double)
          )               # End named capturing group for title
      )?                  # Title is optional
      \s*                 # Optional whitespace
      \)                  # Closing parenthesis
      (?!\()              # Negative lookahead for (
  """,
            re.VERBOSE,
        )

        self.block_pattern = re.compile(
            r"""
      (?P<code>           # Named capturing group for code blocks
          (?:             # Non-capturing group for block or inline code
              ```[\s\S]*?```  # Block code
              |               # OR
              `[^`\n]+?`      # Inline code
          )
      )
  """,
            re.VERBOSE,
        )

    def fix_markdown_links(self, content):
        blocks = self.block_pattern.split(content)

        for i in range(len(blocks)):
            if not self.block_pattern.match(blocks[i]):
                self.logger.debug(f"processing block: {blocks[i]}")
                blocks[i] = self.pattern.sub(self._replace_link, blocks[i])

        return "".join(blocks)

    def _replace_link(self, match):
        link_text = re.sub(r"\s+", " ", match.group("text").strip())
        url = re.sub(r"\s+", " ", match.group("url").strip())
        title = match.group("title")
        if title:
            title = re.sub(r"\s+", " ", title.strip())
            self.logger.debug(f"Fixed link: [{link_text}]({url} {title})")
            return f"[{link_text}]({url} {title})"
        else:
            self.logger.debug(f"Fixed link: [{link_text}]({url})")
            return f"[{link_text}]({url})"
