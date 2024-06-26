import unittest

from texttype_splitter import split_nodes_delimiter
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextTypes


class TestSplitter(unittest.TestCase):
    def test_splitter(self):
        print("\n--- Testing Splitter: base case ---\n")
        text = "This would be an *italic* sentence *including a **bold** word*."
        print(f"\n{text}\n")
        node = TextNode(text, "text")
        new_nodes = split_nodes_delimiter([node])

        expected_output = [
            TextNode("This would be an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" sentence ", "text"),
            [
                TextNode("including a ", "italic"),
                TextNode("bold", "bold"),
                TextNode(" word", "italic"),
            ],
            TextNode(".", "text"),
        ]

        self.assertEqual(new_nodes, expected_output)
