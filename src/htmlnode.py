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
        raise NotImplementedError()
