class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        html_props = ""

        for prop in self.props:
            html_props += f' {prop}="{self.props[prop]}"'

        return html_props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: No value")
        
        if self.tag == None:
            return self.value

        props = self.props_to_html()
        return f'<{self.tag}{props}>{self.value}</{self.tag}>'