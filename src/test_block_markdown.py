import unittest
import textwrap
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    get_heading_tag,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_code,
    block_type_heading,
    block_type_olist,
    block_type_ulist,
    block_type_quote
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = textwrap.dedent("""\
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item""")

        markdown_blocks = markdown_to_blocks(text)
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ],
            markdown_blocks
        )

    def test_markdown_to_blocks_two_lists(self):
        text = textwrap.dedent("""\
            * This should be a separate list from the second one
            * This is the second item

            * This is the first list item in a list block
            * This is a list item
            * This is another list item

            This is a paragraph.

            This is another paragraph.""")

        markdown_blocks = markdown_to_blocks(text)
        self.assertListEqual(
            [
                '* This should be a separate list from the second one\n* This is the second item',
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item',
                'This is a paragraph.',
                'This is another paragraph.'
            ],
            markdown_blocks
        )

    def test_markdown_to_blocks_one_block(self):
        text = "This is only one single line of text"

        markdown_blocks = markdown_to_blocks(text)
        self.assertListEqual(
            [
                'This is only one single line of text'
            ],
            markdown_blocks
        )



    def test_block_to_block_type_paragraph(self):
        text = "This is a paragraph"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type_paragraph, block_type)

    def test_block_to_block_type_heading(self):
        text = "### This is a heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type_heading, block_type)
    
    def test_block_to_block_type_code(self):
        text = textwrap.dedent("""\
            ```
            for item in items:
                print("no")
            ```""")
        block_type = block_to_block_type(text)
        self.assertEqual(block_type_code, block_type)

    def test_block_to_block_type_quote(self):
        text = textwrap.dedent("""\
            >this is so inspiring
            >I could cry
            >but I won't.""")
        block_type = block_to_block_type(text)
        self.assertEqual(block_type_quote, block_type)

    def test_block_to_block_type_ul(self):
        text = textwrap.dedent("""\
            * This is the first list item in a list block
            * This is a list item
            * This is another list item""")
        block_type = block_to_block_type(text)
        self.assertEqual(block_type_ulist, block_type)

    def test_block_to_block_type_ol(self):
        text = textwrap.dedent("""\
            1. This is the first list item in a list block
            2. This is a list item
            3. This is another list item""")
        block_type = block_to_block_type(text)
        self.assertEqual(block_type_olist, block_type)



    def test_heading_tag_1(self):
        text = "### heading# sdjfio"
        tag = get_heading_tag(text)
        self.assertEqual("h3", tag)

    def test_heading_tag_2(self):
        text = "##### #heading"
        tag = get_heading_tag(text)
        self.assertEqual("h5", tag)

    def test_heading_tag_error(self):
        text = "heading"
        with self.assertRaises(ValueError) as context:
            get_heading_tag(text)
        self.assertEqual(str(context.exception), "Input is not a heading block")

    
    
    def test_paragraph(self):
        md = textwrap.dedent("""\
            This is **bolded** paragraph
            text in a p
            tag here""")

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = textwrap.dedent("""\
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with *italic* text and `code` here""")

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = textwrap.dedent("""
            - This is a list
            - with items
            - and *more* items

            1. This is an `ordered` list
            2. with items
            3. and more items""")

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = textwrap.dedent("""\
            # this is an h1

            this is paragraph text

            ## this is an h2""")

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = textwrap.dedent("""
            > This is a
            > blockquote block

            this is paragraph text""")

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    

if __name__ == "__main__":
    unittest.main()