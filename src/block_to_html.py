import re

from htmlnode import ParentNode

from converter import text_node_to_html_node

from splitter import ( text_to_textnodes, block_to_block_type, markdown_to_blocks)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    blocks_types = list(map(lambda block: block_to_block_type(block), blocks))

    tags = []
    clean_text = []

    for i in range(len(blocks_types)):
        current_lines = blocks[i].split("\n")
        match blocks_types[i]:
            case "quote":
                tags.append("blockquote")
                clean_text.append(prefix_extractor(r"> ", current_lines))
            case "unordered_list":
                tags.append("ul")
                clean_text.append(prefix_extractor(r"\* ", current_lines))
            case "ordered_list":
                tags.append("ol")
                clean_text.append(prefix_extractor("\d. ", current_lines))
            case "heading":
                if len(current_lines) > 1:
                    raise ValueError(f"A heading cannot have more than 1 line. {current_lines[0]}")
                print(current_lines[0])
                print(re.findall(r"^(#+)", current_lines[0]))
                level = len(re.findall(r"^(#+)", current_lines[0])[0])
                print(level)
                if level > 6 or not level:
                    raise ValueError( \
                        f"The following heading has an invalid amount of '#': {level}" \
                    )
                tags.append(f"h{level}")
                clean_text.append([current_lines[0][level+1:]])
            case "code":
                tags.append("code")
                clean_text.append(current_lines[3:-3].split("\n"))
            case "paragraph":
                tags.append("p")
                clean_text.append(current_lines)

    for i in range(len(clean_text)):
        print(f"| Tag: '{tags[i]}', text: '{clean_text[i]}'")

    text_node_list = []

    for lines in clean_text:
        if len(lines) == 1:
            text_node_list.append(text_to_textnodes(lines[0]))
        elif len(lines) > 1:
            lines_to_append = []
            for line in lines:
                new_list = text_to_textnodes(line)
                if len(new_list) == 1:
                    lines_to_append.append(new_list)
                else:
                    lines_to_append.append(new_list)
            print(f"\n| LINES TO APPEND: {lines_to_append}\n")
            text_node_list.append(lines_to_append)
        else:
            raise Exception(f"This list has a invalid len: {len(lines)}. List: {lines}")

    text_node_and_tags_list = list(zip(
        text_node_list,
        tags
    ))
    
    print(f"\n| Text nodes list with tags:\n\n{text_node_list}\n")

    children = []
    
    for text_node in text_node_and_tags_list:
        if len(children) > 1:
            print(f"\n| Previous child: {children[-1]}")
        print(f"\n| Current children: {children}\n")
        print(f"\nText node: {text_node}\n")
        tag = text_node[1]
        nodes = text_node[0]
        print(f"| Tag: {tag}. Nodes: {nodes}\n")
        match tag:
            case "ul":
                children.append(
                        ParentNode(
                            tag,
                            list(
                                map(lambda node: ParentNode("li", list(map(lambda line: text_node_to_html_node(line), node))),
                                    nodes
                                    )
                            )
                        )
                )
            case "ol":
                children.append(
                        ParentNode(
                            tag,
                            list(
                                map(lambda node: ParentNode("li", list(map(lambda line: text_node_to_html_node(line), node))),
                                    nodes
                                    )
                            )
                    )
                )
            case "code":
                children.append(
                        ParentNode(
                            "pre",
                            ParentNode(tag, list(map(lambda node: text_node_to_html_node(node)), nodes)))
                )
            case "quote":
                children.append(
                        ParentNode(
                            tag,
                            list(map(lambda node: text_node_to_html_node(node), nodes))
                        )
                )
            case tag if tag[:1] == "h":
                print(f"\n| These are the nodes: {list(nodes)}\n")
                children.append(
                        ParentNode(
                            tag,
                            list(map(lambda node: text_node_to_html_node(node), nodes))
                        )
                )
            case "p":
                children.append(
                        ParentNode(
                            tag,
                            list(map(lambda node: text_node_to_html_node(node), nodes))
                        )
                )

    return ParentNode("div", children)

def prefix_extractor(prefix, lines):
    new_lines = []
    regex_prefix = r"^" + prefix + r"(.*)"
    for line in lines:
        result = re.findall(regex_prefix, line)
        new_lines.append(result[0])
    print(f"\n| RESULT: {new_lines}\n")
    return new_lines
