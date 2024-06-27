import functools

import logging


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
        if not isinstance(other, HTMLNode):
            return False
        
        # Compare tags
        tags_equal = self.tag == other.tag
        
        # Compare values
        values_equal = self.value == other.value
        
        # Compare children presence and their values if both are not None
        if self.children is None and other.children is None:
            children_equal = True
        elif self.children is None or other.children is None:
            children_equal = False
        else:
            # Element-wise comparison of children lists
            if len(self.children) != len(other.children):
                children_equal = False
            else:
                children_equal = all(child_self == child_other for child_self, child_other in zip(self.children, other.children))

        if not children_equal:
            for child_self, child_other in zip(self.children, other.children):
                if child_self != child_other:
                    print(f"Different child: {child_self} != {child_other}")

        
        # Compare props
        if self.props is None and other.props is None:
            props_equal = True
        elif self.props is None or other.props is None:
            props_equal = False
        else:
            props_equal = (
                all(self.props.get(k) == v for k, v in other.props.items()) # Compare "two times" because the keys may be different 
                and all(other.props.get(k) == v for k, v in self.props.items())
            )

        equal = tags_equal and values_equal and children_equal and props_equal
        
        equal_list = [tags_equal, values_equal, children_equal, props_equal]

        if not equal:
            print(f"\n| These HTMLNodes are not the same! '{equal_list}'\n| '{self}'\n| '{other}'")

        return equal


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
        if not isinstance(other, LeafNode):
            return False

        return super().__eq__(other)

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
        
        logging.getLogger(__name__).debug(f"Children: {self.children}")

        return (
            functools.reduce(
                lambda string, child: string + child.to_html(),
                self.children,
                f"<{self.tag}{self.props_to_html()}>",
            )
            + f"</{self.tag}>"
        )
    
    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False

        return super().__eq__(other)

    def __repr__(self):
        final_string = f"ParentNode(\"{self.tag}\", {self.children}"
        if self.props is not None:
            final_string += f", {self.props}"
        return final_string + ")"
