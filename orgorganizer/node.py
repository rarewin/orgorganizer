# -*- coding: utf-8 -*-
import re

ORG_WIDTH = 77  # @todo investigation

RE_HEADLINE = re.compile(r"^(\*+)\s+(.*)")
RE_HEADLINE_TAGS = re.compile(r":([\w\s:]+):$")


class OrgDocument:
    """org文章ルート"""

    __slots__ = ("_nodes", "_content", "_level")

    def __init__(self):
        self._nodes = []
        self._content = ""

    def __iter__(self):

        for node in self._nodes:
            yield from iter(node)

    def append_child(self, node):
        self._nodes.append(node)

    @property
    def level(self):
        return self._level


class OrgHeadlineNode:
    """
    HEADLINE

    STARS KEYWORD PRIORITY TITLE TAGS
    """

    __slots__ = (
        "_level",
        "_children",
        "_title",
        "_status",
        "_tags",
        "_parsed",
        "_content",
        "_parent",
    )

    def __init__(self, level, line):
        self._children = []
        self._parsed = False
        self._tags = []
        self._status = None
        self._title = ""
        self._parent = None

        self._level = level
        self._content = line

    def __str__(self):

        if not self._parsed:
            self.parse()

        ret = "{} {}".format("*" * self._level, self._title)

        if self._tags:
            tag_str = ":{}:".format(":".join(self._tags))
            ret += " " * (ORG_WIDTH - len(ret) - len(tag_str)) + tag_str

        return ret

    def __iter__(self):

        yield self
        for child in self._children:
            yield from iter(child)

    @property
    def level(self):
        return self._level

    @property
    def tags(self):
        self.parse()
        return self._tags

    @property
    def status(self):
        self.parse()
        return self._status

    @property
    def title(self):
        self.parse()
        return self._title

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    def parse(self, force=False):
        """パースを実行する. 実施済みの場合は何もしない"""

        if self._parsed or force:
            return

        self._parsed = True

        m = RE_HEADLINE_TAGS.search(self._content)

        if m:
            self._content = self._content[: -len(m.group(0))].strip()
            self._tags = m.group(1).split(":")

        self._title = self._content

    def set_parent(self, parent):
        self._parent = parent

    def append_child(self, child):
        self._children.append(child)


class OrgProperty:
    def __init__(self):
        pass


def find_parent(nodes, child):

    # 親の階層は, 子の1個上か現在のnodesの長さ - 1
    parent_level = min(child.level - 1, len(nodes) - 1)

    while len(nodes) > parent_level + 1:
        nodes.pop()

    while 0 < parent_level:
        if nodes[parent_level]:
            break
        parent_level -= 1

    while len(nodes) < child.level - 1:
        nodes.append(None)

    nodes.append(child)

    return nodes[parent_level]


def parse_lines(data):

    root = OrgDocument()

    nodes = [
        root,
    ]

    for line in data.split("\n"):

        m = RE_HEADLINE.search(line)

        if m:
            level = len(m.group(1))
            content = m.group(2)
            node = OrgHeadlineNode(level, content)
            parent = find_parent(nodes, node)
            node.set_parent(parent)
            parent.append_child(node)

    return root
