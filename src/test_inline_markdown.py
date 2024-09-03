import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    extract_markdown_links,
    extract_markdown_images,
    text_to_textnodes
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_error(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "a", text_type_code)
        self.assertEqual(str(context.exception), "Invalid Markdown Syntax: Delimiter not supported")

    def test_links_with_match(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ('to boot dev', 'https://www.boot.dev'),
                ('to youtube', 'https://www.youtube.com/@bootdotdev')
            ],
            matches
        )

    def test_links_without_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_images_with_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
               ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
               ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            matches
        )

    def test_images_without_match(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_split_images_(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), my guy"
        node = TextNode(text, text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", text_type_text),
                TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", my guy", text_type_text)
            ],
            new_nodes
        )

    def test_split_images_without_text_start_end(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(text, text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", text_type_text),
                TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes
        )

    def test_split_images_without_match(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
            ]
            , new_nodes
        )

    def test_split_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), my guy"
        node = TextNode(text, text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
                TextNode(", my guy", text_type_text)
            ],
            new_nodes
        )

    def test_split_links_without_text_start_end(self):
        text = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes
        )
    
    def test_split_links_without_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), my guy"
        node = TextNode(text, text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), my guy", text_type_text)
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
