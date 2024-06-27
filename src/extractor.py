import re

import logging

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def extract_title(markdown):
    logger = logging.getLogger(__name__)
    title = re.match(r"^# (.*)", markdown)
    if title is not None:
        logger.info(f"The title of the document will be: '{title.group()}'")
        return title.group(1)
    else:
        raise Exception("Missing title on file")
