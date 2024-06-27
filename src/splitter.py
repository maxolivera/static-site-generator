from embedded_splitter import split_nodes_image, split_nodes_link

from textnode import TextNode

from enum import Enum

from texttype_splitter import split_nodes_delimiter

BlockType = Enum(
    "BlockType",
    ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"],
)


def text_to_textnodes(text):
    if isinstance(text, list):
        final_nodes = []
        for item in text:
            final_nodes.append(text_to_textnodes(item))
    elif not isinstance(text, str):
        raise TypeError(f"The text is not a string, is a {text.__class__}.\nText:{text}")
    else:
        node = TextNode(text, "text")
        print("\nExtracting embedded:\n")
        mid_nodes = split_nodes_link(split_nodes_image([node]))
        print(f"{mid_nodes}\nExtracting other text types:")
        final_nodes = split_nodes_delimiter(mid_nodes)
        print(f"{final_nodes}")
    return final_nodes


def markdown_to_blocks(markdown):
    texts = markdown.split("\n")
    current_text = ""
    blocks = []
    for text in texts:
        text = text.strip()
        if text == "" and current_text:
            blocks.append(current_text)
            current_text = ""
        elif current_text:
            current_text += "\n" + text
        else:
            current_text = text
    if current_text:
        blocks.append(current_text)
    return blocks


def block_to_block_type(block):
    if "# " in block[:8]:
        return BlockType["heading"].name
    if "```" == block[:3] and "```" == block[-3:]:
        return BlockType["code"].name
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True

    lines = block.split("\n")

    for i in range(len(lines)):
        # print(
        #    f"| Line: {i}. First two chars: '{lines[i][:2]}'\n| Initial state: quotes: {is_quote}, ord list: {is_ordered_list}, unord list: {is_unordered_list}"
        # )
        if lines[i][:2] not in ["* ", "- "]:
            is_unordered_list = False
        if not lines[i][:3] == f"{i+1}. ":
            is_ordered_list = False
        if lines[i][:2] != "> ":
            is_quote = False
        # print(
        #        f"| End state: quotes: {is_quote}, ord list: {is_ordered_list}, unord list: {is_unordered_list}"
        # )
        # print(f"| Current line: '{lines[i]}'\n")

    if (is_quote and is_ordered_list or is_quote and is_unordered_list) or (
        is_ordered_list and is_unordered_list
    ):
        raise Exception("Nested type of blocks not supported")

    if is_quote:
        return BlockType["quote"].name
    elif is_unordered_list:
        return BlockType["unordered_list"].name
    elif is_ordered_list:
        return BlockType["ordered_list"].name
    else:
        return BlockType["paragraph"].name
