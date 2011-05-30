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

class PatternElement(object):
    DEFAULT = 0
    COMMIT = 1
    REPEAT = 2
    ALTERNATIVE = 4

    def __init__(self, lex, sur=None, flag=0):
        if not sur:
            sur = lex
        self.lex = lex
        self.sur = sur
        self.flag = flag

    def mark_COMMIT(self):
        self.flag |= PatternElement.COMMIT

    def mark_REPEAT(self):
        self.flag |= PatternElement.REPEAT

    def mark_ALTERNATIVE(self):
        self.flag |= PatternElement.ALTERNATIVE

    def isCOMMIT(self):
        if (self.flag & PatternElement.COMMIT) == 0:
            return False
        else:
            return True

    def isREPEAT(self):
        if (self.flag & PatternElement.REPEAT) == 0:
            return False
        else:
            return True

    def isALTERNATIVE(self):
        if (self.flag & PatternElement.ALTERNATIVE) == 0:
            return False
        else:
            return True

    def __eq__(self, other):
        if other is None: return False
        if type(other) is not PatternElement: return False
        if self.lex == other.lex and self.sur == other.sur and self.flag == other.flag:
            return True
        else:
            return False

    def __repr__(self):
        return "(%s,%s,%d)" % (self.lex, self.sur, self.flag)


PE = PatternElement

class PEmap(object):
    def __init__(self):
        self.column_to_index = {}
        self.index_to_column = []
    
    def add(self, pe):
        if not self.column_to_index.has_key(pe):
            self.index_to_column.append(pe)
            self.column_to_index[pe] = len(self.index_to_column) - 1
        return self.column_to_index[pe]
    
    def indexof(self, pe):
        return self.column_to_index[pe]
    
    def get(self, index):
        return self.index_to_column[index]
    
    def __iter__(self):
        for pe in self.index_to_column:
            yield pe
    
    def __len__(self):
        return len(self.index_to_column)


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
