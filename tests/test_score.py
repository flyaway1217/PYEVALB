# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-13 13:58:26
# Last modified: 2016-10-14 14:12:37

"""
Test class for score.py
"""
from nose.tools import assert_equals

from PYEVALB.scorer import Result
from PYEVALB.scorer import Scorer
from PYEVALB import summary


assert_equals.__self__.maxDiff = None
# from nose.tools import assert_not_equals
# from nose.tools import assert_raises

RESULT_PATH = './data/score/result.txt'
GOLD_PATH = './data/score/gold.txt'
TEST_PATH = './data/score/test.txt'
SUMMARY_PATH = './data/score/summary.txt'

ERROR_RESULT_PATH = './data/score/result_exception.txt'
ERROR_GOLD_PATH = './data/score/gold_exception.txt'
ERROR_TEST_PATH = './data/score/test_exception.txt'


class TestScorer:

    def _read(self, path):
        reval = []
        with open(path, encoding='utf8') as f:
            for line in f:
                s = line.split()
                result = Result()

                result.ID = int(s[0])-1
                result.length = int(s[1])
                result.state = int(s[2])
                result.recall = float(s[3]) / 100
                result.prec = float(s[4]) / 100
                result.matched_brackets = int(s[5])
                result.gold_brackets = int(s[6])
                result.test_brackets = int(s[7])
                result.cross_brackets = int(s[8])
                result.words = int(s[9])
                result.correct_tags = int(s[10])
                result.tag_accracy = float(s[11]) / 100
                reval.append(result)

        return reval

    def setup(self):
        self._true_results = self._read(RESULT_PATH)
        self.maxDiff = None

    def test_score_trees(self):
        scorer = Scorer()
        with open(GOLD_PATH, encoding='utf8') as gold:
            with open(TEST_PATH, encoding='utf8') as test:
                results = scorer.score_corpus(gold, test)
        for ans, value in zip(self._true_results, results):
            assert_equals(str(ans), str(value))

    def test_summary(self):
        scorer = Scorer()
        with open(GOLD_PATH, encoding='utf8') as gold:
            with open(TEST_PATH, encoding='utf8') as test:
                results = scorer.score_corpus(gold, test)

        value = summary.summary(results)
        value = summary._summary2string(value)

        ans = []
        with open(SUMMARY_PATH, encoding='utf8') as f:
                ans = [float(line.strip().split('=')[-1])
                       for line in f]
        print(ans)
        ans = summary.Summary(*ans)
        ans = summary._summary2string(ans)

        assert_equals(ans, value)

    def test_exception(self):
        scorer = Scorer()
        ans = Result()
        ans.state = 2
        with open(ERROR_GOLD_PATH, encoding='utf8') as gold:
            with open(ERROR_TEST_PATH, encoding='utf8') as test:
                results = scorer.score_corpus(gold, test)
        for i, value in enumerate(results):
            ans.ID = i
            assert_equals(str(ans), str(value))
