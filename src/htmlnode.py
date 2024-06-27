import functools

import copy


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This should be overrode")

    def props_to_html(self):
        props = ""
        if self.props is not None:
            for k in self.props:
                props += f' {k}="{self.props[k]}"'
        return props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        self_children = None if self.children is None else copy.deepcopy(self.children)
        other_children = None if other.children is None else copy.deepcopy(other.children)
        if self.props is None and self.props is None:
            props_equals = True
        elif self.props is None or self.props is None:
            props_equals = False
        else:
            props_equals = all((self.props.get(k) == v for k, v in other.props.items()))

        return (
            self.tag == other.tag
            and self.value == other.value
            and self_children == other_children
            and props_equals
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # May raise an ValueError if value is None?
        if value is None:
            raise ValueError("Value cannot be None")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be None")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        super().__eq__(other)

    def __repr__(self):
        final_string = "LeafNode("

        if self.tag is not None:
            final_string += f"\"{self.tag}\""
        else:
            final_string += f"{self.tag}"

        final_string += f", \"{self.value}\""

        if self.props is not None:
            final_string += f", {self.props}"

        return final_string + ")"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A tag must be provided")
        if self.children is None:
            raise ValueError("A parent node must have children")

        return (
            functools.reduce(
                lambda string, child: string + child.to_html(),
                self.children,
                f"<{self.tag}{self.props_to_html()}>",
            )
            + f"</{self.tag}>"
        )
    
    def __repr__(self):
        final_string = f"ParentNode(\"{self.tag}\", {self.children}"
        if self.props is not None:
            final_string += f", {self.props}"
        return final_string + ")"
