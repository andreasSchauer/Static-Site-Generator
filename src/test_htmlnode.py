import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode("a", "This is a link")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("label", "This is text", ["input"], {"for": "email", "name": "email"})
        self.assertEqual(repr(node), "HTMLNode(label, This is text, ['input'], {'for': 'email', 'name': 'email'})")

    def test_props_to_html(self):
        node = HTMLNode("label", "This is text", ["input"], {"for": "email", "name": "email"})
        props = node.props_to_html()
        self.assertEqual(props, ' for="email" name="email"')

    
if __name__ == "__main__":
    unittest.main()