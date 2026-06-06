import unittest
from generator_functions import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract(self):
        markdown = """
# This is the title.         

## This is another header.

# Oops i put another title here, but it should immediately terminate on the first title given.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is the title.")


if __name__ == "__main__":
    unittest.main()
