import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("hello", "italic", "https://www.google.com")
        node2 = TextNode("hello", "italic", "https://www.google.com")
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("hello", "italic", "https://www.google.com")
        node2 = TextNode("This is a text node", "bold", "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("hello", "italic", "https://www.google.com")
        node2 = TextNode("hello", "italic")
        self.assertNotEqual(node, node2)

    def test_eq5(self):
        node = TextNode("hello", "italic", "https://www.google.com")
        node2 = TextNode("hello", "italic", None)
        self.assertNotEqual(node, node2)



    def test_text_to_html_blank_text(self):
        node = TextNode("This should have no tag", "text")
        self.assertEqual(repr(text_node_to_html_node(node)), 'LeafNode(None, This should have no tag, None)')

    def test_text_to_html_bold(self):
        node = TextNode("This should be bold", "bold")
        self.assertEqual(repr(text_node_to_html_node(node)), 'LeafNode(b, This should be bold, None)')

    def test_text_to_html_italic(self):
        node = TextNode("This should be italic", "italic")
        self.assertEqual(repr(text_node_to_html_node(node)), 'LeafNode(i, This should be italic, None)')

    def test_text_to_html_code(self):
        node = TextNode("This should be code", "code")
        self.assertEqual(repr(text_node_to_html_node(node)), 'LeafNode(code, This should be code, None)')

    def test_text_to_html_link(self):
        node = TextNode("This is a link", "link", "https://www.google.com")
        self.assertEqual(repr(text_node_to_html_node(node)), "LeafNode(a, This is a link, {'href': 'https://www.google.com'})")

    def test_text_to_html_image(self):
        node = TextNode("This is an image", "image", "https://www.google.com")
        self.assertEqual(repr(text_node_to_html_node(node)), "LeafNode(img, , {'src': 'https://www.google.com', 'alt': 'This is an image'})")

    def test_text_to_html_error(self):
        node = TextNode("Error", "error")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid text type")
    


if __name__ == "__main__":
    unittest.main()