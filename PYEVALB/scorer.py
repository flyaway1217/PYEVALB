# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-13 10:02:18
# Last modified: 2016-10-15 17:19:14

"""
PYEVALB: Evalb in Python version.
"""

from .parser import ParsingError
from .summary import Result
from . import parser
from . import summary

############################################################
# Exceptions
############################################################


class ScoreException(Exception):
    def get_details(self):
        return self.details()


class LengthUnmatch(ScoreException):
    def __init__(self, len_gold_sentence, len_test_sentence):
        self.len_gold_sentence = len_gold_sentence
        self.len_test_sentence = len_test_sentence

    def details(self):
        a = "Length Unmatched !"
        b = "gold sentence:" + str(self.len_gold_sentence)
        c = "test sentence:" + str(self.len_test_sentence)
        s = '\n'.join([a, b, c])
        s += '\n'
        s += '-'*30
        return s


class WordsUnmatch(ScoreException):
    def __init__(self, gold_sentence, test_sentence):
        self.gold_sentence = gold_sentence
        self.test_sentence = test_sentence

    def details(self):
        a = "Words Unmatched !"
        b = "gold sentence:" + str(self.gold_sentence)
        c = "test sentence:" + str(self.test_sentence)
        s = '\n'.join([a, b, c])
        s += '\n'
        s += '-'*30
        return s


class Scorer:
    """The Scorer class.

    This class is a manager of scoring, it can socre tree
    corpus in a specific configuration.
    Every instance corresponding to a configuration.
    """
    def __init__(self):
        pass

    def _cal_spans(self, gold_nodes, test_nodes):
        """Calculate the common span and across span

        Args:
            gold_spans: a list of nodes in gold tree
            test_spans: a list of nodes in test tree

        Returns:
            a tuple span_result:
                span_result[0]: the number of common spans
                span_result[1]: the number of crossing spans
        """
        common = set(gold_nodes) & set(test_nodes)
        unmatched_spans = [node.span for node in test_nodes
                           if node not in common]
        gold_spans = [node.span for node in gold_nodes]

        cross_counter = 0
        # the crossing spans
        for u in unmatched_spans:
            for g in gold_spans:
                if (u.s < g.s and u.e > g.s and u.e < g.e):
                    cross_counter += 1
                    break
                elif (u.s > g.s and u.s < g.e and u.e > g.e):
                    cross_counter += 1
                    break

        return len(common), cross_counter

    def score_trees(self, gold_tree, test_tree):
        '''Score the two trees

        Args:
            gold_tree: the gold tree
            test_tres: the test tree

        Returns:
            An instance of Result
        '''
        # Preparing
        gold_label_nodes = gold_tree.non_terminal_labels
        test_label_nodes = test_tree.non_terminal_labels

        gold_poss = gold_tree.poss
        test_poss = test_tree.poss

        gold_sentence = gold_tree.sentence
        test_sentence = test_tree.sentence

        # Check
        if len(gold_sentence) != len(test_sentence):
            raise LengthUnmatch(len(gold_sentence), len(test_sentence))

        if gold_sentence != test_sentence:
            raise WordsUnmatch(gold_sentence, test_sentence)

        # Statistics
        result = Result()
        common_numeber, cross_number = self._cal_spans(
                gold_label_nodes, test_label_nodes)
        correct_poss_num = sum([gold == test for gold, test
                               in zip(gold_poss, test_poss)])

        result.length = len(gold_sentence)
        result.state = 0
        result.recall = common_numeber / len(gold_label_nodes)
        result.prec = common_numeber / len(test_label_nodes)
        result.matched_brackets = common_numeber
        result.gold_brackets = len(gold_label_nodes)
        result.test_brackets = len(test_label_nodes)
        result.cross_brackets = cross_number
        result.words = len(gold_sentence)
        result.correct_tags = correct_poss_num
        result.tag_accracy = correct_poss_num / len(gold_poss)

        return result

    def score_corpus(self, f_gold, f_test):
        """
        score the treebanks

        Args:
            f_gold: a iterator of gold treebank
            f_test: a iterator of test treebank

        Returns:
            a list of instances of Result
        """
        results = []
        for ID, (gold, test) in enumerate(zip(f_gold, f_test)):
            try:
                gold_tree = parser.create_from_bracket_string(gold)
                test_tree = parser.create_from_bracket_string(test)
                current_result = self.score_trees(gold_tree, test_tree)
            except (WordsUnmatch, LengthUnmatch) as e:
                current_result = Result()
                current_result.state = 2
                print(e.details())
            except ParsingError as e:
                print(e.errormessage)
            finally:
                current_result.ID = ID
                results.append(current_result)
        return results

    def evalb(self, gold_path, test_path, result_path):
        with open(gold_path, encoding='utf8') as gold_f:
            with open(test_path, encoding='utf8') as test_f:
                results = self.score_corpus(gold_f, test_f)
                s = summary.summary(results)
                summary.write_table(result_path, results, s)
