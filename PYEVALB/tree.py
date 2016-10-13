# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-11 09:30:12
# Last modified: 2016-10-13 11:33:33

"""
Bracket Tree Class.

Loading the bracket trees.
"""

import collections

Span = collections.namedtuple('Span', ['s', 'e'])


class Node:
    """The definition of node class.

    Attributes:
        value: The value of this node.
        children: A list of children nodes.
    """
    def __init__(self, value):
        """Construct for a new Node class

        Args:
            value: str - The value of this node.
                        If current node is non-terminal,
                        then the value is constituent tag.
                        If current node is terminal, then the value is word.
            children: list(Node) - The children of this node.
        """
        self._value = value.strip()
        self._children = []
        self._span = Span(-1, -1)

    def isLeaf(self):
        return len(self.children) == 0

    def isPos(self):
        return (len(self.children) == 1 and
                self.children[0].isLeaf() is True)

    ########################################################
    # Property methods
    ########################################################
    @property
    def value(self):
        return self._value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def span(self):
        return self._span

    @span.setter
    def span(self, value):
        self._span = value

    ########################################################
    # Magic methods
    ########################################################
    def __repr__(self):
        s = 'Node:' + self.value
        p = '({a},{b})'.format(a=self.span.s,
                               b=self.span.e)
        return s+p

    def __eq__(self, node):
        return str(self) == str(node)

    def __hash__(self):
        return hash(str(self))


class Tree:
    """The structure of a tree.

    This class is simple a structure of a tree, does not
    contain any construct function about building a tree.
    """
    def __init__(self, root, deepcopy=False):
        """ Build a tree structure.

        Args:
            root: Node - The root node of current tree.
            deepcopy: Bool - If deepcopy is True, this class
                            will deep copy each children node
                            of given root to construct a new tree.
        """
        if deepcopy is True:
            self._root = self._deepcopy(root)
        else:
            self._root = root

        # Initialization
        values = self._get_nodes()
        self._terminal = values[0]
        self._non_terminal = values[1]
        self._non_terminal_labels = values[2]
        self._depth = values[3]

        self._pos_sentence = self._get_pos_sentence(self.root)
        self._sentence, self._poss = self._extract_sequence(self._pos_sentence)

        # Set the span for each node
        self._length = 0
        self._set_span(self.root)

    ########################################################
    # Property methods
    ########################################################
    @property
    def root(self):
        return self._root

    @property
    def terminals(self):
        """Return a list of terminal node.

        All the leaf nodes, which means it
        only includes word node.
        """
        return self._terminal

    @property
    def non_terminals(self):
        """Return a list of non-terminal node.

        All nodes except leaf node, which means it
        also includes the POS tag node.
        """
        return self._non_terminal

    @property
    def non_terminal_labels(self):
        """Return a list of label nodes.
        Includes all the nodes except pos tag and word node.
        """
        return self._non_terminal_labels

    @property
    def depth(self):
        """Return the depth of current tree.
        """
        return self._depth

    @property
    def sentence(self):
        """Return a list of words.

        For example:
        [上海 浦东 开发 与 法制 建设 同步]
        """
        return self._sentence

    @property
    def poss(self):
        """Return a list of pos tag

        For example:
        [NR NR NN CC NN NN VV]
        """
        return self._poss

    @property
    def pos_sentence(self):
        """Return a list of segments.

        For example:
        [上海_NN 浦东_NR 开发_NN 与_CC 法制_NN 建设_NN 同步_VV]
        """
        return self._pos_sentence

    ########################################################
    # Helping methods
    ########################################################
    def _deepcopy(self, root):
        """Make the deep copy of given node and its subtree.
        """
        new_root = Node(root.value)
        for child in root.children:
            new_root.children.append(self._deepcopy(child))
        return new_root

    def _to_bracket(self, node):
        """Transform tree structure into bracket strings.

        Args:
            node: node - The root of tree of subtree.

        Return:
            str - A bracket string.
        """
        # For pos tag label node
        if node.isPos():
            pos_tag = node.value
            word = node.children[0].value
            s = '('+' '.join([pos_tag, word])+')'
            return s
        # Constituent label node
        else:
            string = []
            for child in node.children:
                string.append(self._to_bracket(child))
            string = ' '.join(string)
            label = node.value
            string = '(' + label + ' ' + string + ')'
            return string

    def _get_pos_sentence(self, node):
        """Return the plain sentence
        Args:
            node: a tree node.
        Return:
            a list of word_pos in the sentence
            For example:
                ['上海_NR', '浦东_NR', '开发_NN', '与_CC',
                '法制_NN', '建设_NN', '同步_VV']
        """
        if node.isPos():
            leaf = node.children[0]
            return ['_'.join([leaf.value, node.value])]
        else:
            partial = []
            for child in node.children:
                partial += self._get_pos_sentence(child)
            return partial

    def _extract_sequence(self, pos_sentence):
        sentence = [item.split('_')[0] for item in pos_sentence]
        poss = [item.split('_')[-1] for item in pos_sentence]

        return sentence, poss

    def _get_nodes(self):
        """Collect the different type nodes

        Returns:
            terminal: list(node) - A list of terminal(leaf) node.
            non_terminal: list(node)- A list of non-terminal(leaf) node.
            depth: int - The depth of current tree.
        """
        nodes = []
        depth = self._depth(self.root, nodes)
        terminal = [node for node in nodes if node.isLeaf() is True]
        non_terminal = [node for node in nodes if node.isLeaf() is False]
        labels = [node for node in nodes
                  if node.isPos() is False and node.isLeaf() is False]
        return terminal, non_terminal, labels, depth

    def _depth(self, node, nodes):
        """Transfer the ndoes in DFS order.
        """
        nodes.append(node)
        depths = []
        if node.isLeaf() is False:
            for child in node.children:
                depths.append(self._depth(child, nodes))
            return max(depths) + 1
        else:
            return 0

    def _set_span(self, node):
        if node.isLeaf():
            node.span = Span(self._length, self._length+1)
            self._length += 1
            return
        else:
            for child in node.children:
                self._set_span(child)
            node.span = Span(
                    node.children[0].span.s,
                    node.children[-1].span.e)

    ########################################################
    # Magic methods
    ########################################################
    def __repr__(self):
        return self._to_bracket(self.root)
