import unittest
from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "www.google.co.uk", "target": "_blank"})
        res = HTMLNode.props_to_html(node)
        self.assertEqual(res, ' href="www.google.co.uk" target="_blank"')
    
    def test_props_to_html_none(self):
        node = HTMLNode(None)
        res = HTMLNode.props_to_html(node)
        self.assertEqual(res, "")

    def test_props_to_html_tagged(self):
        node = HTMLNode(tag = "<h1>", value="Test Title", props={
            "title": "Testing Title",
            "autocapitalize": "words"
        } )
        res = HTMLNode.props_to_html(node)
        self.assertEqual(res, ' title="Testing Title" autocapitalize="words"')

    def test_leafnodes_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        res = LeafNode.to_html(node)
        self.assertEqual(res, "<p>This is a paragraph of text.</p>")

    def test_leafnodes_html_with_props(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        res = LeafNode.to_html(node)
        self.assertEqual(res, "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leafnodes_no_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            LeafNode.to_html(node)

    def test_leafnodes_tag_h1(self):
        node = LeafNode("h1", "This is a Heading.")
        res = LeafNode.to_html(node)
        self.assertEqual(res, "<h1>This is a Heading.</h1>")