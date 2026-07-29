from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(markdown: str) -> BlockType:
    if re.match(r"^(#{1,6} )", markdown):
        return BlockType.HEADING
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n") #splits text into lines
    if all((line != "" and line[0] == ">") for line in lines):
        return BlockType.QUOTE
    if all(line[0:2] == "- " for line in lines):
        return BlockType.UNORDERED
    if all((re.match(r"^(\d+\. )", line)) for line in lines):
        ordered = True
        for index, line in enumerate(lines):
            expected_number = index + 1
            actual_number = int(line.split(".", 1)[0])
            if actual_number == expected_number:
                continue
            else:
                ordered = False
                break
        if ordered:
            return BlockType.ORDERED
        else:
            return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH




