# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.1
#
# Date: 2016-10-14 09:32:33
# Last modified: 2016-10-14 14:16:38

"""
Sum up the score result and wirte as markdown table.
"""

import collections

import pytablewriter

from PYEVALB.scorer import Result

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
