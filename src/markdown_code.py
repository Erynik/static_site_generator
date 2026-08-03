import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from block import block_to_block_type, BlockType
from textnode import text_node_to_html_node


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
            new_nodes.append(node)
            continue
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


def text_to_textnodes(text):
    bold_split = split_nodes_delimiter([TextNode(text, TextType.TEXT)],"**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)
    final_nodes = link_split
    return final_nodes


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    final_blocks = []
    for block in new_blocks:
        if block == "":
            continue
        stripped_block = block.strip()
        final_blocks.append(stripped_block)
    return final_blocks
            
def text_to_children(text):
    #takes in string of text, returns list of HTMLNodes for the inline markdown
    #uses text_to_textnodes, followed by textnode_to_htmlnode
    new_text_nodes = text_to_textnodes(text)
    new_children = []
    for node in new_text_nodes:
        child = text_node_to_html_node(node)
        new_children.append(child)
    return new_children

def markdown_to_html_node(markdown):
    #split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    #loop over each block
    new_nodes = []
    for block in blocks:
        #determine block type
        block_type = block_to_block_type(block)
        #create HTMLNode based on blocktype
        match block_type:
            case BlockType.PARAGRAPH:
                paragraph = block.replace("\n", " ")
                para_node = ParentNode(tag = 'p', children = text_to_children(paragraph))
                new_nodes.append(para_node)
            case BlockType.CODE:
                code = TextNode(block.strip("```").lstrip("\n"), TextType.TEXT) 
                text_node = text_node_to_html_node(code)
                code_node = ParentNode(tag = 'code', children = [text_node])
                pre_code_node = ParentNode(tag = 'pre', children = [code_node])
                new_nodes.append(pre_code_node)      
            case BlockType.QUOTE:
                quote_lines = block.split("\n")
                quote_lines_trimmed = []
                for line in quote_lines:
                    new_line = line.strip("> ")
                    quote_lines_trimmed.append(new_line)
                quote_text = " ".join(quote_lines_trimmed)
                quote_node = ParentNode(tag = 'blockquote', children = text_to_children(quote_text))
                new_nodes.append(quote_node)
            case BlockType.UNORDERED:
                list_lines = block.split("\n")
                line_nodes = []
                for line in list_lines:
                    trimmed_line = line[2:]
                    line_node = ParentNode(tag="li", children=text_to_children(trimmed_line))
                    line_nodes.append(line_node)
                list_node = ParentNode(tag="ul", children=line_nodes)
                new_nodes.append(list_node)
            case BlockType.ORDERED:
                list_lines = block.split("\n")
                line_nodes = []
                for line in list_lines:
                    index_dot = line.find('.')
                    trimmed_line = line[index_dot+2:]
                    line_node = ParentNode(tag="li", children=text_to_children(trimmed_line))
                    line_nodes.append(line_node)
                list_node = ParentNode(tag="ol", children=line_nodes)
                new_nodes.append(list_node)         

            case BlockType.HEADING:
                heading_text = block.strip("# ")
                heading_count: int = block[:7].count('#')
                tag_constructed = f"h{heading_count}"
                heading_node = ParentNode(tag=tag_constructed, children=text_to_children(heading_text))
                new_nodes.append(heading_node)


    #outside of block loop. adds all above nodes to parent HTMLNode for the page.
    parent_node = ParentNode(tag = 'div', children = new_nodes)
    return parent_node