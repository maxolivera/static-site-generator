from htmlnode import (
    ParentNode,
    LeafNode
)

import copy

import unittest

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        print("\n--- Testing ParentNode: Equals ---")
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        print(node.to_html())

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_grandparent_eq(self):
        print("\n--- Testing ParentNode: Grandparent node ---")
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        parent_node = copy.deepcopy(node)
        parent_node.children.append(node)

        print(parent_node.to_html())

        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>"
        )

    def test_exception(self):
        print("\n--- Testing ParentNode: Exception ---")
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, LeafNode("p", "this is a paragraph.")).to_html()

        self.assertTrue("A tag must be provided" in str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            ParentNode("h2", None).to_html()
        self.assertTrue("A parent node must have children" in str(cm.exception))
       
if __name__ == "__main__":
    unittest.main_()
