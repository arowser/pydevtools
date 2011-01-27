from sys import argv, path
path.append('..')

from unittest import TestCase, main
from bintools.dwarf import DWARF


class TestDwarfQuery(TestCase):
    def setUp(self):
        self.dwarf = DWARF('../test/test')
    
    def test_loc_by_addr(self):
        loc = self.dwarf.get_loc_by_addr(0x8048475)
        self.assertEqual(loc, ('/home/emilmont/Workspace/dbg/test/main.c', 36, 0))
    
    def test_loc_by_sym(self):
        loc = self.dwarf.get_loc_by_sym('main')
        self.assertEqual(loc, ('/home/emilmont/Workspace/dbg/test/main.c', 54, 0)) 
        
        loc = self.dwarf.get_loc_by_sym('temp')
        self.assertEqual(loc, ('/home/emilmont/Workspace/dbg/test/main.c', 15, 0))
    
    def test_addr_by_sym(self):
        addr = self.dwarf.get_addr_by_sym('main')
        self.assertEqual(addr, 0x80484ac)
    
    def test_addr_by_loc(self):
        addr = self.dwarf.get_addr_by_loc('a/test.c', 10)
        self.assertEqual(addr, 0x8048403)


if __name__ == '__main__':
    main()
