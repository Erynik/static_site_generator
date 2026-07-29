import unittest
from block import BlockType, block_to_block_type

class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        md = "this should just be a paragraph\nwith some newlines\nending here"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_to_block_type_code(self):
        md= "```\nthis is a code block\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_code_short(self):
        md= "```\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, block_type)
    
    def test_block_to_block_type_bad_ordered(self):
        md = "1. atext\n3. btext"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_quote(self):
        md = "> text1\n>text2\n> text3"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, block_type)
    
    def test_block_to_block_type_unordered(self):
        md = "- text1\n- text2\n- text3"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED, block_type)

    def test_block_to_block_type_ordered(self):
        md = "1. line 1\n2. text 2\n3. text four"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED, block_type)

if __name__ == "__main__":
    unittest.main()