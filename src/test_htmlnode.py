from htmlnode import HTMLNode

import copy

import unittest

p_node = HTMLNode("p", "This is a text node")

a_node = HTMLNode(
    "a", "boot.dev", None, {"href": "https://www.boot.dev", "target": "_blank"}
)


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = copy.deepcopy(p_node)
        node2 = copy.deepcopy(p_node)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = copy.deepcopy(p_node)
        node2 = copy.deepcopy(a_node)
        self.assertTrue(not node == node2)

    def test_children(self):
        childrens = []
        for i in range(5):
            node = copy.deepcopy(p_node)
            node.value = f"This is p node #{i}"
            childrens.append(node)
        node2 = copy.deepcopy(a_node)
        node2.children = childrens
        self.assertEqual(
            f"> HTMLNode(a, boot.dev, {childrens}, {node2.props})", repr(node2)
        )

    def test_props_to_html(self):
        node = copy.deepcopy(a_node)
        self.assertEqual(
            f' href="https://www.boot.dev" target="_blank"', node.props_to_html()
        )


if __name__ == "__main__":
    unittest.main_()
