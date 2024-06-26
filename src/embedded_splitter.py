from textnode import TextNode

from extractor import extract_markdown_links, extract_markdown_images


def split_nodes_image(old_nodes):
    new_nodes = []
    current_segment = ""

    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)

        if not images:  # If no images in text, just append and continue to next node
            new_nodes.append(node)
            continue

        j = 0
        while j < len(text):
            if not images:  # All images have been extracted
                new_nodes.append(TextNode(text[j : len(text)], "text"))
                break

            char = text[j]

            # The below 'if' checks:
            # First: if the character is an '!', which is the first char of an embedded image
            # Second: if the slice after the '![' coincide with the alt text of the first image (image[0][0])
            # Third: if the slice after the '(' (which would be {4 [because of "![""]("] + len of link.text} positions to {len of image.url}) coincide with the url of the image (image[0][1])

            if (
                char == "!"
                and text[j + 2 : j + len(images[0][0]) + 2] == images[0][0]
                and text[
                    j + len(images[0][0]) + 4 : j
                    + len(images[0][0])
                    + 4
                    + len(images[0][1])
                ]
                == images[0][1]
            ):
                if current_segment:  # If there is anything before the image, append it
                    new_nodes.append(TextNode(current_segment, "text"))
                    current_segment = ""

                current_image = images.pop(0)

                # Append the TextNode of this image

                new_nodes.append(TextNode(current_image[0], "image", current_image[1]))

                len_url = len(current_image[1])
                len_alt_text = len(current_image[0])

                j = j + len_url + len_alt_text + 5  # ![]() characters
            else:
                current_segment += char
                j += 1

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    current_segment = ""

    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)

        if not links:  # If no links in text, just append and continue to next node
            new_nodes.append(node)
            continue

        j = 0
        while j < len(text):
            if not links:  # All links have been extracted
                new_nodes.append(TextNode(text[j : len(text)], "text"))
                break

            char = text[j]

            # The below 'if' checks:
            # First: if the character is an '[' which is the first char of an embedded link
            # Second: if the slice after the '[' coincide with the text of the first link (links[0][0])
            # Third: if the slice after the '(' (which would be {3 [because of "[" "]("] + len of link.text} positions to {len of link.url}) coincide with the url of the link (links[0][1])

            if (
                char == "["
                and text[j + 1 : j + len(links[0][0]) + 1] == links[0][0]
                and text[
                    j + len(links[0][0]) + 3 : j
                    + len(links[0][0])
                    + 3
                    + len(links[0][1])
                ]
                == links[0][1]
            ):
                if current_segment:  # If there is anything before the link, append it
                    new_nodes.append(TextNode(current_segment, "text"))
                    current_segment = ""

                current_link = links.pop(0)

                # Append the TextNode of this link

                new_nodes.append(TextNode(current_link[0], "link", current_link[1]))

                len_text = len(current_link[0])
                len_url = len(current_link[1])

                j = j + len_text + len_url + 4  # []() characters
            else:  # If not add the char to the string
                current_segment += char
                j += 1

    return new_nodes
