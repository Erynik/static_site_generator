import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url_none(self):
        node = TextNode("this is a text node", TextType.BOLD, None)
        node2 = TextNode("this is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("this is a text node", TextType.CODE, "www.google.co.uk")
        node2 = TextNode("this is a text node", TextType.CODE, "www.google.co.uk")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_image(self):
        node = TextNode("alt text", TextType.IMAGE, "www.fakeimage.com/img1.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), " src=\"www.fakeimage.com/img1.jpg\" alt=\"alt text\"")

    def test_text_bold(self):
        node = TextNode("this is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a bold text")

    def test_text_italic(self):
        node = TextNode("this is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is an italic text")

    def test_text_code(self):
        node = TextNode("this is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is a code text")

    def test_text_none(self):
        node = TextNode("this is an invalid text", TextType.FANCY)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
        


if __name__ == "__main__":
    unittest.main()