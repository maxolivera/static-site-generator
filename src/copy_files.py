import shutil

import logging

import os

def copy_files():
    logger = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO)

    # Check if static dir exits
    if not os.path.exists("static"):
        raise Exception("There is no 'static' directory")
    else:
        # Check if static dir is empty
        if len(os.listdir("static")) == 0:
            logger.warning("'static' directory is empty")
            return

    # Check if public dir exists, in such case remove it
    if os.path.exists("public"):
        logger.warning("'public' directory found, it will be deleted")
        shutil.rmtree("public")
    
    os.mkdir("public")

    # Start copying the files
    copy_to_other_dir("static", "public")


def copy_to_other_dir(origin: str, destiny: str):
    for item in os.listdir(origin):
        logging.info(f"Found something: '{item}' inside of '{origin}'")
        item_path = os.path.join(origin, item)
        if os.path.isdir(item_path):
            new_origin = os.path.join(origin, item)
            new_destiny = os.path.join(destiny, item)

            logging.info(f"It's a directory, inside of '{origin}'")
            logging.info(f"Creating new directory: '{new_destiny}'")

            os.mkdir(new_destiny)
            copy_to_other_dir(new_origin, new_destiny)
        elif os.path.isfile(item_path):
            logging.info(f"It's a file. Copying it to '{destiny}'")
            shutil.copy(item_path, destiny)
        else:
            logging.critical(f"{item} is not file nor directory")
