# PYEVALB

EVEVALB is a python version of [Evalb][] which is used to score the bracket tree banks.

# Examples

## Score two corpus

```python
from PYEVALB import scorer

gold_path = 'gold_corpus.txt'
test_path = 'test_corpus.txt'
result_path = 'result.txt'

scorer.evalb(gold_path, test_path, result_path)
```

And the result would be:
```Markdown

 ID | length | state | recall | prec | matched_brackets | gold_brackets | test_brackets | cross_brackets | words | correct_tags | tag_accracy 
---:|-------:|------:|-------:|-----:|-----------------:|--------------:|--------------:|---------------:|------:|-------------:|------------:
   0|      44|      0|    0.57|  0.61|                31|             54|             51|              16|     44|            43|         0.98
   1|      13|      0|    0.64|  0.60|                 9|             14|             15|               3|     13|            12|         0.92
   2|      29|      0|    0.97|  0.97|                29|             30|             30|               0|     29|            29|         1.00
   3|      20|      0|    0.80|  0.80|                20|             25|             25|               4|     20|            20|         1.00
   4|      19|      0|    0.91|  1.00|                21|             23|             21|               0|     19|            19|         1.00
   5|      71|      0|    0.67|  0.68|                52|             78|             77|              15|     71|            65|         0.92
   6|      16|      0|    0.61|  0.69|                11|             18|             16|               0|     16|            14|         0.88
   7|      27|      0|    0.92|  0.96|                24|             26|             25|               0|     27|            26|         0.96
   8|      19|      0|    1.00|  1.00|                20|             20|             20|               0|     19|            19|         1.00
   9|      41|      0|    0.80|  0.78|                32|             40|             41|               5|     41|            39|         0.95

=================================================================================================================================================
Number of sentence:	10.00
Number of Error sentence:	0.00
Number of Skip  sentence:	0.00
Number of Valid sentence:	10.00
Bracketing Recall:	75.91
Bracketing Precision:	77.57
Bracketing FMeasure:	76.73
Complete match:	10.00
Average crossing:	4.30
No crossing:	50.00
Tagging accuracy:	95.65
```

## Score two trees

```python
from PYEVALB import scorer
from PYEVALB import parser

gold = '(IP (NP (PN 这里)) (VP (ADVP (AD 便)) (VP (VV 产生) (IP (NP (QP (CD 一) (CLP (M 个))) (DNP (NP (JJ 结构性)) (DEG 的)) (NP (NN 盲点))) (PU ：) (IP (VP (VV 臭味相投) (PU ，) (VV 物以类聚)))))) (PU 。))'

test = '(IP (IP (NP (PN 这里)) (VP (ADVP (AD 便)) (VP (VV 产生) (NP (QP (CD 一) (CLP (M 个))) (DNP (ADJP (JJ 结构性)) (DEG 的)) (NP (NN 盲点)))))) (PU ：) (IP (NP (NN 臭味相投)) (PU ，) (VP (VV 物以类聚))) (PU 。))'

gold_tree = parser.create_from_bracket_string(gold)
test_tree = parser.create_from_bracket_string(test)

result = scorer.score_trees(gold_tree, test_tree)

print('Recall =' + str(result.recall))
print('Precision =' + str(result.prec))
```

And the result is:

```bash
Recall = 64.29
Precision =  56.25
```


[Evalb]: http://nlp.cs.nyu.edu/evalb/
