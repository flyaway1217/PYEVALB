# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-13 10:02:18
# Last modified: 2016-10-13 16:06:10

"""
PYEVALB: Evalb in Python version.
"""

from PYEVALB.parser import ParsingError
from PYEVALB import parser

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

############################################################
# Result class
############################################################


class Result:
    """The class of result data

    Attributes:
        _staticis: is a dict of statistics:
            ID: the ID of current sentence
            length: the length of the sentence
            state:  the state of the current compare  0:OK,1:skip,2:error
            recall: the recall of the two trees
                    recall = matched bracketing / brackets of gold data
            prec:   the precision of the two trees
                    prec = matched bracketing / brackets of test data
            matched_brackets: the number of matched brackets
            gold_brackets: the number of gold brackets
            test_brackets: the number of test brackets
            cross_brackets: the number of cross brackets
            words: the number of unique words
            correct_tags: the number of correct tags
            tag_accracy: the accruacy of tags
    """
    STATISTICS_TABLE = [
            'ID', 'length', 'state', 'recall', 'prec', 'matched_brackets',
            'gold_brackets', 'test_brackets',
            'cross_brackets', 'words', 'correct_tags', 'tag_accracy'
            ]
    SUMMARY_TABLE = [
            'Number of sentence', 'Number of Error sentence',
            'Number of Skip  sentence', 'Number of Valid sentence',
            'Bracketing Recall', 'Bracketing Precision',
            'Bracketing FMeasure', 'Complete match',
            'Average crossing', 'No crossing', 'Tagging accuracy'
            ]

    def __init__(self):
        self._staticis = dict()

        # Initialize the dict
        for name in Result.STATISTICS_TABLE:
            self._staticis[name] = 0

    def __repr__(self):
        sout = ''
        for name in Result.STATISTICS_TABLE:
            value = self._staticis[name]
            s = name + ":"
            if type(value) == int:
                ss = '{0: >3d}'.format(value)
            else:
                ss = '{0: >5.2f}'.format(value*100)
            sout += (s+ss+' ')
        return sout

    def __getattr__(self, name):
        if name == "_staticis":
            return self.__dict__[name]
        elif name in Result.STATISTICS_TABLE:
            return self._staticis.get(name, 0)
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if name == "_staticis":
            self.__dict__[name] = value
        elif name in Result.STATISTICS_TABLE:
            self._staticis[name] = value
        else:
            print(name)
            raise AttributeError

    def tostring(self):
        sout = ''
        for name in Result.STATISTICS_TABLE:
            value = self._staticis[name]
            if type(value) == int:
                s = '{0: >7d}'.format(value)
            else:
                s = '{0: >9.2f}'.format(value*100)
            sout += s
        return sout


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

    # def result2string(self, results):
    #     string = ''
    #     sout = []
    #     for item in results:
    #         sout.append(item.tostring())
    #     string += '\n'.join(sout)
    #     return string

    # def summary2string(self, summary):
    #     string = []
    #     for name, value in zip(Result.SUMMARY_TABLE, summary):
    #         if type(value) == int:
    #             string.append(name+":\t"+'{0:5d}'.format(value))
    #         else:
    #             string.append(name+":\t"+'{0:.4f}'.format(value))
    #     return '\n'.join(string)

    # def summary(self, results):
    #     """Calculate the summary of resutls

    #     Args:
    #         results: a list of result of each sentence

    #     Returns:
    #         a list contains all the summary data.
    #         The data in the list is ordered by Result.SUMMARY_TABLE.
    #     """
    #     summay_list = [0] * len(Result.SUMMARY_TABLE)

    #     # Number of sentence
    #     summay_list[0] = len(results)

    #     # Number of Error sentence
    #     # 2:Error
    #     summay_list[1] = len([item for item in results if item.state == 2])

    #     # Number of Skip sentence
    #     # 1:skip
    #     summay_list[2] = len([item for item in results if item.state == 1])

    #     correct_results = [item for item in results if item.state == 0]

    #     # Number of Skip sentence
    #     sentn = summay_list[0] - summay_list[1] - summay_list[2]
    #     summay_list[3] = sentn

    #     # Bracketing Recall: matched brackets / gold brackets
    #     summay_list[4] = (sum([item.matched_brackets for
    #                            item in correct_results]) /
    #                       sum([item.gold_brackets for
    #                            item in correct_results]))

    #     # Bracketing Precision: matched brackets / test brackets
    #     summay_list[5] = (sum([item.matched_brackets for
    #                           item in correct_results]) /
    #                       sum([item.test_brackets for
    #                           item in correct_results]))

    #     # Bracketing FMeasure
    #     summay_list[6] = ((2 * summay_list[4] * summay_list[5]) /
    #                       (summay_list[4] + summay_list[5]))

    #     # Complete match
    #     summay_list[7] = (len([item for item in correct_results
    #                       if item.matched_brackets == item.gold_brackets and
    #                       item.matched_brackets ==
    #                       item.test_brackets]) / sentn * 100)

    #     # Average match
    #     summay_list[8] = (sum([item.cross_brackets for
    #                       item in correct_results]) / sentn)

    #     # No crossing
    #     summay_list[9] = (len([item for item in correct_results
    #                       if item.cross_brackets == 0]) / sentn * 100)

    #     # Tagging accuracy: total correct tags / total words
    #     summay_list[10] = (sum([item.correct_tags for item
    #                        in correct_results]) /
    #                        sum([item.words for item in correct_results]))

    #     return summay_list

    # def evalb(self, gold_file_name, test_file_name):
    #     gold_file = open(gold_file_name)
    #     test_file = open(test_file_name)
    #     results = self.score_corpus(gold_file, test_file)
    #     summary = self.summary(results)
    #     string = []

    #     string.append(self._set_head())
    #     string.append(self.result2string(results))
    #     string.append(self._set_tail())
    #     string.append(self.summary2string(summary))
    #     return '\n'.join(string)
