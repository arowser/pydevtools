#!/usr/bin/env python
#--------------------------------------------------------------
# Manage elf files 
#--------------------------------------------------------------

import StringIO
import os
import struct
import sys
from optparse import OptionParser
from devtools.elf import *

class ElfViewer(object):
    def __init__(self, elfobj):
        self.elfobj = elfobj 
    def display_elf_header(self):
        elfobj = self.elfobj
        print "Elf Header"
        print "Elf Class                        : %s" \
                                            % elfobj.header.elfclass
        print "Elf Data                         : %s" \
                                            % elfobj.header.elfdata
        print "Elf Version                      : %d, 0x%x" \
                % (elfobj.header.version,elfobj.header.version)
        #OS/ABI
        #ABI Version
        print "Type                             : %d, 0x%x" \
                        % (elfobj.header.type,elfobj.header.type)
        print "Machine                          : %s" \
                        % elfobj.header.machine
        print "Entry point address:             : %d, 0x%x"\
                        % (elfobj.header.entry,elfobj.header.entry)
        print "Start of program headers (offset): %d, 0x%x bytes" \
                    % (elfobj.header.ph_offset,elfobj.header.ph_offset)
        print "Start of section headers (offset): %d, 0x%x bytes" \
                    % (elfobj.header.sh_offset,elfobj.header.sh_offset)
        print "Flags:                           : %d, 0x%x" \
                        % (elfobj.header.flags,elfobj.header.flags)
        print "Size of this header:             : %d, 0x%x" \
                % (elfobj.header.header_size,elfobj.header.header_size)
        print "Size of program headers:         : %d, 0x%x" \
            % (elfobj.header.ph_entry_size,elfobj.header.ph_entry_size)
        print "Number of program headers:       : %d, 0x%x" \
                    % (elfobj.header.ph_count,elfobj.header.ph_count)
        print "Size of section headers:         : %d, 0x%x" \
            % (elfobj.header.sh_entry_size,elfobj.header.sh_entry_size)
        print "Number of section headers:       : %d, 0x%x" \
                    % (elfobj.header.sh_count,elfobj.header.sh_count)
        print "Section header string table index: %d, 0x%x" \
                    % (elfobj.header.shstrndx,elfobj.header.shstrndx)    

    def display_program_header(self):
        elfobj = self.elfobj
        if len(elfobj.prog_headers)<=0 :
            print "No Program Header"
        else :
            plural = 's' if len(elfobj.prog_headers)>1 else ' '
            plural = "Program Header %s" % plural    
            print plural
            print "Entry point address:             : 0x%x"\
                                                %elfobj.header.entry
        
            print "Type Offset VirtAddr PhysAddr "\
                    "FileSiz MemSiz Flg Align"
        
            strfmt = "0x%x  0x%08x     0x%08x       0x%08x"\
                         " 0x%08x    0x%08x    0x%x  0x%08x"
        
            for phr in elfobj.prog_headers :    
                  print strfmt % \
                    (phr.type, phr.offset, phr.vaddr, phr.paddr, 
                     phr.filesz, phr.memsz, phr.flags, phr.align)

        def display_program_header(self):
            pass

if __name__ == '__main__':
    try:
        usage = 'Usage: %prog [options]\n'\
                '  Manage Elf files'
        optparser = OptionParser(usage=usage)
        optparser.add_option('-e', '--elfheader', dest='elfhdr',
                             action='store_true',
                             help='Show ELF header')
        optparser.add_option('-l', '--program-headers', dest='phdr',
                             action='store_true',
                             help='Show Program header')
        optparser.add_option('-S', '--sections-headers', dest='shdr',
                             action='store_true',
                             help='Show Program header')
        optparser.add_option('-d', '--debug', dest='debug',
                             action='store_true',
                             help='show debug information')
        (options, args) = optparser.parse_args(sys.argv[1:])
         
        try:
            infile = open(args[0], 'r') or sys.stdin
        except IOError, e:
            raise AssertionError('Ivalid input file: %s' % str(e))
        
        #build ELF object from infile
        try :
            elfobj = ELF(infile)
            elfviewer = ElfViewer(elfobj)
            
            line_needed = False
            
            if options.elfhdr is True :
                elfviewer.display_elf_header()
                line_needed = True
                
            if options.phdr is True :
                if line_needed is True : print "" 
                elfviewer.display_program_header()
                line_needed = True
                
            if options.shdr is True :
                if line_needed is True : print ""
                elfviewer.display_section_header()
                
                
        except ParseError, e:
            raise AssertionError("Invalid Elf File Error: %s" % str(e))

    except AssertionError , e:
        print >> sys.stderr, "Error: %s" % e
        exit(-1)