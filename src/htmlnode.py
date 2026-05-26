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
        raise NotImplementedError()

    def props_to_html(self) -> str:
        string = ""
        if not self.props:
            return string
        for key, value in self.props:
            string += f' {key}="{value}"'
        return string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, htmlnode):
        return (
            self.tag == htmlnode.tag
            and self.value == htmlnode.value
            and self.children == htmlnode.children
            and self.props == htmlnode.props
        )
