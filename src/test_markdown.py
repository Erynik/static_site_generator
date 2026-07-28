import unittest
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
    
    def test_regex_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://google.co.uk/) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_two_links(self):
        matches = extract_markdown_links("This is a text with two [link](http://google.com/) normal [links](https://bing.com/)")
        self.assertListEqual(matches, [("link", "http://google.com/"), ("links", "https://bing.com/")])

    def test_extract_markdown_links_with_image(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.co.uk/) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://google.co.uk/")], matches)

    def test_extract_markdown_boot(self):
        matches = extract_markdown_images("![alt](url) some text ![alt2](url2)")
        self.assertListEqual(matches, [("alt", "url"), ("alt2", "url2")])

if __name__ == "__main__":
    unittest.main()