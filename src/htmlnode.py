class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This should be overrode")

    def props_to_html(self):
        props = ""
        for k in self.props:
            attribute = f"{k}=\"{self.props[k]}\""
            if len(props) == 0:
                props = attribute
            else:
                props += " " + attribute
        return props

    def __repr__(self):
        return f"> HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        self_children = None if self.children is None else sorted(self.children)
        other_children = None if other.children is None else sorted(other.children)
        return (
            self.tag == other.tag
            and self.value == other.value
            and self_children == other_children
            and self.props == other.props
        )

    def copy(self):
        tag = self.tag
        value = self.value
        children = None if self.children is None else list(self.children)
        props = None if self.props is None else dict(self.props)
        return HTMLNode(tag, value, children, props)
 
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # May raise an ValueError if value is None?
        if value is None:
            raise ValueError("Value cannot be None")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be None")
        content = self.value
        if not self.tag is None:
            end_tag = f"</{self.tag}>"
            start_tag = f"<{self.tag}"
            if not self.props is None:
                start_tag += f" {self.props_to_html()}"
            start_tag += ">"
            return start_tag + content + end_tag
        else:
            return content
            
