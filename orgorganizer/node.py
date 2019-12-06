import re


class OrgBaseNode:
    def __init__(self):
        pass


class OrgRootNode:

    __slots__ = ("_nodes",)

    def __init__(self):
        self._nodes = []

    def __iter__(self):
        for n in self._nodes:
            yield n

    def add_node(self, node):
        self._nodes.append(node)


class OrgHeadlineNode(OrgBaseNode):

    __slots__ = ("_level", "_parsed", "_title", "_children")

    RE_HEADLINE = re.compile(r"^(\*+)\s+(\w+)")

    def __init__(self, line):

        m = self.RE_HEADLINE.search(line)

        self._level = len(m.group(1)) - 1
        self._content = m.group(2)
        self._parsed = False
        self._children = []

    def __str__(self):
        return "{} {}".format("*" * (self._level + 1), self._content)

    @property
    def level(self):
        return self._level


def parse_lines(data):

    root = OrgRootNode()

    for line in data.split("\n"):

        if line[0] == "*":
            node = OrgHeadlineNode(line)
            root.add_node(node)

    return root
