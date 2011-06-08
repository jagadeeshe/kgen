'''
Created on Jun 6, 2011

@author: jagadeeshe
'''
import unittest
from kgen.datastructure import PE, KgenTable


class KgenTableTest(unittest.TestCase):

    def test_default(self):
        table = KgenTable(3)
        self.assertEqual(1, len(table))
        self.assertEqual('1: 0 0 0 1\n', str(table))

    def test_getitem(self):
        table = KgenTable(3)
        self.assertEqual(1, len(table))
        self.assertEqual(False, table[1].committed)
        self.assertEqual([], table[1].context)
        self.assertEqual(0, table[1,0])
        self.assertEqual(0, table[1,1])
        self.assertEqual(0, table[1,2])

    def test_getitem_indexerror(self):
        table = KgenTable(3)
        self.assertRaises(IndexError, table.__getitem__, 0)
        self.assertRaises(IndexError, table.__getitem__, '1')
        self.assertRaises(IndexError, table.__getitem__, (1, 2, 3))

    def test_add_transition(self):
        table = KgenTable(2)
        table.create_state(1, PE('m'))
        self.assertEqual(0, table[1,0])
        self.assertEqual(0, table[1,1])
        self.assertEqual(0, table[2,0])
        self.assertEqual(0, table[2,1])
        table.add_transition(1, 1, 2)
        self.assertEqual(0, table[1,0])
        self.assertEqual(2, table[1,1])
        self.assertEqual(0, table[2,0])
        self.assertEqual(0, table[2,1])
        table.add_transition(2, 0, 1)
        self.assertEqual(0, table[1,0])
        self.assertEqual(2, table[1,1])
        self.assertEqual(1, table[2,0])
        self.assertEqual(0, table[2,1])
        self.assertEqual('1: 0 2 1\n2: 1 0 1\n', str(table))

    def test_create_state(self):
        table = KgenTable(3)
        new_state = table.create_state(1, PE('m'))
        self.assertEqual(2, new_state)
        self.assertEqual(2, len(table))
        self.assertEqual([], table[1].context)
        self.assertEqual([PE('m')], table[2].context)

    def test_iter(self):
        table = KgenTable(3)
        for state in table:
            self.assertEqual(1, state)


if __name__ == "__main__":
    unittest.main()