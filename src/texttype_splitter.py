from textnode import TextNode, TextTypes

from htmlnode import HTMLNode, ParentNode, LeafNode


def identify_delimiter(text, index):
    if text[index : index + 2] == "**":
        return "**", 2, "bold"
    elif text[index] == "*":
        return text[index], 1, "italic"
    elif text[index] == "`":
        return text[index], 1, "code"
    else:
        return None, 1, None


def parse_text(node):
    if not isinstance(node, TextNode):
        raise ValueError(f"{node} is not a TextNode, it's a {node.__class__}")

    url = node.url
    parsed_nodes = []
    current_segment = ""
    stack = []  # Tuple with delimiter string and index
    text = node.text
    is_nested = False

    i = 0
    while i < len(text):
        delimiter, step, text_type = identify_delimiter(text, i)

        # print(f"Current stack: {stack}\nCurrent char: \"{text[i]}\"\nCurrent segment: \"{current_segment}\"\nCurrent nodes: {parsed_nodes}\n")

        if delimiter:  # Check for delimiters
            # print(f"\n| Text: '{text}'\n| I found a delimiter, which is: {delimiter} at {i} index\n")

            if stack:  # If stack isn't empty
                if (
                    stack[-1][0] == delimiter
                ):  # and the delimiter matches with the current delimiter
                    # print("\n| It's a closing delimiter")
                    start_index = stack.pop()[1]
                    nested_text = text[start_index + len(delimiter) : i]

                    if not text_type:
                        raise Exception(
                            f"A delimiter '{delimiter}' was found but no text_type was assigned"
                        )

                    if is_nested:
                        is_nested = False
                        # print(f"\n| This text: '{nested_text}' has a nested element!\n| The parse_text function will be called with this text: '{nested_text}' and this text_type: '{text_type}'\n| The TextNode will be as follows: '{repr(TextNode(nested_text, text_type))}'")
                        nested_element_list = parse_text(
                            TextNode(nested_text, text_type, url)
                        )
                        parsed_nodes.append(nested_element_list)
                    else:
                        parsed_nodes.append(TextNode(nested_text, text_type, url))
                        # print(f"\n| I would append this text: \"{nested_text}\" as \"{text_type}\"\n")

                    current_segment = ""

                else:  # If stack isn't empty but delimiter didn't match
                    # print(f"\n| Found delimiter, but it's not: '{stack[-1][0]}'. Instead, is: '{delimiter}'\n")
                    is_nested = True
            else:
                # print("\n| It's an opening delimiter\n")
                if current_segment:
                    parsed_nodes.append(
                        TextNode(current_segment, node.text_type.name, url)
                    )
                    current_segment = ""
                # Push delimiter to stack and move index
                stack.append((delimiter, i))
        else:
            current_segment += text[i]
        i += step

    # Append remaining text as a text node if any
    if current_segment:
        parsed_nodes.append(TextNode(current_segment, node.text_type.name, url))

    return parsed_nodes


def split_nodes_delimiter(old_nodes, delimiter=None, text_type="text"):
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(parse_text(node))

    return new_nodes
