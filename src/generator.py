import logging

import re

from extractor import extract_title

from block_to_html import markdown_to_html_node

import os


def generate_path(from_path: str, template_path: str, dest_path: str):
    """Generate a HTML file from a MD file to a given destination
    Args:
       from_path (str): MD file, but the function do not check it
       template_path (str): HTML file, with {{ Title }} and {{ Content }} placeholders
       dest_path (str): Where the HTML generted path will be placed
    """

    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    logger = logging.getLogger(__name__)

    if os.path.isfile(from_path):
        with open(from_path, "r", encoding="utf-8") as f:
            markdown = f.read()
    else:
        raise Exception(f"File to be converted is not valid: '{from_path}'")
   
    if os.path.isfile(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        raise Exception(f"Template file is not valid: '{template_path}'")

    html_nodes = markdown_to_html_node(markdown)
     
    # Verify HTML file has {{ Title }} and {{ Content }} placeholders
    amount_titles = len(re.findall("{{ Title }}", template))
    
    if amount_titles != 1:
        if amount_titles < 1:
            raise Exception("{{ Title }} placeholder not found")
        else:
            raise Exception("More than one {{ Title }} placeholder found")

    amount_content = len(re.findall("{{ Content }}", template))
    
    if amount_content != 1:
        if amount_content < 1:
            raise Exception("{{ Content }} placeholder not found")
        else:
            raise Exception("More than one {{ Content }} placeholder found")

    # Change title and content
    content = html_nodes.to_html()
    logger.debug(f"The content of the HTML file will be: {content}")
    title = extract_title(markdown)

    template_with_title = template.replace("{{ Title }}", title)
    document = template_with_title.replace("{{ Content }}", content)

    # If dest_path doesn't exits, create it
    dir_dest_path = os.path.dirname(dest_path)
    logger.debug(f"The destination path is: '{dir_dest_path}'")
    logger.debug(f"The destination path, including file, is: '{dest_path}'")
    

    if not os.path.isdir(dir_dest_path):
        logger.warning(f"Destination directory not found, it will be created: '{dir_dest_path}')")
        os.makedirs(dir_dest_path)

    # Create file
    with open(dest_path, "w+", encoding="utf-8") as f:
        f.write(document)

def generate_pages_recursive(dir_path_content: str, template_path:str, dest_dir_path:str):
    for path in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, path)
        if os.path.isdir(current_path):   
            logging.getLogger(__name__).debug(f"Found a directory: {current_path}'")
            new_dest = os.path.join(dest_dir_path, path)
            generate_pages_recursive(
                current_path,
                template_path,
                new_dest
            )
        elif os.path.isfile(current_path):
            if path[-3:] == ".md":
                logging.getLogger(__name__).debug(f"Found a '.md' file: {current_path}'")
                new_path = path[:-3] + ".html"
                new_dest = os.path.join(dest_dir_path, new_path)
                generate_path(
                    current_path,
                    template_path,
                    new_dest
                )
        else:
            raise Exception(f"Path invalid: '{current_path}'")
