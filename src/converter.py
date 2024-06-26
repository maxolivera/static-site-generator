from htmlnode import LeafNode

from textnode import TextNode


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError(f"{text_node} is not a TextNode, it's a {text_node.__class__}")
    text = text_node.text
    match text_node.text_type.name:
        case "text":
            return LeafNode(None, text)
        case "bold":
            return LeafNode("b", text)
        case "italic":
            return LeafNode("i", text)
        case "code":
            return LeafNode("code", text)
        case "link":
            return LeafNode("a", text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text})
        case _:
            raise ValueError(f"{text_node.text_type.name} is not supported")
