import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
    
    def test_parent_node_no_child(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
        
    def test_parent_multiple_siblings(self):
        child_nodes = [
            LeafNode("span", "child 1"),
            LeafNode("div", "child 2"),
            LeafNode("b", "bold child 3"),
            LeafNode("i", "italic child 4"),
            LeafNode(None, "normal child 5")
        ]
        parent_node = ParentNode("p", child_nodes)
        self.assertEqual(parent_node.to_html(), "<p><span>child 1</span><div>child 2</div><b>bold child 3</b><i>italic child 4</i>normal child 5</p>")

    def test_parent_empty_children(self):
        child_node = []
        parent_node = ParentNode("p", child_node)
        self.assertEqual(parent_node.to_html(), "<p></p>")

    def test_parent_no_tag(self):
        child_node = [LeafNode("span", "child 1")]
        with self.assertRaises(ValueError):
            ParentNode(None, child_node).to_html()

    def test_parent_nested_siblings(self):
        child_nodes = [
            LeafNode("span", "child 1"),
            ParentNode("p", [
                LeafNode("i", "nested italic child"), 
                LeafNode("b", "nested bold child")
                ]),
            LeafNode("div", "child 2")

        ]
        parent_node = ParentNode("h1", child_nodes)
        self.assertEqual(parent_node.to_html(),"<h1><span>child 1</span><p><i>nested italic child</i><b>nested bold child</b></p><div>child 2</div></h1>")


    def test_parent_deep_nest(self):
        child_nodes = [ParentNode("a", [ParentNode("b", [ParentNode("c", [LeafNode("d", "child")])])])]
        parent_node = ParentNode("h1", child_nodes)
        self.assertEqual(parent_node.to_html(), "<h1><a><b><c><d>child</d></c></b></a></h1>")


if __name__ == "__main__":
    unittest.main()