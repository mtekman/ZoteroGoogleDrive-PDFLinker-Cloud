#!/usr/bin/env python3

from sys import stderr
from datetime import datetime

class LogFile:

    @staticmethod
    def timestamp():
        return str(datetime.now()).split('.')[0]

    def __init__(self, caller):
        self.caller = caller
        
        self.__log = open('zg_pdf.log', 'a')
        self.__log.write("\n====== % s =======\n" % LogFile.timestamp())


    def log(self, *text, **keyw):
        silent = False
        if 'silent' in keyw:
            silent = True
            del keyw['silent']
        
        print( "[%s] -- %s -- " % (LogFile.timestamp(), self.caller), *text, **keyw, file=self.__log)

        if not silent:
            print( "[Info]", self.caller, *text, **keyw, file=stderr)

