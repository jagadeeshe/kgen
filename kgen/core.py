'''
Created on May 5, 2011

@author: jagadeesh
'''
__version__ = "1.0"

import sys
import copy
from optparse import OptionParser
from UserDict import UserDict
from datastructure import PE

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


def add_optional_element(list1):
    for pe_list in list1:
        if pe_list[0] == PE(''):
            return
    list1.append([PE('')])

def mark_alternate(alt_list):
    itemlist = alt_list[0]
    for i in range(len(itemlist)-1):
        itemlist[i].mark_ALTERNATIVE()


def add_optional_lhs(lhs_list, ast):
    for lhs_row in lhs_list:
        for pe in lhs_row:
            ''' add commit column '''
            pe.mark_COMMIT()
            ast.columns.append(pe)


def add_obligatory_lhs(lhs_list, ast):
    for lhs_row in lhs_list:
        for pe in lhs_row:
            ''' add normal column '''
            pe1 = copy.deepcopy(pe)
            ast.columns.append(pe1)
            ''' add complement column '''
            pe.sur = '@'
            ast.columns.append(pe)


config = UserDict()
config.verbose = False
config.input = ''
config.output = ''

def init_args(args, values):
    usage = "usage: %prog [options] INPUT-FILE OUTPUT-FILE"
    description = '''This program is used to compile pc-kimmo two level rules into state tables.
INPUT-FILE - text file containing two-level rule description.
OUTPUT-FILE - pc-kimmo rule file.
'''
    version = "kgen %s"%__version__
    
    parser = OptionParser(usage=usage, description=description, version=version)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="generate debug information")
    
    (_, args) = parser.parse_args(args=args, values=values)
    
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)
    values.input = args[0]
    values.output = args[1]
