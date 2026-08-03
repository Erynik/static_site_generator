import unittest
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_immediate_mixed(self):
        node = TextNode(
            "![immediate image](imgur.com/jpg.jpg) followed by a [link](www.google.com) and then some other text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("immediate image", TextType.IMAGE, "imgur.com/jpg.jpg"),
                TextNode(" followed by a [link](www.google.com) and then some other text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_images_mixed(self):
        node = TextNode(
            "![immediate image](imgur.com/jpg.jpg) followed by a [link](www.google.com) and then some other text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("![immediate image](imgur.com/jpg.jpg) followed by a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(" and then some other text", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_all_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    
    def test_all_empty_string(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_all_plain_text(self):
        text = "this is just plain text with no markdown"
        new_nodes = text_to_textnodes(text)
        self.assertEqual([TextNode("this is just plain text with no markdown", TextType.TEXT)], new_nodes)

    def test_all_one_bold(self):
        text = "this is just one bit of **bolded text** only"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("this is just one bit of ", TextType.TEXT),
                TextNode("bolded text", TextType.BOLD),
                TextNode(" only", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_all_only_bold(self):
        text = "**all of this text is bolded**"
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("all of this text is bolded", TextType.BOLD)
        ], new_nodes)

    def test_all_adjacent_all(self):
        text = "_italic_**bold**`code` text with [link](www.link.com)![and image](www.imgur.com/a.jpg)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("italic", TextType.ITALIC),
                TextNode("bold", TextType.BOLD),
                TextNode("code", TextType.CODE),
                TextNode(" text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.link.com"),
                TextNode("and image", TextType.IMAGE, "www.imgur.com/a.jpg")
            ],
            new_nodes
        )
    
    def test_all_malformed(self):
        text = "malformed **bold"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_all_double_code(self):
        text = "here's `code` and `more code` now"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("here's ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
                TextNode(" now", TextType.TEXT)
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items        
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
>this is a quote block
>over multiple lines
>that should be quoteblocked
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote block over multiple lines that should be quoteblocked</blockquote></div>"
        )

if __name__ == "__main__":
    unittest.main()
