from enum import Enum

TextTypes = Enum("TextType",
        [
            "text",
            "bold",
            "italic",
            "code",
            "link",
            "image"
        ])

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextTypes[text_type]
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
