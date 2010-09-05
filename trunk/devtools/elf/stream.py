"""
Copyright (c) 2010, Cambridge Silicon Radio Ltd.
Written by Emilio Monti <emilmont@gmail.com>
"""
from sys import exit
from traceback import print_stack
from io import FileIO
from struct import unpack


class ParseError(Exception):
    pass


class ElfStream:
    BITS_32, BITS_64 = 1, 2
    LITTLE_ENDIAN, BIG_ENDIAN = 1, 2
    
    def set_bits(self, bits):
        if bits == ElfStream.BITS_32:
            pass
        elif bits == ElfStream.BITS_64:
            pass
        else:
            raise ParseError("Invalid elf class")
        self.bits = bits
    
    def set_endianness(self, endianness):
        if endianness == ElfStream.LITTLE_ENDIAN:
            self.u16 = self.ULInt16
            self.u32 = self.ULInt32
            self.u64 = self.ULInt64
            self.s16 = self.SLInt16
            self.s32 = self.SLInt32
            self.s64 = self.SLInt64
        elif endianness == ElfStream.BIG_ENDIAN:
            self.u16 = self.UBInt16
            self.u32 = self.UBInt32
            self.u64 = self.UBInt64
            self.s16 = self.SBInt16
            self.s32 = self.SBInt32
            self.s64 = self.SBInt64
        else:
            raise ParseError("Invalid data encoding")
        self.endianness = endianness
    
    def fatal(self, msg):
        print '@0x%x FatalError: %s\n' % (self.tell(), msg)
        print_stack()
        exit(2)

    def constant(self, length, value):
        const = self.read(length) 
        if const != value:
            raise ParseError('Wrong constant: %s != %s' % (const, value))

    def u08(self):
        return ord(self.read(1))
    
    def s08(self):
        return unpack('b', self.read(1))[0]
    
    def bytes(self, n):
        return map(ord, self.read(n))

    def skip(self, length):
        self.seek(length, 1)

    # Little Endian
    def ULInt16(self):
        return unpack('<H', self.read(2))[0]

    def ULInt32(self):
        return unpack('<I', self.read(4))[0]

    def ULInt64(self):
        return unpack('<Q', self.read(8))[0]

    def SLInt16(self):
        return unpack('<h', self.read(2))[0]

    def SLInt32(self):
        return unpack('<i', self.read(4))[0]

    def SLInt64(self):
        return unpack('<q', self.read(8))[0]

    # Big Endian
    def UBInt16(self):
        return unpack('>H', self.read(2))[0]

    def UBInt32(self):
        return unpack('>I', self.read(4))[0]

    def UBInt64(self):
        return unpack('>Q', self.read(8))[0]

    def SBInt16(self):
        return unpack('>h', self.read(2))[0]

    def SBInt32(self):
        return unpack('>i', self.read(4))[0]

    def SBInt64(self):
        return unpack('>q', self.read(8))[0]

    def load_entries(self, offset, n, Entry):
        entries = []
        if offset != 0:
            self.seek(offset)
            for i in range(n):
                entries.append(Entry(self, i))
        return entries


class ElfFile(FileIO, ElfStream):
    def __init__(self, path):
        FileIO.__init__(self, path, 'rb')
