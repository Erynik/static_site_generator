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

if __name__ == "__main__":
    unittest.main()