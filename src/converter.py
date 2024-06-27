import copy

from htmlnode import (LeafNode, ParentNode)

from textnode import (TextNode, TextTypes)

def text_node_to_html_node(text_node):
    if isinstance(text_node, list):
        final_nodes = []
        tag = get_text_type_tag(text_node[0].text_type)
        for item in text_node:
            if item.text_type == text_node[0].text_type:
                node = copy.deepcopy(item)
                node.text_type = TextTypes["text"]
            else:
                node = item
            final_nodes.append(text_node_to_html_node(node))
        return ParentNode(tag, final_nodes)
    elif isinstance(text_node, TextNode):
        text = text_node.text
        tag = get_text_type_tag(text_node.text_type)
        match tag:
            case None | "b" | "i" | "code":
                return LeafNode(tag, text)
            case "a":
                return LeafNode(tag, text, {"href": text_node.url})
            case "img":
                return LeafNode(tag, "", {"src": text_node.url, "alt": text})
            case _:
                raise ValueError(f"{text_node.text_type.name} is not supported")
    else:
        raise ValueError(f"{text_node} is not a TextNode, it's a {text_node.__class__}")

def get_text_type_tag(text_type):
    match text_type.name:
        case "text":
            return None
        case "bold":
            return "b"
        case "italic":
            return "i"
        case "code":
            return "code"
        case "link":
            return "a"
        case "image":
            return "img"
        case _:
            raise ValueError(f"{text_node.text_type.name} is not supported")
