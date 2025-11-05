
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        st = ''
        if self.props:
            for prop in self.props:
                st += f' {prop}="{self.props[prop]}"' if self.props[prop] != '' else f' {prop}'
        return st

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode requires a value")
        if self.tag == None:
            return f'{self.value}'
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(node1, node2):
        if (
                node1.tag == node2.tag
                and node1.value == node2.value
                and node1.props == node2.props
            ):
            return True
        return False

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode requires a tag")
        if self.children == None:
            raise ValueError("ParentNode requires children")
        else:
            html = ''
            for child in self.children:
                html += child.to_html()

            return f'<{self.tag}{self.props_to_html()}>{html}</{self.tag}>'

    def __eq__(node1, node2):
        if (
                node1.tag == node2.tag
                and node1.children == node2.children
                and node1.props == node2.props
            ):
            return True
        return False
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

