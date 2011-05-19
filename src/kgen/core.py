'''
Created on May 5, 2011

@author: jagadeesh
'''


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

        'REG_OR',
        'REG_REPEAT',
        'UNDER',
    )

class KgenException(Exception): pass

class TwoLevelString(object):

    def __init__(self, other=None):
        self.lexical = ''
        self.surface = ''
        if other != None:
            self += other

    def __add__(self, other):
        self._validate(other)
        if type(other) == TwoLevelString:
            self.lexical += other.lexical
            self.surface += other.surface
            return self
        else:
            self.lexical += other[0]
            self.surface += other[1]
            return self

    def _validate(self, other):
        if type(other) == tuple:
            if len(other) != 2:
                raise KgenException("tuple with length > 2 is not allowed")
            lex, sur = other
            if lex == None or sur == None or lex == '' or sur == '':
                raise KgenException("one or both of lex, sur either None or empty")
            if len(lex) != 1 or len(sur) != 1:
                raise KgenException("length of lex or sur is not 1")
        elif type(other) != TwoLevelString:
            raise KgenException("cannot add %s" % other)

    def __getitem__(self, index):
        return (self.lexical[index], self.surface[index])

    def __len__(self):
        return len(self.lexical)

    def __iter__(self):
        for i in range(len(self.lexical)):
            yield (self.lexical[i], self.surface[i])

    def __eq__(self, other):
        if type(other) != TwoLevelString:
            return False
        return self.lexical == other.lexical and self.surface == other.surface
