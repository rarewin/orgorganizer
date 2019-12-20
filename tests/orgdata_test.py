# -*- coding: utf-8 -*-
import unittest

from orgorganizer.node import parse_lines


class NodeTest(unittest.TestCase):
    """OrgのNodeクラスのテスト"""

    def test_headline_1level(self):
        """レベル1のHEADLINEテスト"""

        document = parse_lines("*  TODO [#A] hoge  :a:b:")
        it = document.__iter__()

        node = next(it)
        self.assertEqual(node.level, 1)
        self.assertEqual(node._parsed, False)
        self.assertEqual(node.keyword, "TODO")
        self.assertEqual(node.title, "hoge")
        self.assertEqual(node._parsed, True)
        self.assertEqual(node.tags, ["a", "b"])
        self.assertEqual(node.priority, "A")
        self.assertEqual(
            node.__str__(), "* TODO [#A] hoge" + " " * 56 + ":a:b:",
        )

        with self.assertRaises(StopIteration):
            next(it)

    def test_headline_2level(self):
        """レベル2のHEADLINEテスト"""

        document = parse_lines("** DONE fuga")
        it = document.__iter__()

        node = next(it)
        self.assertEqual(node.level, 2)
        self.assertEqual(node.title, "fuga")
        self.assertEqual(node._parsed, True)
        self.assertEqual(node.keyword, "DONE")
        self.assertEqual(node.__str__(), "** DONE fuga")

        with self.assertRaises(StopIteration):
            next(it)

    def test_headline_levels(self):
        """複数レベルのHEADLINEのテスト"""

        document = parse_lines(
            """* hoge
** TODO fuga
** DONE moge
*** mogemoge
*** mogemoge
"""
        )
        it = document.__iter__()

        node1 = next(it)
        self.assertEqual(node1.level, 1)
        self.assertEqual(node1.title, "hoge")
        self.assertEqual(node1._parsed, True)
        self.assertEqual(node1.__str__(), "* hoge")

        node2 = next(it)
        self.assertEqual(node2.level, 2)
        self.assertEqual(node2.title, "fuga")
        self.assertEqual(node2._parsed, True)
        self.assertEqual(node2.keyword, "TODO")
        self.assertEqual(node2.__str__(), "** TODO fuga")

        node3 = next(it)
        self.assertEqual(node3.level, 2)
        self.assertEqual(node3.title, "moge")

        self.assertIn(node2, node1.children)
        self.assertIn(node3, node1.children)
        self.assertEqual(node3._parsed, True)
        self.assertEqual(node3.keyword, "DONE")
        self.assertEqual(node3.__str__(), "** DONE moge")

        self.assertEqual(node2.parent, node1)
        self.assertEqual(node3.parent, node1)

        node4 = next(it)
        self.assertEqual(node4.level, 3)
        self.assertEqual(node4.title, "mogemoge")
        self.assertEqual(node4.__str__(), "*** mogemoge")
        self.assertEqual(node4._parsed, True)

        self.assertEqual(node4.parent, node3)
        self.assertIn(node4, node3.children)

        node5 = next(it)
        self.assertEqual(node5.level, 3)
        self.assertEqual(node5.title, "mogemoge")
        self.assertEqual(node5.__str__(), "*** mogemoge")
        self.assertEqual(node5._parsed, True)

        self.assertEqual(node5.parent, node3)
        self.assertNotEqual(node4, node5)

        with self.assertRaises(StopIteration):
            next(it)

        self.assertEqual(
            document.__str__(),
            """* hoge
** TODO fuga
** DONE moge
*** mogemoge
*** mogemoge""",
        )
