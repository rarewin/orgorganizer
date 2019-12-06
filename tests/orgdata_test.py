import unittest
import pytest

from orgorganizer.node import parse_lines


class NodeTest(unittest.TestCase):
    """OrgのNodeクラスのテスト"""

    def test_headline_0level(self):
        root = parse_lines("* hoge")
        it = root.__iter__()

        node = next(it)
        self.assertEqual(node.level, 0)
        self.assertEqual(node._content, "hoge")
        self.assertEqual(node.__str__(), "* hoge")

        with self.assertRaises(StopIteration):
            next(it)

    def test_headline_1level(self):

        root = parse_lines("** fuga")
        it = root.__iter__()

        node = next(it)
        self.assertEqual(node.level, 1)
        self.assertEqual(node._content, "fuga")
        self.assertEqual(node.__str__(), "** fuga")

        with self.assertRaises(StopIteration):
            next(it)

    def test_headline_levels(self):

        root = parse_lines(
            """* hoge
** fuga"""
        )
        it = root.__iter__()

        node = next(it)
        self.assertEqual(node.level, 0)
        self.assertEqual(node._content, "hoge")
        self.assertEqual(node.__str__(), "* hoge")

        node = next(it)
        self.assertEqual(node.level, 1)
        self.assertEqual(node._content, "fuga")
        self.assertEqual(node.__str__(), "** fuga")

        with self.assertRaises(StopIteration):
            next(it)
