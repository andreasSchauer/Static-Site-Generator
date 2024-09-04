import unittest
import textwrap
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
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


if __name__ == "__main__":
    unittest.main()
