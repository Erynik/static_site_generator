

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        result = []
        for prop, val in self.props.items():
            result.append(f' {prop}="{val}"')
        final = "".join(result)
        return final
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props: dict | None = None):
        super().__init__(tag, value, children = None, props = props)

    def to_html(self):
        if not self.value:
            raise ValueError(f"LeafNode must have a value.")
        if not self.tag:
            return f"{self.value}"
        else:
            props = self.props_to_html()
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props: dict | None = None):
        super().__init__(tag = tag, value = None, children = children, props = props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Node must have a tag.")
        if self.children is None:
            raise ValueError("Parent Node requires children.")
        else:
            open_tag = f"<{self.tag}>"
            closing_tag = f"</{self.tag}>"
            child_vals = ""
            for child in self.children:
                child_vals += child.to_html()
            return f"{open_tag}{child_vals}{closing_tag}"
