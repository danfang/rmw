#!/usr/bin/python

import threading
import rpyc
import os

class RMWClient(object):
    def file_reminder(self, flags, target):
        try:
            c = rpyc.connect("localhost", 18861)
            target = os.path.abspath(target)
            return c.root.file_reminder(flags, target)
        except:
            return 'Unable to connect'

    def show(self):
        try:
            c = rpyc.connect("localhost", 18861)
            return c.root.show()
        except:
            return 'Unable to connect'

    def clear(self, index = None):
        try:
            c = rpyc.connect("localhost", 18861)
            return c.root.clear(index)
        except:
            return 'Unable to connect'


