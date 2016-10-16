# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author: Flyaway - flyaway1217@gmail.com
# Blog: zhouyichu.com
#
# Python release: 3.4.5
#
# Date: 2016-10-15 16:11:29
# Last modified: 2016-10-15 17:59:37

"""
Comamnd interface
"""
import argparse

from PYEVALB.scorer import Scorer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('gold_path', help='The path of gold tree bank.',
                        type=str)

    parser.add_argument('test_path', help='The path of test tree bank.',
                        type=str)
    parser.add_argument('result_path', help='The path of result report.',
                        type=str)

    args = parser.parse_args()

    scorer = Scorer()
    scorer.evalb(args.gold_path, args.test_path, args.result_path)

if __name__ == '__main__':
    main()
