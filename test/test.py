# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 21:08:30
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 21:08:30
@Desc:
"""

from operator import itemgetter, attrgetter

d1 = {1:23, 'b': 62}
d2 = {1:24, 'b': 2}
d3 = {1:23, 'b': 54}
d4 = {1:23, 'b': 1}
d5 = {1:1, 'b': 9}
d6 = {1:23, 'b': 32}
d7 = {1:5, 'b': 33}
d8 = {1:39, 'b': 100}

li = [d1, d2, d3, d4, d5, d6, d7, d8]

def cmpf(a, b, key1, key2):
     if (a[key1] != b[key1]):
             return a[key1] - b[key1]
     else:
             return a[key2] - b[key2]

def rcmpf(a, b, key1, key2):
     if (a[key1] != b[key1]):
             return b[key1] - a[key1]
     else:
             return a[key2] - b[key2]

# key1、key2均为升序
AA = sorted(li, cmp=lambda a,b: cmpf(a, b, 1, 'b'))

# key1降序、key2升序
BB = sorted(li, cmp=lambda a,b: rcmpf(a, b, 1, 'b'))
print(AA)
print(BB)

# student_tuples = [('john', 'A', 15),('jane', 'B', 12),('dave', 'B', 10)]
# def XXOO(tInfo1, tInfo2, x, y):
#     if tInfo1[x] != tInfo2[x]:
#         return tInfo1[x] > tInfo2[x]    # x 升序
#     return tInfo1[y] < tInfo2[y]        # y 降序
# AA = sorted(student_tuples, key = itemgetter(1, 2))
# BB = sorted(student_tuples, key = itemgetter(1, 2), reverse=True)
# CC = sorted(student_tuples, cmp=lambda a,b: XXOO(a, b, 1, 2))
# print(AA)
# print(BB)
# print(CC)
