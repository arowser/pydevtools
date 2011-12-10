from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from queue import Queue
from os import read
from os.path import join
import select
import errno
from logging import debug, info, error, basicConfig, DEBUG #, INFO

from gdb.mi_parser import parse, Stream, Async, Result


class Debugger:
    def handle_stream_msg(self, msg):
        if msg.type == Stream.CONSOLE:
            info(msg.string)
        elif msg.type == Stream.TARGET:
            info('> %s' % msg.string)
        elif msg.type == Stream.ERROR_LOG:
            error(msg.string)
    
    def handle_async(self, msg):
        # These messages should change the state of the debugger to reflect
        # changes in the remote target
        pass


class GDB(Thread):
    PROMPT = '(gdb)'
    # '-tty', '/dev/pts/4', '--command=.gdbinit'
    CMD = ['gdb', '-q', '-nw', '-i', 'mi']
    MSG_EOF, MSG_TERM = 0, 1
    TERMINATOR = '(gdb) '
    
    def __init__(self, dir, prog, dbg):
        Thread.__init__(self)
        cmd = GDB.CMD + ['--cd=%s' % dir, join(dir, prog)]
        debug('[CMD] %s' % ' '.join(cmd))
        self.gdb = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        self.results_queue = Queue()
        self.token = 1
        self.dbg = dbg
    
    def send_cmd(self, cmd):
        cmd = '%d%s' % (self.token, cmd)
        debug('[TX] %s' % cmd)
        t = self.token
        self.gdb.stdin.write(cmd + '\n')
        self.token += 1
        return t
    
    def add_msg(self, msg):
        debug('[RX] %s' % msg)
        msg = parse(msg)
        if isinstance(msg, Stream):
            self.dbg.handle_stream_msg(msg)
        elif isinstance(msg, Async):
            self.dbg.handle_async(msg)
        elif isinstance(msg, Result):
            self.results_queue.put(msg)
    
    def get_result(self, t=None):
        msg = self.results_queue.get()
        if t is not None and msg.token != t:
            raise Exception("Expected token %d, received token %d." % (t, msg.token))
        return msg
    
    def sync_cmd(self, cmd, klass='done'):
        t = self.send_cmd(cmd)
        r = self.get_result(t)
        if r.klass != klass:
            raise Exception('Expected "%s" notification, received %s' % (klass, r.klass))
        return r.results
    
    def run(self):
        buffer = ''
        while True:
            try:
                select.select([self.gdb.stdout], [], [])
            except select.error as e:
                if e.args[0] == errno.EINTR:
                    continue
                raise
            
            data = read(self.gdb.stdout.fileno(), 1024)
            if data == "":
                if buffer:
                    raise Exception("Incomplete message: %s" % buffer)
                # self.results_queue.put(GDB.MSG_EOF)
                debug('[RX] EOF')
                break
            
            data = buffer + data
            buffer = ''
            
            msg = []
            for c in data:
                if c == '\n':
                    msg_line = ''.join(msg)
                    if msg_line == GDB.TERMINATOR:
                        # self.results_queue.put(GDB.MSG_TERM)
                        debug('[RX] (gdb)')
                    else:
                        self.add_msg(msg_line)
                    msg = []
                else:
                    msg.append(c)
            
            if msg:
                msg = ''.join(msg)
                if msg == GDB.TERMINATOR:
                    # self.results_queue.put(GDB.MSG_TERM)
                    debug('[RX] (gdb)')
                else:
                    buffer = msg
    
    def set(self, key, var):
        self.sync_cmd('-gdb-set %s %s' % (key, str(var)))
    
    def set_vars(self, vars):
        for key, value in vars.items():
            self.set(key, value)
    
    def init(self):
        self.set_vars({
            'confirm': 'off',
            'width': 0,
            'height': 0,
            'auto-solib-add': 'on',
            'stop-on-solib-events': 1,
        })
        self.sync_cmd('-interpreter-exec console echo')
        
        

if __name__ == '__main__':
    basicConfig(level=DEBUG, format='%(levelname)-8s %(message)s')
    dbg = Debugger()
    gdb = GDB('/home/em01/workspace/TestGDB', 'Debug/TestGDB', dbg)
    gdb.start()
    
    gdb.init()
    
    print('done')
    