import unittest

from block_to_html import markdown_to_html_node

from htmlnode import (ParentNode, LeafNode)

class TestMDToHTMLNode(unittest.TestCase):
    def test_base_case(self):
        print("\n--- Testing Markdown to HTMLNode ---\n") 
        text = """# This is a h1 *heading*

        ## This is a **h2** heading

        This is a *normal **paragraph***

        * This is
        * an unordered
        * list

        1. And this
        2. is an 
        3. **ordered** list

        `HTML` is great!"""

        parent = markdown_to_html_node(text)

        print(f"Div node:\n{parent}")

        expected_output = ParentNode("div",
            [
                ParentNode(
                    "h1",
                    [LeafNode(None, "This is a h1 "), LeafNode("i", "heading")]
                ),
                ParentNode(
                    "h2",
                    [LeafNode(None, "This is a "), LeafNode("b", "h2"), LeafNode(None, " heading")]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is a "),
                        ParentNode(
                            "i",
                            [
                                LeafNode(None, "normal "),
                                LeafNode("b", "paragraph")
                            ]
                        )
                    ]
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "This is")]),
                        ParentNode("li", [LeafNode(None, "an unordered")]),
                        ParentNode("li", [LeafNode(None, "list")])
                    ]
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "And this")]),
                        ParentNode("li", [LeafNode(None, "is an")]),
                        ParentNode("li", [LeafNode("b", "ordered"), LeafNode(None, " list")])
                    ]
                ),
                ParentNode(
                    "p",
                    [LeafNode("code", "HTML"), LeafNode(None, " is great!")]
                )
            ]
        )

        self.assertEqual(
            parent,
            expected_output
        )

        print("\n--- End of test ---\n")
