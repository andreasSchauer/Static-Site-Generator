import unittest
import textwrap
from page_generator import extract_title


class TestPageGenerator(unittest.TestCase):
    def test_extract_title_at_start(self):
        text = textwrap.dedent("""\
            # This is the heading

            This is just a regular paragraph.""")
        
        heading = extract_title(text)
        self.assertEqual(heading, "This is the heading")


    def test_extract_title_mid_text(self):
        text = textwrap.dedent("""\
            Why are there words before the heading?

            ## h2 before h1?          

            # This is the heading

            This is just a regular paragraph.""")
        
        heading = extract_title(text)
        self.assertEqual(heading, "This is the heading")
    


if __name__ == "__main__":
    unittest.main()