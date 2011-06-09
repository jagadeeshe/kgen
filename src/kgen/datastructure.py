'''
Created on Jun 8, 2011

@author: jagadeesh
'''
from UserList import UserList

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

    def defaultToFail(self):
        return self.isCOMMIT()

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

    def isPairwiseSame(self, other):
        if other is None: return False
        if type(other) is not PatternElement: return False
        if self.lex == other.lex and self.sur == other.sur:
            return True
        else:
            return False
        
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
    def __init__(self, padding=0):
        self.column_to_index = {}
        self.index_to_column = []
        self.padding = padding
    
    def add(self, pe):
        if not self.column_to_index.has_key((pe.lex, pe.sur)):
            self.index_to_column.append(pe)
            self.column_to_index[(pe.lex, pe.sur)] = len(self.index_to_column) - 1
        if pe.isCOMMIT():
            idx = self.column_to_index[(pe.lex, pe.sur)]
            self.index_to_column[idx].mark_COMMIT()
        return self.column_to_index[(pe.lex,pe.sur)]
    
    def indexof(self, pe):
        return self.column_to_index[(pe.lex, pe.sur)]
    
    def __getitem__(self, index):
        return self.index_to_column[index]
    
    def __iter__(self):
        for i in range(len(self.index_to_column)):
            yield (i, self.index_to_column[i])
    
    def match(self, pe):
        for col_index, col in self:
            if col.isPairwiseSame(pe) and (not col.defaultToFail() or pe.isCOMMIT()):
                yield (col_index, col)
        
    def __len__(self):
        return len(self.index_to_column)
    
    def __str__(self):
        output1 = ' ' * (self.padding + 2)
        output2 = ' ' * (self.padding + 2)
        output3 = ' ' * (self.padding + 2)
        for pe in self.index_to_column:
            output1 += ' %s' % pe.lex
            output2 += ' %s' % pe.sur
            output3 += '--'
        output1 += ' @'
        output2 += ' @'
        output3 += '--'
        return "%s\n%s\n%s-" % (output1, output2, output3)


class KgenTable(object):
    def __init__(self, column_size, padding=0):
        self.column_size = column_size
        self.padding = padding
        self.rows = []
        self._add_default_row()
        self._add_default_row()
    
    def _add_default_row(self):
        cols = [0] * self.column_size
        row = UserList(cols)
        row.context = []
        row.committed = False
        self.rows.append(row)
        return row
    
    def add_transition(self, from_state, column_index, to_state):
        self.rows[from_state][column_index] = to_state
    
    def create_state(self, old_state, pe):
        new_state = len(self) + 1
        self._add_default_row()
        self.rows[new_state].context = self.rows[old_state].context[:]
        self.rows[new_state].context.append(pe)
        return new_state
    
    def __getitem__(self, index):
        state = 0
        col_idx = None
        if type(index) == int and index != 0:
            state = index
        elif type(index) == tuple and len(index) == 2:
            state = index[0]
            col_idx = index[1]
        else:
            raise IndexError("list index out of range")
        if col_idx != None:
            if state <= len(self):
                return self.rows[state][col_idx]
            else:
                return 0
        else:
            return self.rows[state]
    
    def __iter__(self):
        for state in range(1, len(self)+1):
            yield state
    
    def __len__(self):
        return len(self.rows) - 1
    
    def __str__(self):
        output = ''
        for r in self:
            output += ' ' * self.padding
            output += '%d' % r
            if self[r].committed:
                output += '.'
            else:
                output += ':'
            for c in range(self.column_size):
                output += ' %d' % max(0, self[r,c])
            if self[r].committed:
                output += ' 0'
            else:
                output += ' 1'
            output += '\n'
        return output


NODE_TYPE_KIMMOCOMMENT = 1
NODE_TYPE_SUBSET = 2
NODE_TYPE_PAIR = 3
NODE_TYPE_RULE = 4
NODE_TYPE_NEWLINE = 5

class Node(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


class ParseTree(object):
    def __init__(self):
        self.nodes = []
        self.subsets = {}
        self.lhs = None
        self.operator = ''
        self.rhs = None
        self.columns = []
    
    def r_error(self):
        pass
    
    def add_ruleset(self):
        pass
    
    def add_eol(self):
        self.nodes.append(Node(NODE_TYPE_NEWLINE, '\n'))
    
    def r_opt_eol(self):
        pass
    
    def r_opt_eol_empty(self):
        pass
    
    def add_kimmo_comment(self, comment):
        self.nodes.append(Node(NODE_TYPE_KIMMOCOMMENT, comment))
    
    def has_subset_name(self, name):
        return self.subsets.has_key(name)
    
    def get_subset(self, name):
        return self.subsets[name][1]
    
    def subset_lineno(self, name):
        return self.subsets[name][0]
    
    def add_subset(self, subset, lineno):
        self.subsets[subset[0]] = (lineno, subset[1])
        self.nodes.append(Node(NODE_TYPE_SUBSET, (lineno, subset[0], subset[1])))
    
    def add_pair(self, s1, s2):
        self.nodes.append(Node(NODE_TYPE_PAIR, (s1, s2)))
    
    def add_rule(self, lineno):
        self.nodes.append(Node(NODE_TYPE_RULE, (lineno, self.rhs, self.columns)))

    def __iter__(self):
        for node in self.nodes:
            yield node
