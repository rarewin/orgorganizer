import unittest

from orgorganizer.node import parse_lines


class NodeTest(unittest.TestCase):
    """OrgのNodeクラスのテスト"""

    def test_headline_1level(self):
        document = parse_lines("* hoge  :a:b:")
        it = document.__iter__()

        node = next(it)
        self.assertEqual(node.level, 1)
        self.assertEqual(node._parsed, False)
        self.assertEqual(node.title, "hoge")
        self.assertEqual(node._parsed, True)
        self.assertEqual(node.tags, ["a", "b"])
        self.assertEqual(node.status, None)
        self.assertEqual(
            node.__str__(),
            "* hoge                                                                  :a:b:",
        )

        with self.assertRaises(StopIteration):
            next(it)

    def test_headline_2level(self):

        document = parse_lines("** fuga")
        it = document.__iter__()

        node = next(it)
        self.assertEqual(node.level, 2)
        self.assertEqual(node.title, "fuga")
        self.assertEqual(node._parsed, True)
        self.assertEqual(node.__str__(), "** fuga")

        with self.assertRaises(StopIteration):
            next(it)

    def test_headline_levels(self):
        """複数レベルのHEADLINEのテスト"""

        document = parse_lines(
            """* hoge
** fuga"""
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
        self.assertEqual(node2.__str__(), "** fuga")
        self.assertEqual(node2._parsed, True)

        self.assertEqual(node2.parent, node1)

        with self.assertRaises(StopIteration):
            next(it)
