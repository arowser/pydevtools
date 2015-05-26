# Python modules for Software Development Tools #
PyDevTools is a suite of python modules for the rapid prototyping of software development tools.

Currently, the project include modules for:
  * ELF handling
  * DWARF handling

If you have any issues, please try the latest version from SVN. If it doesn't help, report a [new issue](http://code.google.com/p/pydevtools/issues/entry) for bugs, or desired features. (possibly, attaching the target ELF file to reproduce the issue).

For any feedback, or for joining the project, just drop an e-mail at our developers google group: https://groups.google.com/d/forum/pydevtools

Large part of the modules has been developed for internal applications at [CSR](http://www.csr.com) (copyright owner).
CSR allowed to release the whole project under the BSD license.

## Install ##
```
easy_install BinTools
```
If you have issues please first try latest source from SVN repository. See Source tab for instructions.

## Dwarf Dump ##
```
$ ./dwarfdump.py ../test/test

[...]
<1><137> subprogram
external: True
name: dummy_a
decl_file: a/test.c
decl_line: 10
prototyped: True
low_pc: 0x08048403
high_pc: 0x08048410
frame_base: 
    <0x1f:0x20> DW_OP_breg4:+4
    <0x20:0x22> DW_OP_breg4:+8
    <0x22:0x2c> DW_OP_breg5:+8

<1><158> variable
name: my_static_var
decl_file: a/test.c
decl_line: 4
type: 79
location: DW_OP_addr:+134520852

.debug_line: line number info for a single cu
a/test.c [  6,0] 0x080483e4 - is_stmt
a/test.c [  7,0] 0x080483ea - is_stmt
a/test.c [  8,0] 0x08048401 - is_stmt
a/test.c [ 10,0] 0x08048403 - is_stmt
a/test.c [ 11,0] 0x08048409 - is_stmt
[...]
```

## DWARF Viewer ##
```
./dwarfviewer.py ../test/test
```

![http://www.emilmont.net/lib/exe/fetch.php?media=tools:dwarfviewer.png](http://www.emilmont.net/lib/exe/fetch.php?media=tools:dwarfviewer.png)

## DWARF Query ##
```
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
```

## ELF ##
```
>>> from bintools.elf import ELF
>>> elf = ELF('../test/test')
>>> for s in elf.sect_dict['.text'].get_symbols():
...     print s.get_name()
... 

__do_global_dtors_aux
frame_dummy
__do_global_ctors_aux
my_static_func
f3
f2
__libc_csu_fini
_start
__libc_csu_init
f1
dummy_a
__i686.get_pc_thunk.bx
main
dummy_b
[...]
```