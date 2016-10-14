# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-14 10:27:39
# Last modified: 2016-10-14 14:36:03

"""
Example of the scoring result.
"""

from PYEVALB.scorer import Scorer

GOLD_PATH = './data/score/gold.txt'
TEST_PATH = './data/score/test.txt'
RESULT_PATH = './data/score/table.md'


def test_table():
        scorer = Scorer()
        scorer.evalb(GOLD_PATH, TEST_PATH, RESULT_PATH)
