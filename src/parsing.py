from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        splitted = old_node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise Exception("Invalid markdown syntax: unclosed delimiter")
        for i in range(len(splitted)):
            if splitted[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splitted[i], text_type))
    return new_nodes
