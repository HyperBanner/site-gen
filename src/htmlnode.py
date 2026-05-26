class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str | None:
        raise NotImplementedError("Only child classes implement to_html()")

    def props_to_html(self) -> str:
        string = ""
        if not self.props:
            return string
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, html_node):
        return (
            self.tag == html_node.tag
            and self.value == html_node.value
            and self.children == html_node.children
            and self.props == html_node.props
        )


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, leaf_node):
        return (
            self.tag == leaf_node.tag
            and self.value == leaf_node.value
            and self.props == leaf_node.props
        )


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        string = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            string += node.to_html()
        string += f"</{self.tag}>"
        return string

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
