import unittest

from embedded_splitter import (split_nodes_link, split_nodes_image)

from textnode import (TextTypes, TextNode)

class TestEmbeddedSplitter(unittest.TestCase):
    def test_split_image(self):
        print("\n--- Testing Embedded Splitter: image ---\n")
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        expected_output = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode("second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]

        nodes = split_nodes_image([TextNode(text, "text")])

        try:
            self.assertEqual(
                expected_output,
                nodes
            )
            print("\n--- End of test: Everything OK ---\n")
        except AssertionError as ae:
            print("\n| Test failed!\n")
            print(f"\n| Text: '{text}'\n\n| Expected output: '{expected_output}'\n| Actual output:   '{nodes}'")
        except Exception as e:
            print(f"\n| Something went wrong!\n | Exception: {e}\n")

    def test_split_link(self):
        print("\n--- Testing Embedded Splitter: link ---\n")
        text = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        expected_output = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode("second image", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]

        nodes = split_nodes_link([TextNode(text, "text")])

        try:
            self.assertEqual(
                expected_output,
                nodes
            )
            print("\n--- End of test: Everything OK ---\n")
        except AssertionError as ae:
            print("\n| Test failed!\n")
            print(f"\n| Text: '{text}'\n\n| Expected output: '{expected_output}'\n| Actual output: '{nodes}'")
        except Exception as e:
            print(f"\n| Something went wrong!\n | Exception: {e}\n")
