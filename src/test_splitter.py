import unittest

import functools

from splitter import block_to_block_type, text_to_textnodes, markdown_to_blocks


def printlist(lst, level=1):
    print("[")
    identation = "\t" * level
    for item in lst:
        print(identation, end="")
        if isinstance(item, list):
            printlist(item, level + 1)
        else:
            print(f"{item},")
    print(f"{identation[:-1]}]")


class TestSplitter(unittest.TestCase):
    def test_base_case(self):
        print("\n--- Testing Splitter: base case ---\n")
        text = "This is **text with an *italic* word** and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        print(f"Text: '{text}'")

        print("List of nodes:\n")
        printlist(text_to_textnodes(text))

    def test_markdown_to_html(self):
        text = """This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items"""

        expected_output = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]

        blocks = markdown_to_blocks(text)

        self.assertEqual(expected_output, blocks)

    def test_multiple_new_lines_with_spaces(self):
        text = """This is **bolded** paragraph

                
        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items


        """

        expected_output = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]

        blocks = markdown_to_blocks(text)

        self.assertEqual(expected_output, blocks)

    def test_return_nothing(self):
        text = "\n \n\n    \n"

        expected_output = []

        blocks = markdown_to_blocks(text)

        self.assertEqual(expected_output, blocks)

    def test_block_type_assignment(self):
        print("\n--- Testing Block Type detection ---\n")

        text = """```
        this is a code block
        ```

        ## This is heading

        # This is also a heading

        This is a normal paragraph

        > This is
        > a quote

        * This
        * is
        * an unordered_list"""

        expected_output = [
            "code",
            "heading",
            "heading",
            "paragraph",
            "quote",
            "unordered_list",
        ]

        blocks = markdown_to_blocks(text)

        block_types = list(map(lambda current: block_to_block_type(current), blocks))

        self.assertEqual(expected_output, block_types)

        print("\n--- End of test ---\n")
