import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode_constructor(self):
        node = HTMLNode("a", "This is a link")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_HTMLNode_repr(self):
        node = HTMLNode("label", "This is text", ["input"], {"for": "email", "name": "email"})
        self.assertEqual(repr(node), "HTMLNode(label, This is text, ['input'], {'for': 'email', 'name': 'email'})")

    def test_HTMLNode_props_to_html(self):
        node = HTMLNode("label", "This is text", ["input"], {"for": "email", "name": "email"})
        props = node.props_to_html()
        self.assertEqual(props, ' for="email" name="email"')



    def test_LeafNode_constructor(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertEqual(node.props, None)

    def test_LeafNode_to_html_no_children(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), '<p>This is a paragraph</p>')

    def test_LeafNode_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_LeafNode_to_html_no_tag(self):
        node = LeafNode(None, "I am speed")
        self.assertEqual(node.to_html(), "I am speed")



    def test_ParentNode_to_html_standard(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")



    def test_ParentNode_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: Parent Node needs children")
    


    def test_ParentNode_to_html_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("p", "I like turtles"),
                LeafNode("p", "They are very cute"),
                LeafNode(None, "chicken")
            ]
        )

        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: No tag")



    def test_ParentNode_to_html_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text")
                            ]
                        ),
                    ]
                ),
                ParentNode(
                   "div",
                    [
                        LeafNode("p", "I like turtles"),
                        LeafNode("p", "They are very cute"),
                        LeafNode(None, "chicken")
                    ] 
                )
            ],
            {
                "id": "container"
            }
        )
        self.assertEqual(node.to_html(), '<div id="container"><div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div><div><p>I like turtles</p><p>They are very cute</p>chicken</div></div>')

    
    
if __name__ == "__main__":
    unittest.main()