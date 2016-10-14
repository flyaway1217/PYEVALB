# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-14 09:32:33
# Last modified: 2016-10-14 14:35:02

"""
Sum up the score result and wirte as markdown table.
"""

import collections

import pytablewriter


SUMMARY_TABLE = [
            'Number of sentence', 'Number of Error sentence',
            'Number of Skip  sentence', 'Number of Valid sentence',
            'Bracketing Recall', 'Bracketing Precision',
            'Bracketing FMeasure', 'Complete match',
            'Average crossing', 'No crossing', 'Tagging accuracy'
            ]

SUMMARY_NAME_TABLE = [
            'sent_num', 'error_sent_num',
            'skip_sent_num', 'valid_sent_num',
            'bracket_recall', 'bracket_prec',
            'bracker_fmeasure', 'complete_match',
            'average_crossing', 'no_crossing', 'tagging_accuracy'
            ]

Summary = collections.namedtuple('Summary', SUMMARY_NAME_TABLE)


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

    def __init__(self):
        self._staticis = dict()

        # Initialize the dict
        for name in Result.STATISTICS_TABLE:
            self._staticis[name] = 0

    def tolist(self):
        reval = []
        for name in Result.STATISTICS_TABLE:
            value = self._staticis[name]
            if type(value) == int:
                value = '%d' % value
            else:
                value = '%.2f' % value
            reval.append(value)
        return reval

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


def write_table(path, results, summary):
    with open(path, 'w', encoding='utf8') as f:
        writer = pytablewriter.MarkdownTableWriter()
        writer.stream = f
        writer.table_name = 'Score Result'
        writer.header_list = [' ' + v + ' ' for v
                              in Result.STATISTICS_TABLE]
        writer.value_matrix = [v.tolist() for v in results]
        writer.write_table()

        summary = _summary2string(summary)

        f.write('\n')
        f.write('='*145)
        f.write('\n')
        f.write(summary)


def summary(results):
    """Calculate the summary of resutls

    Args:
        results: a list of result of each sentence

    Returns:
        a list contains all the summary data.
        The data in the list is ordered by Result.SUMMARY_TABLE.
    """
    summay_list = [0] * len(SUMMARY_TABLE)

    # Number of sentence
    summay_list[0] = len(results)

    # Number of Error sentence
    # 2:Error
    summay_list[1] = len([item for item in results if item.state == 2])

    # Number of Skip sentence
    # 1:skip
    summay_list[2] = len([item for item in results if item.state == 1])

    correct_results = [item for item in results if item.state == 0]
    sentn = len(correct_results)

    # Number of Skip sentence
    summay_list[3] = sentn

    # Bracketing Recall: matched brackets / gold brackets
    summay_list[4] = (sum([item.matched_brackets for
                           item in correct_results]) /
                      sum([item.gold_brackets for
                           item in correct_results])) * 100

    # Bracketing Precision: matched brackets / test brackets
    summay_list[5] = (sum([item.matched_brackets for
                          item in correct_results]) /
                      sum([item.test_brackets for
                          item in correct_results])) * 100

    # Bracketing FMeasure
    summay_list[6] = ((2 * summay_list[4] * summay_list[5]) /
                      (summay_list[4] + summay_list[5]))

    # Complete match
    summay_list[7] = (len([item for item in correct_results
                      if item.matched_brackets == item.gold_brackets and
                      item.matched_brackets ==
                      item.test_brackets]) / sentn * 100)

    # Average crossing
    summay_list[8] = (sum([item.cross_brackets for
                      item in correct_results]) / sentn)

    # No crossing
    summay_list[9] = (len([item for item in correct_results
                      if item.cross_brackets == 0]) / sentn * 100)

    # Tagging accuracy: total correct tags / total words
    summay_list[10] = (sum([item.correct_tags for item
                       in correct_results]) /
                       sum([item.words for item in correct_results])) * 100

    summay_list = [float(v) for v in summay_list]
    return Summary(*summay_list)

########################################################
# Helping methods
########################################################


def _summary2string(summary):
    string = []
    for name, value in zip(SUMMARY_TABLE, summary):
        string.append(name+":\t"+'{0:.2f}'.format(value))
    return '\n'.join(string)
