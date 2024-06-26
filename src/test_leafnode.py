import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_exception(self):
        print("\n--- Testing LeafNode: Exception ---")
        with self.assertRaises(ValueError) as cm:
            LeafNode("p", None)
        self.assertTrue("Value cannot be None" in str(cm.exception))

    def test_node_with_props(self):
        print("\n--- Testing LeafNode: Node with props to html ---")
        node = LeafNode("a", "Best backend course!", {"href": "https://www.boot.dev"})
        print(node.to_html())
        self.assertEqual(
            node.to_html(), '<a href="https://www.boot.dev">Best backend course!</a>'
        )


if __name__ == "__main__":
    unittest.main_()
