import unittest
from markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestMarkDown(unittest.TestCase):
    def test_markdown_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_markdown_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_markdown_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_markdown_unbalanced(self):
        node = TextNode("this is text with an **unbalanced delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "**", TextType.BOLD)

    def test_markdown_no_delim(self):
        node = TextNode("this is text with no matching delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()