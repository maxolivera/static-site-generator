import unittest

from extractor import extract_markdown_images, extract_markdown_links


class TestExtractor(unittest.TestCase):
    def test_images_extractor(self):
        print("\n--- Testing Extractor: image extraction ---\n")
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_output = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]

        images = extract_markdown_images(text)
        try:
            self.assertEqual(images, expected_output)
            print("\n--- End of test: Everything OK ---\n")
        except AssertionError as ae:
            print("\n| Fail test!\n")
            print(
                f"| Text: '{text}'\n\n| Expected output: '{expected_output}'\n| Actual output: '{images}'"
            )
        except Exception as e:
            print(f"\n| Something went wrong!\n| Exception: {e}\n")

    def test_links_extractor(self):
        print("\n--- Testing Extractor: link extraction ---\n")
        text = "This is an [example](https://www.example.com) and this is other [link](https://www.boot.dev)"
        expected_output = [
            ("example", "https://www.example.com"),
            ("link", "https://www.boot.dev"),
        ]

        links = extract_markdown_links(text)

        try:
            self.assertEqual(links, expected_output)
            print("\n--- End of test: Everything OK ---\n")
        except AssertionError as ae:
            print("\n| Fail test!\n")
            print(
                f"| Text: '{text}'\n\n| Expected output: '{expected_output}'\n| Actual output: '{links}'"
            )
        except Exception as e:
            print(f"\n| Something went wrong!\n| Exception: {e}\n")
