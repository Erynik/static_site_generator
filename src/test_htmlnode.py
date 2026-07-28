import unittest
from htmlnode import HTMLNode

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
