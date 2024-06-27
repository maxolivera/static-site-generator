import logging

import argparse

from copy_files import copy_files

import os

from generator import generate_path


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
    md_files = []

    if os.path.isdir(content_dir):
        content_dir_files = os.listdir(content_dir)
        if len(content_dir_files) == 0:
            raise Exception("No files on 'content' folder")
        for file in content_dir_files:
            if file[-3:] == ".md":
                md_files.append(file)
        logger.info(f"{len(md_files)} '.md' files found")

    template_file = None

    for file in list_files:
        if file == "template.html":
            if template_file is None:
                template_file = file
            else:
                raise Exception("More than one 'template.html' found")

    if template_file is None:
        raise Exception("'template.html' file not found")

    for file in md_files:
        logger.info(f"Generating '{file[:-3]}.html' file of {file}")
        generate_path(
            os.path.join(content_dir, file),
            template_file,
            os.path.join("public", file[:-3] + ".html")
        )

main()
