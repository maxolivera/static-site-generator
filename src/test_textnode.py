import unittest

from textnode import (
    TextNode,
    TextTypes
)

basic_node = TextNode("This is a test", "bold")

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = basic_node.copy()
        node2 = basic_node.copy()
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = basic_node.copy()
        node2 = basic_node.copy()
        node2.url = "https://www.boot.dev"
        self.assertTrue(not node == node2)

    def test_url_null(self):
        node = basic_node.copy()
        self.assertTrue(node.url == None)
        
    def test_repr(self):
        node = basic_node.copy()
        node.text_type = TextTypes.code
        node.url = "https://www.my.web.site"
        self.assertEqual(
                "TextNode(This is a test, code, https://www.my.web.site)",
        repr(node)
        )

if __name__ == "__main__":
    unittest.main_()
