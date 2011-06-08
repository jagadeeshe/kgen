'''
Created on May 5, 2011

@author: jagadeesh
'''
import copy

FAIL = -1

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
        ''' add commit column '''
        pe.mark_COMMIT()
        ast.columns.append(pe)


def add_obligatory_lhs(lhs, ast):
    for pe in lhs:
        ''' add normal column '''
        pe1 = copy.deepcopy(pe)
        ast.columns.append(pe1)
        ''' add complement column '''
        pe.sur = '@'
        ast.columns.append(pe)
