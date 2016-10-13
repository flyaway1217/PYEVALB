# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-12 16:50:12
# Last modified: 2016-10-13 10:49:56

"""
Test for parser.py
"""

from nose.tools import assert_equals
from nose.tools import assert_not_equals
from nose.tools import assert_raises

from PYEVALB import parser
from PYEVALB.tree import Tree


BRACKETED_PATH = './data/BRACKETED.txt'
POSTAGGED_PATH = './data/POSTAGGED.txt'
SEGMENTED_PATH = './data/SEGMENTED.txt'


class TestParser:

    def setup(self):
        self._bank = []
        for line in self._read(BRACKETED_PATH):
            tree = parser.create_from_bracket_string(line)
            self._bank.append(tree)

    def _read(self, path):
        with open(path, encoding='utf8') as f:
            for line in f:
                yield line.strip()

    def test_create_from_bracket_string(self):
        for tree, line in zip(self._bank, self._read(BRACKETED_PATH)):
            answer = ''.join(line.split())
            value = ''.join(str(tree).split())
            assert_equals(answer, value)

        s = ('(IP (VP () (NP  (NN 一个) (NN ))))')
        tree = parser.create_from_bracket_string(s)
        answer = ''.join(s.split())
        value = ''.join(str(tree).split())
        assert_equals(answer, value)

    def test_poss_sentence(self):
        postags = self._read(POSTAGGED_PATH)
        for tree, poss in zip(self._bank, postags):
            value = tree.pos_sentence
            value = ' '.join(value)
            assert_equals(poss, value)

    def test_sentence(self):
        sent = self._read(SEGMENTED_PATH)
        for tree, poss in zip(self._bank, sent):
            value = tree.sentence
            value = ' '.join(value)
            assert_equals(poss, value)

    def test_poss(self):
        postags = self._read(POSTAGGED_PATH)
        for tree, poss in zip(self._bank, postags):
            poss = [v.split('_')[-1] for v in poss.split()]
            poss = ' '.join(poss)
            value = tree.poss
            value = ' '.join(value)
            assert_equals(poss, value)

    def test_nodes(self):
        s = ('(IP (VP 这是) (NP  (NN 一个) (NN 测试)))')
        tree = parser.create_from_bracket_string(s)

        ans = 'Node:这是(0,1) Node:一个(1,2) Node:测试(2,3)'
        values = tree.terminal
        values = [str(v) for v in values]
        values = ' '.join(values)
        assert_equals(values, ans)

        ans = ('Node:IP(0,3) Node:VP(0,1) Node:NP(1,3) '
               'Node:NN(1,2) Node:NN(2,3)')
        values = tree.non_terminal
        values = [str(v) for v in values]
        values = ' '.join(values)
        assert_equals(values, ans)

        ans = 'Node:IP(0,3) Node:NP(1,3)'
        values = tree.label
        values = [str(v) for v in values]
        values = ' '.join(values)
        assert_equals(values, ans)

    def test_depth(self):
        depths = [4, 2, 11]
        for ans, tree in zip(depths, self._bank):
            assert_equals(ans, tree.depth)

    def test_deep(self):
        s = ('(IP (VP 这是) (NP  (NN 一个) (NN 测试)))')
        tree1 = parser.create_from_bracket_string(s)
        tree2 = Tree(tree1.root, deepcopy=True)
        tree3 = Tree(tree1.root)
        assert_not_equals(id(tree1.root), id(tree2.root))
        assert_equals(id(tree1.root), id(tree3.root))

    def test_parsing_error(self):
        assert_raises(parser.ParsingError,
                      parser.create_from_bracket_string,
                      ' ')
