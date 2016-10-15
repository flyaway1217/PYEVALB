# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-12 09:29:56
# Last modified: 2016-10-15 17:16:55

"""
Create tree structures from string.

1. Penn Tree Bank:
    The format should be:
    (IP (NP (NP (NR 上海) (NR 浦东)) (NP (NN 开发) (CC 与)
    (NN 法制) (NN 建设))) (VP (VV 同步)))

"""

import collections

from .tree import Node
from .tree import Tree


class ParsingError(Exception):
    """Exception class of parser.
    """
    def __init__(self, errormessage):
        self.errormessage = 'Parsing Error:'
        self.errormessage += errormessage


def create_from_bracket_string(line):
    """Create tree structure from a given string.
    """
    stack = collections.deque()
    if len(line.strip()) == 0:
        raise ParsingError('Empty String !')

    # Clean the input string
    sentence = line.replace('(', ' ( ')
    sentence = sentence.replace(')', ' ) ')

    sentence = sentence.split()
    for char in sentence:
        if char != ')':
            stack.append(char)
        else:
            if type(stack[-1]) == str and stack[-2] == '(':
                stack.append(char)
            else:
                _stack_operation(stack)
    root = stack.pop()
    return Tree(root)


def _stack_operation(stack):
    """The standard operation on the stack.

    Pop items and insert a new item.

    Args:
        stack
    """
    if len(stack) == 0:
        return
    children = []

    # Special case for '(' or ')' as the content of sentence.
    value = stack.pop()
    if type(value) == str:
        value = Node(value)
    children.append(value)

    while len(stack) != 0 and stack[-1] != '(':
        value = stack.pop()
        if type(value) == str:
            value = Node(value)
        children.append(value)
    parent = children.pop()
    children.reverse()
    parent.children = children
    stack.pop()
    stack.append(parent)
