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
        for k, v in self.props:
            attribute = f"{k}=\"{self.props[k]}"
            if len(props) == 0:
                props = attribute
            else:
                props += " " + attribute
        
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
 