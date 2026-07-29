import re
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


def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        text_to_split = node.text
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = text_to_split.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text_to_split = sections[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        text_to_split = node.text
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = text_to_split.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text_to_split = sections[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes
