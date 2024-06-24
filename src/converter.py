from textnode import (
    TextNode,
    TextTypes
)

from htmlnode import (
    HTMLNode,
    ParentNode,
    LeafNode
)

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
            return LeafNode("a", text, { "href": text_node.url })
        case "image":
            return LeafNode("img", "", { "src": text_node.url, "alt": text })
        case _:
            raise ValueError(f"{text_node.text_type.name} is not supported")

def parse_text(node):
    
    if not isinstance(node, TextNode):
        raise ValueError(f"{node} is not a TextNode, it's a {node.__class__}")

    parsed_nodes = []
    current_segment = ""
    stack = [] # Tuple with delimiter string and index
    text = node.text

    i = 0
    while i < len(text):
        
        # print(f"Current stack: {stack}\nCurrent char: \"{text[i]}\"\nCurrent segment: \"{current_segment}\"\nCurrent nodes: {parsed_nodes}\n")
        
        if text[i] in ["*", "`"]:  # Check for delimiters 
            if text[i:i+2] in ["**"]: # Check also the next char in case it is bold
                delimiter = ( "**", i)
                step = 2
            else: # If it isn't bold then save the delimiter as the current char
                delimiter = (text[i], i)
                step = 1
            
            # print(f"\n| Text: {text}\n| I found a delimiter, which is: {delimiter} at {i} index")

            if stack: # If stack is empy
                if stack[-1][0] == delimiter[0]: # and the delimiter matches with the current delimiter
                    # print("| It's a closing delimiter")
                    start_index = stack.pop()[1]
                    nested_text = text[start_index + len(delimiter[0]):i]
                    # Process any inner text recursively
                    if delimiter[0] == "**":
                        # print(f"\n | I would append this text: \"{nested_text}\" as \"bold\"\n")
                        parsed_nodes.append(TextNode(nested_text, "bold"))
                    elif delimiter[0] == "*":
                        # print(f"\n | I would append this text: \"{nested_text}\" as \"italic\"\n")
                        parsed_nodes.append(TextNode(nested_text, "italic"))
                    elif delimiter[0] == "`":
                        # print(f"\n | I would append this text: \"{nested_text}\" as \"code\"\n")
                        parsed_nodes.append(TextNode(nested_text, "code"))
                    current_segment = ""
                    step = len(delimiter[0])
            else:
                # print("| It's an opening delimiter\n")
                if current_segment:
                    parsed_nodes.append(TextNode(current_segment, node.text_type.name))
                    current_segment = ""
                # Push delimiter to stack and move index
                stack.append(delimiter)
        else:
            current_segment += text[i]
            step = 1
        i += step
    
    # Append remaining text as a text node if any
    if current_segment:
        parsed_nodes.append(TextNode(current_segment, node.text_type.name))

    return parsed_nodes

def split_nodes_delimiter(old_nodes, delimiter=None, text_type="text"):
    new_nodes = []
    for node in old_nodes: #first splitter
        new_nodes.extend(parse_text(node))        
    for i in range(len(new_nodes)):
        for char in new_nodes[i].text:
            if char in ["*", "`"]: # If the text of one of the returned nodes has a delimiter
                new_nodes[i] = parse_text(new_nodes[i]) # Replace said node with a new list
                break # Next node

    return new_nodes
