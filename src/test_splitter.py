import unittest

from textnode import TextNode

from splitter import text_to_textnodes

def printlist(lst, level=1):
    print("[")  
    identation = "\t" * level
    for item in lst:
        print(identation, end="")
        if isinstance(item, list):
            printlist(item, level+1)
        else:
            print(f"{item},")
    print(f"{identation[:-1]}]")


class TestSplitter(unittest.TestCase):
    def test_base_case(self):
        print("\n--- Testing Splitter: base case ---\n")
        text = "This is **text with an *italic* word** and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        
        print(f"Text: '{text}'")

        print(f"List of nodes:\n")
        printlist(text_to_textnodes(text))

