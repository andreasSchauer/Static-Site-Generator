import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertEqual(node.props, None)

    def test_to_html_no_children(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), '<p>This is a paragraph</p>')

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_tag(self):
        node = LeafNode(None, "I am speed")
        self.assertEqual(node.to_html(), "I am speed")

    
if __name__ == "__main__":
    unittest.main()