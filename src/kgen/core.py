'''
Created on May 5, 2011

@author: jagadeesh
'''
import copy


tokens = (
        'KIMMO_COMMENT',
        'COMMENT',

        'ID',

        'EOL',
        'SEGMENT',
        'SUBSET',
        'SUBSET_NAME',
        'PAIRS',
        'RULE',

        'ONLY_OCCURS',
        'ALWAYS_OCCURS',
        'ALWAYS_AND_ONLY_OCCURS',
        'NEVER_OCCURS',

        'COLON',
        'COMMA',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',

        'REG_OR',
        'REG_REPEAT',
        'UNDER',
    )

class PatternElement(list):
    DEFAULT = 0
    COMMIT = 1
    REPEAT = 2
    ALTERNATIVE = 4

    def __init__(self, lex, sur=None, flag=0):
        if not sur:
            sur = lex
        list.__init__(self, [lex, sur, flag])

    def mark_COMMIT(self):
        self[2] |= PatternElement.COMMIT

    def mark_REPEAT(self):
        self[2] |= PatternElement.REPEAT

    def mark_ALTERNATIVE(self):
        self[2] |= PatternElement.ALTERNATIVE

    def isCOMMIT(self):
        if (self[2] & PatternElement.COMMIT) == 0:
            return False
        else:
            return True

    def isREPEAT(self):
        if (self[2] & PatternElement.REPEAT) == 0:
            return False
        else:
            return True

    def isALTERNATIVE(self):
        if (self[2] & PatternElement.ALTERNATIVE) == 0:
            return False
        else:
            return True

PE = PatternElement


def cross_product(list1, list2):
    target = []
    for s1 in list1:
        for s2 in list2:
            target.append(s1 + s2)
    return target


def mark_alternate(alt_list):
    itemlist = alt_list[0]
    for i in range(len(itemlist)-1):
        itemlist[i].mark_ALTERNATIVE()


def add_optional_lhs(lhs, ast):
    for pe in lhs:
        pe.mark_COMMIT()
        ast.columns.append(pe)


def add_obligatory_lhs(lhs, ast):
    for pe in lhs:
        pe1 = copy.deepcopy(pe)
        ast.columns.append(pe1)
        pe[1] = '@' # complement
        ast.columns.append(pe)
