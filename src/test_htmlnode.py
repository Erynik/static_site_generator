import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "www.google.co.uk", "target": "_blank"})
        res = HTMLNode.props_to_html(node)
        self.assertEqual(res, 'href="www.google.co.uk" target="_blank"')