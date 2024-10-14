#!/usr/bin/env python3
'''
read conjure JSON output representing an Essence spec
'''

import sys
import json
A = json.load(sys.stdin)
print(A['mLanguage']['language']['Name'])
print(A['mLanguage']['version'])
statements = A['mStatements']
#print(len(statements), "statements")
for s in statements:
    if not 'SuchThat' in s: continue
    c = s['SuchThat']
    if not c: continue
    for constraint in c:
        if not 'Op' in constraint: continue
        d = constraint['Op']
        if not d: continue
        if not 'MkOpEq' in d: continue
        e = d['MkOpEq']
        if len(e) != 2: continue
        lhs = e[0]
        rhs = e[1]
        # print(lhs, '=', rhs)
        if len(lhs) == 1 and 'Op' in rhs:
             rhs = rhs['Op']
             if 'MkOpSum' in rhs:
                 rhs = rhs['MkOpSum']
                 if not 'AbstractLiteral' in rhs: continue
                 rhs = rhs['AbstractLiteral']['AbsLitMatrix']
                 if len(rhs) == 2:
                     lhs = rhs[0]
                     rhs = rhs[1]
                     print(lhs, '+', rhs)

# want to rewrite:
# X '+' Y -> Y '+' X
# if X > Y lexically and they are both non-constant expressions
# X + Y -> value(X) + value(Y)
# if they are both constants

#print(A)
