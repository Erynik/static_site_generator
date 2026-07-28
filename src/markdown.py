from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
    ) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            raise Exception("Invalid Markdown Syntax")
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) %2 == 0:
                raise Exception("Invalid Markdown Syntax")
            for index, value in enumerate(split_node):
                if value == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(value, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(value, text_type))
    return new_nodes


