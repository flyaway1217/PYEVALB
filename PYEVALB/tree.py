# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-11 09:30:12
# Last modified: 2016-10-13 09:00:29

"""
Bracket Tree Class.

Loading the bracket trees.
"""

# import collections

# Span = collections.namedtuple('Span', ['s', 'e'])


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
        # self._span = Span(-1, -1)

    def isLeaf(self):
        return len(self._children) == 0

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

    # @property
    # def span(self):
    #     return self._span

    # @span.setter
    # def span(self, value):
    #     self._span = value

    ########################################################
    # Helping methods
    ########################################################
    def __repr__(self):
        s = 'Node:' + self.value
        return s


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
        self._terminal, self._non_terminal, self._depth = self._get_nodes()
        self._pos_sentence = self._get_pos_sentence(self.root)
        self._sentence, self._poss = self._extract_sequence(self._pos_sentence)

    ########################################################
    # Property methods
    ########################################################
    @property
    def root(self):
        return self._root

    @property
    def terminal(self):
        return self._terminal

    @property
    def non_terminal(self):
        return self._non_terminal

    @property
    def depth(self):
        return self._depth

    @property
    def sentence(self):
        return self._sentence

    @property
    def poss(self):
        return self._poss

    @property
    def pos_sentence(self):
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
        if (len(node.children) == 1 and
                node.children[0].isLeaf() is True):
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
        if len(node.children) == 1 and node.children[0].isLeaf():
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
        return terminal, non_terminal, depth

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

    def __repr__(self):
        return self._to_bracket(self.root)
