#!/usr/bin/python

"""
File based logging.
"""

import traceback
from datetime import datetime

def _caller(back = 3):
    return traceback.extract_stack(None, back)[0][2]

class Log(object):

    def __init__(self, logFile, debugMode = False):
        assert type(logFile) == str
        assert type(debugMode) == bool

        open(logFile, 'a').close()
        self.logFile = logFile
        self.debugMode = debugMode

    def _write(self, message, pad, caller):
        with open(self.logFile, 'a') as f:
            f.write('{date}: {pad}{caller} - {message}\n'.format(date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pad = pad, caller = caller, message = message))

    def write(self, message, pad = '', caller = None):
        c = caller if caller else _caller()

        self._write(message, pad, c)

    def debug(self, message):
        if self.debugMode:
            self.write(message, 5 * '#' + ' ', _caller())

    def error(self, message):
        self.write(message, 10 * '*' + ' ', _caller())

