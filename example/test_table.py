# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-14 10:27:39
# Last modified: 2016-10-14 13:50:55

"""
Example of the scoring result.
"""

from PYEVALB.scorer import Scorer
from PYEVALB import summary

GOLD_PATH = './data/gold.txt'
TEST_PATH = './data/test.txt'
RESULT_PATH = './table.md'


def test_table():
    with open(GOLD_PATH, encoding='utf8') as gold_f:
        with open(TEST_PATH, encoding='utf8') as test_f:
            scorer = Scorer()
            results = scorer.score_corpus(gold_f, test_f)
            s = summary.summary(results)
            summary.write_table(RESULT_PATH, results, s)
