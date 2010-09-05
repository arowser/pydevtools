"""
Copyright (c) 2010, Cambridge Silicon Radio Ltd.
Written by Emilio Monti <emilmont@gmail.com>
"""
from array import array
from devtools.elf.stream import ParseError
from devtools.elf.enums import SHT, SHF


class Header:
    def __init__(self, elf):
        elf.constant(4, "\x7fELF")
        
        elf.set_bits(elf.u08())
        elf.set_endianness(elf.u08())
        
        self.version = elf.u08()
        elf.skip(9)
        
        self.type = elf.u16()
        self.machine = elf.u16()
        self.version = elf.u32()
        self.entry = elf.u32()
        self.ph_offset = elf.u32()
        self.sh_offset = elf.u32()
        self.flags = elf.u32()
        self.header_size = elf.u16()
        self.ph_entry_size = elf.u16()
        self.ph_count = elf.u16()
        self.sh_entry_size = elf.u16()
        self.sh_count = elf.u16()
        self.shstrndx = elf.u16()


class SectionHeader:
    def __init__(self, elf, index):
        self.elf = elf
        self.index = index
        
        self.name_index = elf.u32()
        self.type = elf.u32()
        self.flags = elf.u32()
        self.addr = elf.u32()
        self.offset = elf.u32()
        self.size = elf.u32()
        self.link = elf.u32()
        self.info = elf.u32()
        self.addralign = elf.u32()
        self.entsize = elf.u32()
        
        self.name = None
    
    def is_loadable(self):
        return self.type == SHT.PROGBITS and self.flags & SHF.ALLOC == SHF.ALLOC
    
    def is_execinstr(self):
        return self.flags & SHF.EXECINSTR == SHF.EXECINSTR
    
    def get_name(self):
        if self.name == None:
            self.name = self.elf.shstrtab[self.name_index]
        return self.name
    
    def get_symbols(self):
        return [sym for sym in self.elf.symbols if sym.shndx == self.index]


class ProgramHeader:
    def __init__(self, elf, index):
        self.elf = elf
        self.index = index
        
        self.type = elf.u32()
        self.offset = elf.u32()
        self.vaddr = elf.u32()
        self.paddr = elf.u32()
        self.filesz = elf.u32()
        self.memsz = elf.u32()
        self.flags = elf.u32()
        self.align = elf.u32()


class Symbol:
    LENGTH = 16
    
    def __init__(self, elf, index):
        self.elf = elf
        self.index = index
        
        self.name_index = elf.u32()
        self.value = elf.u32()
        self.size = elf.u32()
        self.info = elf.u08()
        self.other = elf.u08()
        self.shndx = elf.u16()
        
        self.name = None
    
    def get_name(self):
        if self.name is None:
            self.name = self.elf.strtab[self.name_index]
        return self.name
    
    def get_bind(self):
        return self.info >> 4
    
    def get_type(self):
        return self.info & 0xF


class StringTable:
    def __init__(self, stream, offset, size):
        self.offset = offset
        stream.seek(offset)
        self.table = array('c', stream.read(size))
        self.max = len(self.table)
    
    def __getitem__(self, key):
        if (key >= self.max):
            raise ParseError('The required index is out of the table: (0x%x) +%d (max=%d)' % (self.offset, key, self.max))
        i = self.table[key:].index('\x00') + key
        return self.table[key:i].tostring()
