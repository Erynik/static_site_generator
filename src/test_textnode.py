import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()