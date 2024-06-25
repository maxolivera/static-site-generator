from embedded_splitter import (split_nodes_image, split_nodes_link)

from textnode import (TextNode, TextTypes)

from texttype_splitter import (split_nodes_delimiter)

def text_to_textnodes(text):
    node = TextNode(text, "text")
    print("\nExtracting embedded:\n")
    mid_nodes = split_nodes_link(split_nodes_image([node]))
    print(f"{mid_nodes}\nExtracting other text types:")
    final_nodes = split_nodes_delimiter(mid_nodes)
    print(f"{final_nodes}")
    return final_nodes
