import unittest

from textnode import TextNode


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

    
if __name__ == "__main__":
    unittest.main()