# -*- coding: utf-8 -*-
import re

ORG_WIDTH = 77  # @todo investigation

RE_HEADLINE = re.compile(r"^(\*+)\s+(.*)")
RE_HEADLINE_TAGS = re.compile(r"\s+:([\w%#@:]+):$")


class OrgDocument:
    """org文章ルート"""

    __slots__ = ("_nodes", "_content", "_level", "_keywords")

    def __init__(self):
        self._nodes = []
        self._content = ""
        self._keywords = ["TODO", "DONE"]

    def __iter__(self):

        for node in self._nodes:
            yield from iter(node)

    def __str__(self):

        lines = []

        for n in self:
            lines.append(n.__str__())

        return "\n".join(lines)

    def append_child(self, node):
        self._nodes.append(node)

    @property
    def level(self):
        return self._level

    @property
    def keywords(self):
        return self._keywords


class OrgHeadlineNode:
    """
    HEADLINE

    STARS KEYWORD PRIORITY TITLE TAGS
    """

    __slots__ = (
        "_level",
        "_children",
        "_keyword",
        "_priority",
        "_title",
        "_tags",
        "_parsed",
        "_content",
        "_parent",
        "_root",
    )

    def __init__(self, level, line, root):
        self._parsed = False
        self._children = []
        self._parent = None

        self._keyword = ""
        self._priority = ""
        self._title = ""
        self._tags = []

        self._level = level
        self._content = line

        self._root = root

    def __str__(self):

        self.parse()

        stars = "*" * self._level
        keyword = f"{self._keyword} " if self._keyword else ""
        priority = f"[#{self._priority}] " if self.priority else ""
        ret = f"{stars} {keyword}{priority}{self._title}"

        # TAGまでのスペース調整
        if self._tags:
            tags = ":".join(self._tags)
            tag_str = f":{tags}:"
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
    def title(self):
        self.parse()
        return self._title

    @property
    def priority(self):
        self.parse()
        return self._priority

    @property
    def keyword(self):
        self.parse()
        return self._keyword

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

        # KEYWORDをみつける
        t = self._content.strip().split(" ", maxsplit=1)

        if len(t) == 2 and t[0] in self._root.keywords:
            self._keyword = t[0]
            self._content = t[1].strip()

        t = self._content.split(" ", maxsplit=1)

        if (
            len(t) == 2
            and t[0].startswith("[#")
            and t[0].find("]") == 3
            and len(t[0]) == 4
        ):
            self._priority = t[0][2]
            self._content = t[1].strip()

        m = RE_HEADLINE_TAGS.search(self._content)

        if m:
            self._content = self._content[: -len(m.group(0))].strip()
            self._tags = m.group(1).split(":")

        self._title = self._content
        self._content = None

    def set_parent(self, parent):
        self._parent = parent

    def append_child(self, child):
        self._children.append(child)


class OrgProperty:
    def __init__(self):
        pass


def find_parent(nodes, child):
    """nodes中のchildの親を探し, nodesを更新する"""

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
            node = OrgHeadlineNode(level, content, root)
            parent = find_parent(nodes, node)
            node.set_parent(parent)
            parent.append_child(node)

    return root
