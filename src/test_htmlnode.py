from htmlnode import HTMLNode

import unittest

p_node = HTMLNode(
        "p",
        "This is a text node" 
        )

a_node = HTMLNode(
        "a",
        "boot.dev",
        None,
        {
            "href": "https://www.boot.dev",
            "target": "_blank"
        }
        )

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = p_node.copy()
        node2 = p_node.copy()
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = p_node.copy()
        node2 = a_node.copy()
        self.assertTrue(not node == node2)

    def test_children(self):
        childrens = []
        for i in range(5):
            node = p_node.copy()
            node.value = f"This is p node #{i}"
            childrens.append(node)
        node2 = a_node.copy()
        node2.children = childrens
        self.assertEqual(
                f"> HTMLNode(a, boot.dev, {childrens}, {node2.props})",
                repr(node2)
                )
