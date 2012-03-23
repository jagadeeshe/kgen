'''
Created on May 11, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from mock_ast import MockAST
from kgen.datastructure import PE
from StringIO import StringIO

class parserTest(unittest.TestCase):

    def __init__(self, methodName='run'):
        unittest.TestCase.__init__(self, methodName)
        klexer = KgenLexer()
        mockAST = MockAST()
        self.output = StringIO()
        self.kparser = KgenParser(klexer, self.output, mockAST)


    def test_p_kimmo_comments_empty(self):
        data = ''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, len(mockAST.kimmo_comments))


    def test_p_kimmo_comment(self):
        data = '''!;kimmo comment
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual([';kimmo comment'], mockAST.kimmo_comments)
        self.assertEqual(0, mockAST.eol_term)


    def test_p_kimmo_comments(self):
        data = '''!;first comment
                  !;second comment
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual([';first comment', ';second comment'], mockAST.kimmo_comments)
        self.assertEqual(0, mockAST.eol_term)


    def test_p_kimmo_comments_spaced(self):
        data = '''!;first comment
                  
                  !;second comment
                  
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual([';first comment', ';second comment'], mockAST.kimmo_comments)
        self.assertEqual(2, mockAST.eol_term)


    def test_p_eol_term(self):
        data = '''
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(1, mockAST.eol_term)


    def test_p_eol(self):
        data = '''
                
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(2, mockAST.eol_term)


    def test_p_opt_eol_empty(self):
        data = ''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, mockAST.opt_eol)
        self.assertEqual(1, mockAST.opt_eol_empty)


    def test_p_opt_eol(self):
        data = '''
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, mockAST.opt_eol_empty)
        self.assertEqual(1, mockAST.opt_eol)


    def test_p_subsets_empty(self):
        data = ''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, len(mockAST.subsets))


    def test_p_subset_unnamed(self):
        data = '''
                SUBSET     a
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(1, mockAST.error)
        self.assertEqual('Line 2: subset should have name. see the rule for naming a subset.\n', self.output.getvalue())


    def test_p_subset_unnamed_and_named(self):
        data = '''
                SUBSET     a
                SUBSET C b c d f
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(1, mockAST.error)
        self.assertEqual('Line 2: subset should have name. see the rule for naming a subset.\n', self.output.getvalue())
        self.assertEqual(1, len(mockAST.subsets))
        self.assertEqual('bcdf', mockAST.get_subset('C'))


    def test_p_subset_no_segment_string(self):
        data = '''
                SUBSET A
                
                SUBSET C    b c d f
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(1, mockAST.error)
        self.assertEqual('Line 2: subset definition should be on the same line.\n', self.output.getvalue())
        self.assertEqual(1, len(mockAST.subsets))
        self.assertEqual('bcdf', mockAST.get_subset('C'))


    def test_p_duplicate_subset_definition(self):
        data = '''
                SUBSET A     a
                SUBSET A     e i o u
                
                SUBSET C    b c d f
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('Line 3: subset A is already defined in line 2.\n', self.output.getvalue())
        self.assertEqual(2, len(mockAST.subsets))
        self.assertEqual('a', mockAST.get_subset('A'))
        self.assertEqual('bcdf', mockAST.get_subset('C'))


    def test_p_subsets(self):
        data = '''
                SUBSET V    a
                SUBSET C    b c d f
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(2, len(mockAST.subsets))
        self.assertEqual('a', mockAST.get_subset('V'))
        self.assertEqual('bcdf', mockAST.get_subset('C'))


    def test_p_pairlist(self):
        data = '''
            PAIRS b c d +
                  b c d 0
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(4, len(mockAST.pairs))
        self.assertTrue(mockAST.pairs.has_key(('b', 'b')))
        self.assertTrue(mockAST.pairs.has_key(('c', 'c')))
        self.assertTrue(mockAST.pairs.has_key(('d', 'd')))
        self.assertTrue(mockAST.pairs.has_key(('+', '0')))


    def test_p_lhs_pair(self):
        data = '''RULE 
            p:b => a _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        p1 = [PE('p', 'b', PE.COMMIT)]
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual([p1], mockAST.lhs)
        self.assertEqual(p1, mockAST.columns)


    def test_p_rule_only_occurs(self):
        data = '''RULE 
            p:b => a _ b
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('=>', mockAST.operator)


    def test_p_rule_only_occurs_left_context(self):
        data = '''RULE 
            p:b => a _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('=>', mockAST.operator)
        self.assertEqual([[PE('a')]], mockAST.lc)
        self.assertEqual(None, mockAST.rc)


    def test_p_rule_only_occurs_long_left_context(self):
        data = '''RULE 
            p:b => abc _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('=>', mockAST.operator)
        self.assertEqual([[PE('a'), PE('b'), PE('c')]], mockAST.lc)
        self.assertEqual(None, mockAST.rc)


    def test_p_rule_only_occurs_right_context(self):
        data = '''RULE 
            p:b => _ a
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('=>', mockAST.operator)
        self.assertEqual([[PE('a')]], mockAST.rc)
        self.assertEqual(None, mockAST.lc)


    def test_p_rule_always_occurs(self):
        data = '''RULE 
            p:b <= a _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('<=', mockAST.operator)
        self.assertEqual([[PE('a'),PE('p','@')]], mockAST.rhs)
        self.assertEqual([PE('p','b'),PE('p','@')], mockAST.columns)


    def test_p_rule_never_occurs(self):
        data = '''RULE 
            p:b /<= a _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('/<=', mockAST.operator)
        self.assertEqual(0, len(mockAST.columns))


    def test_p_rule_only_and_always_occurs(self):
        data = '''RULE 
            p:b <=> a _ 
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual('<=>', mockAST.operator)
        self.assertEqual([[PE('a'),PE('p','@')], [PE('a'),PE('p','b',PE.COMMIT)]], mockAST.rhs)
        self.assertEqual([PE('p','b'),PE('p','@'),PE('p','b',PE.COMMIT)], mockAST.columns)

