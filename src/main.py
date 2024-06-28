import logging

import argparse

from copy_files import copy_files

import os

from generator import generate_pages_recursive


def main():
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument( '-log',
                         '--loglevel',
                         default='warning',
                         help='Provide logging level. Example --loglevel debug, default=warning' )

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel.upper())
    logging.info("Logging now setup.")
    
    logging.info("Copying static files")
    copy_files()

    list_files = os.listdir()
    
    content_dir = "content"

    template_file = None

    for file in list_files:
        if file == "template.html":
            if template_file is None:
                template_file = file
            else:
                raise Exception("More than one 'template.html' found")

    if template_file is None:
        raise Exception("'template.html' file not found")

    generate_pages_recursive(
        content_dir,
        template_file,
        "public/"
    )

main()
