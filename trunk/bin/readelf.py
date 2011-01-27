#!/usr/bin/env python
#--------------------------------------------------------------
# Manage elf files 
#--------------------------------------------------------------
from sys import argv, path
path.append('..')

import StringIO
import string
import os
import struct
import sys
import argparse
from bintools.elf import *

def transposed(lists, defval=0):
   if not lists: return []
   return map(lambda *row: [elem or defval for elem in row], *lists)

class ElfViewer(object):
    def __init__(self, elfobj):
        self.elfobj = elfobj 
    def display_elf_header(self):
        elfobj = self.elfobj
        print "Elf Header"
        print "Elf Class                        : %s" \
                                            % ELFCLASS[elfobj.header.elfclass]
        print "Elf Data                         : %s" \
                                            % ELFDATA[elfobj.header.elfdata]
        print "Elf Version                      : %d, 0x%x" \
                % (elfobj.header.version,elfobj.header.version)        
        #OS/ABI to implement ...
        #ABI Version to implment ...
        print "Type                             : %d, 0x%x" \
                        % (elfobj.header.type,elfobj.header.type)
        print "Machine                          : %s" \
                        % MACHINE[elfobj.header.machine]
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
    
    @staticmethod
    def display_iter_obj_formatted(tbl_config,iterobj):
        
        titles = [title[0] for title in tbl_config]
        records = []
        records.append(titles)
        for obj in iterobj :
            str_fields = []
            for fld in tbl_config :
                str_fields.append( fld[1] % getattr(obj, fld[2]))
            records.append(str_fields)
       
        #transpose lines to cols
        records = transposed(records)
        
        #create a table of normalised value        
        norm_records = []
        for col in records :
            max_len = 0
            for str_val in col:
                if type(str_val) == type('') and len(str_val) >= max_len:
                    max_len = len(str_val)
                    
            #max_len = max( len(str_val) for str_val in col)
            norm_fields = []
            for str_val in col :
                if (type(str_val) != type('')) :
                    str_val = ''
                norm_fields.append( string.ljust(str_val,max_len, ' '))
                
            norm_records.append(norm_fields)
        
        #transpose cols to lines
        norm_records = transposed(norm_records)
        
        #print lines
        for ln in norm_records :
            print "".join("%s " % v for v in ln)
        
        
    def display_program_header(self):
        elfobj = self.elfobj
        if len(elfobj.prog_headers)<=0 :
            print "No Program Header"
        else :
            plural = 's' if len(elfobj.prog_headers)>1 else ' '
            plural = "Program Header%s" % plural    
            print plural
            print "Entry point address:             : 0x%x"\
                                                %elfobj.header.entry

            tbl =   [ 
                    # name       #fmt     #field name
                    ['Type',    '0x%x'  , 'type'], 
                    ['Offset',  '0x%08x', 'offset'],
                    ['VirtAddr','0x%08x', 'vaddr'],
                    ['PhysAddr','0x%08x', 'paddr'],
                    ['FileSiz', '0x%08x', 'filesz'],
                    ['MemSiz',  '0x%08x', 'memsz'],
                    ['Flg',     '0x%08x', 'flags'],
                    ['Align',   '0x%08x', 'align'],
                    ]

            self.display_iter_obj_formatted(tbl,elfobj.prog_headers)

    def display_section_header(self):
        elfobj = self.elfobj
        if len(elfobj.sect_headers)<=0 :
            print "No Sections Header"
        else :
            plural = 's' if len(elfobj.sect_headers)>1 else ' '
            plural = "Section Header%s" % plural    
            print plural
            
            tbl =   [ 
                    # name       #fmt     #field name
                    ['Nr',      '%d',       'index'], 
                    ['Name',    '%s',       'name'],
                    ['type',    '0x%x',     'type'],
                    ['Addr',    '0x%08x',   'addr'],
                    ['Off',     '0x%08x',   'offset'],
                    ['Size',    '0x%08x',   'size'],
                    ['ES',      '0x%x',     'entsize'],
                    ['flg',     '0x%x',     'flags'],
                    ['Lk',      '0x%x',     'link'],
                    ['Inf',     '0x%x',     'info'],
                    ['Align',   '0x%x',     'addralign'],
                    ]

            self.display_iter_obj_formatted(tbl,elfobj.sect_headers)


if __name__ == '__main__':
    
    try:
        optparser = argparse.ArgumentParser(description='Read Elf Files.')
        optparser.add_argument('-e, --elfheader', dest='elfhdr',
                                 action='store_true',
                                 help='Show ELF header')
        optparser.add_argument('-l, --program-headers', dest='phdr',
                                 action='store_true',
                                 help='Show Program Table')
        optparser.add_argument('-S, --sections-headers', dest='shdr',
                                 action='store_true',
                                 help='Show Sections Table')
        optparser.add_argument('-d, --debug', dest='debug',
                                 action='store_true',
                                 help='show debug information')
        optparser.add_argument('filename', type=str,
                                 help='File to read')
        args = optparser.parse_args()
        try:
            infile = open(args.filename, 'r')
        except IOError, e:
            raise AssertionError('Ivalid input file: %s' % str(e))

        try :
            #build ELF object from infile
            elfobj = ELF(infile)
            
            #build ELF Viewer from elfobj
            elfviewer = ElfViewer(elfobj)
            
            line_needed = False
            
            if args.elfhdr is True :
                elfviewer.display_elf_header()
                line_needed = True
                
            if args.phdr is True :
                if line_needed is True : print "" 
                elfviewer.display_program_header()
                line_needed = True
                
            if args.shdr is True :
                if line_needed is True : print ""
                elfviewer.display_section_header()
                
                
        except ParseError, e:
            raise AssertionError("Invalid Elf File Error: %s" % str(e))

    except AssertionError , e:
        print >> sys.stderr, "Error: %s" % e
        exit(-1)