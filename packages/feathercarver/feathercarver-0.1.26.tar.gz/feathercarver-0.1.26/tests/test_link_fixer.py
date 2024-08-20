from feathercarver.link_fixer import LinkFixer


def test_fix_markdown_links():
    link_fixer = LinkFixer()
    input_content = """
   [Link 1
   
   ](https://example.com)

   Normal text

   ```
   [Code block link
   ](https://example.com)
   ```

   [Link 2
   ](https://another-example.com)
   """

    expected_output = """
   [Link 1](https://example.com)

   Normal text

   ```
   [Code block link
   ](https://example.com)
   ```

   [Link 2](https://another-example.com)
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_link_with_title():
    link_fixer = LinkFixer()
    input_content = """
   [Link with title](https://example.com "Example Title")
   """

    expected_output = """
   [Link with title](https://example.com "Example Title")
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_link_with_title_and_newlines():
    link_fixer = LinkFixer()
    input_content = """
   [
   Link
   
   with
   
   title
   ](
   
   https://example.com
   "Example
   
   Title"
   )
   """

    expected_output = """
   [Link with title](https://example.com "Example Title")
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_link_with_single_quotes_title():
    link_fixer = LinkFixer()
    input_content = """
   [Link with single quotes](https://example.com 'Single Quotes Title')
   """

    expected_output = """
   [Link with single quotes](https://example.com 'Single Quotes Title')
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_multiple_links_with_titles():
    link_fixer = LinkFixer()
    input_content = """
   [Link 1](url1 "Title 1")

   Some text

   [Link 2](url2 "Title 2")

   More text

   [Link 3](url3 "Title 3")
   """

    expected_output = """
   [Link 1](url1 "Title 1")

   Some text

   [Link 2](url2 "Title 2")

   More text

   [Link 3](url3 "Title 3")
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_link_with_escaped_characters_in_title():
    link_fixer = LinkFixer()
    input_content = """
   [Link with escaped characters](https://example.com "Title with \"Quotes\" and \\Backslashes")
   """

    expected_output = """
   [Link with escaped characters](https://example.com "Title with \"Quotes\" and \\Backslashes")
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_link_with_parentheses_in_url():
    link_fixer = LinkFixer()
    input_content = """
   [Link with parentheses](https://example.com/path/(with)/parentheses "Title")
   """

    expected_output = """
   [Link with parentheses](https://example.com/path/(with)/parentheses "Title")
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_link_with_special_characters_in_text_and_url():
    link_fixer = LinkFixer()
    input_content = """
   [Link with !@#$%^&*()__+special 
   
   characters](https://example.com/!@#$%^&*()__+special/characters "Title with !@#$%^&*()__+special characters")
   """

    expected_output = """
   [Link with !@#$%^&*()__+special characters](https://example.com/!@#$%^&*()__+special/characters "Title with !@#$%^&*()__+special characters")
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_nested1():
    link_fixer = LinkFixer()
    input_content = """
[

![name](https://name.com)

](https://name2.com)
   """

    expected_output = """
[![name](https://name.com)](https://name2.com)
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_nested2():
    link_fixer = LinkFixer()
    input_content = """
[

![name](https://name.com)

](https://name2.com)[

![name3](https://name3.com)

](https://name4.com)
   """

    expected_output = """
[![name](https://name.com)](https://name2.com)[![name3](https://name3.com)](https://name4.com)
   """

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_image_links():
    link_fixer = LinkFixer()
    input_content = """
![[Pasted image 20240228064725.png]]

![[Pasted image 20240228064723.png]]
"""

    expected_output = input_content

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_slow():
    link_fixer = LinkFixer()
    input_content = """
[a](https://a.com)
Keywords: program to an interface
   """

    expected_output = input_content

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_slow2():
    link_fixer = LinkFixer()
    input_content = """
[a](http://a.aaa) aaa aaaa aaa aaa aaa aaa aaa aaa aaa aaa aaa aaa
   """

    expected_output = input_content

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_slow3():
    link_fixer = LinkFixer()
    input_content = """
- [[test - test test test test test test test test test test test test test test test test test test test test test test test test test test test test]]
"""

    expected_output = input_content

    assert link_fixer.fix_markdown_links(input_content) == expected_output


def test_modified_link_alongside_code_block_link():
    link_fixer = LinkFixer()
    input_content = """
[

koffeinsource/go-imgur: Go library to use the imgur.com API](https://github.com/koffeinsource/go-imgur?tab=readme-ov-file "koffeinsource/go-imgur: Go library to use the imgur.com API")

```
[

koffeinsource/go-imgur: Go library to use the imgur.com API](https://github.com/koffeinsource/go-imgur?tab=readme-ov-file "koffeinsource/go-imgur: Go library to use the imgur.com API")
```
"""

    expected_output = """
[koffeinsource/go-imgur: Go library to use the imgur.com API](https://github.com/koffeinsource/go-imgur?tab=readme-ov-file "koffeinsource/go-imgur: Go library to use the imgur.com API")

```
[

koffeinsource/go-imgur: Go library to use the imgur.com API](https://github.com/koffeinsource/go-imgur?tab=readme-ov-file "koffeinsource/go-imgur: Go library to use the imgur.com API")
```
"""

    assert link_fixer.fix_markdown_links(input_content) == expected_output
