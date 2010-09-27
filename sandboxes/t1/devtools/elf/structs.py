"""
Copyright (c) 2010, Cambridge Silicon Radio Ltd.
Written by Emilio Monti <emilmont@gmail.com>
"""
from array import array
from devtools.elf.stream import ParseError
from devtools.elf.enums import SHT, SHF, MACHINE, ELFCLASS, ELFDATA
import os

class Header(object):
    
    def __init__(self, elf):
        elf.constant(4, "\x7fELF")
        self._elfclass = elf.u08()
        elf.set_bits(self._elfclass)
        
        self.set_elfdata = elf.u08()
        elf.set_endianness(self.set_elfdata)
        
        self.version = elf.u08()
        elf.skip(9)
        
        self.type = elf.u16()
        self.machine_raw = elf.u16()
        self._machine = None
        self.set_machine(self.machine_raw)
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

    # machine property accessors
    def set_machine(self, value):
        if isinstance(value, str) and value.startswith('EM_'):
            value = getattr(MACHINE,value)
        
        if isinstance(value,MACHINE):
            self._machine = value
                        
        if isinstance(value,int):
            self._machine = value
        
    def get_machine(self):
        #look to return an enum name ...
        en_list = [ method for method in dir(MACHINE) \
                    if isinstance(getattr(MACHINE,method), int) and 
                    method.startswith('EM_')]
        
        #print en_list
        
        for en in en_list :
            if (getattr(MACHINE,en) == int(self._machine)):
                return en
        #enum name not found return raw value
        return self._machine
    
    def del_machine(self):
        del self._machine
        
    #use property 
    machine = property(get_machine,set_machine,del_machine,'machine definition')
    
    # elfclass property accessors
    def set_elfclass(self, value):
        if isinstance(value, str) and value.startswith('ELF'):
            value = getattr(ELFCLASS,value)
        
        if isinstance(value,ELFCLASS):
            self._elfclass = value
                        
        if isinstance(value,int):
            self._elfclass = value
        
    def get_elfclass(self):
        #look to return an enum name ...
        en_list = [ method for method in dir(ELFCLASS) \
                    if isinstance(getattr(ELFCLASS,method), int) and 
                    method.startswith('ELF')]
        
        for en in en_list :
            if (getattr(ELFCLASS,en) == int(self._elfclass)):
                return en
        #enum name not found return raw value
        return self._elfclass
    
    def del_elfclass(self):
        del self._elfclass
        
    #use property 
    elfclass = property(get_elfclass,set_elfclass,del_elfclass,'elf class')
    
    
    # elfdata property accessors
    def set_elfdata(self, value):
        if isinstance(value, str) and value.startswith('ELF'):
            value = getattr(ELFDATA,value)
        
        if isinstance(value,ELFDATA):
            self._elfdata = value
                        
        if isinstance(value,int):
            self._elfdata = value
        
    def get_elfdata(self):
        #look to return an enum name ...
        en_list = [ method for method in dir(ELFDATA) \
                    if isinstance(getattr(ELFDATA,method), int) and 
                    method.startswith('ELF')]
        
        for en in en_list :
            if (getattr(ELFDATA,en) == int(self._elfdata)):
                return en
        #enum name not found return raw value
        return self._elfdata
    
    def del_elfdata(self):
        del self._elfdata
        
    #use property 
    elfdata = property(get_elfdata,set_elfdata,del_elfdata,'elf data')
    
    

class SectionHeader(object):
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
        self._data = None
        
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
    
    def get_data(self):
        if self._data == None:
            curr_offset = self.elf.io.tell()
            self.elf.io.seek(self.offset, os.SEEK_SET)
            self._data = self.elf.io.read(self.size)
            self.elf.io.seek(curr_offset, os.SEEK_SET)
        return self._data
        
    def set_data(self, data):
        if len(data) != len(self.__data) :
            raise ParseError('Size of new data (%d) mismatch with current '
                                'size (%d)' % (len(data), self.size))
        self._data = data
        curr_offset = self.elf.io.tell()
        self.elf.io.seek(self.offset, os.SEEK_SET)
        self.elf.io.read(self.__data)
        self.elf.io.seek(curr_offset, os.SEEK_SET)
    
    def del_data(self):
        del self._data
        
    #use property 
    data = property(get_data,set_data,del_data,'section data')

class ProgramHeader(object):
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


class Symbol(object):
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


class StringTable(object):
    def __init__(self, stream, offset, size):
        self.offset = offset
        stream.seek(offset)
        self.table = array('c', stream.read(size))
        self.max = len(self.table)
    
    def __getitem__(self, key):
        if (key >= self.max):
            raise ParseError('The required index is out of the table: (0x%x) '
                        '+%d (max=%d)' % (self.offset, key, self.max))
        i = self.table[key:].index('\x00') + key
        return self.table[key:i].tostring()
