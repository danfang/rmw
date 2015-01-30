#!/usr/bin/python

import threading
import rpyc
import os

class RMWClient(object):
    def file_reminder(self, args):
        r_type, value, target = args
        target = os.path.abspath(target)
        c = rpyc.connect("localhost", 18861)
        return c.root.file_reminder(r_type, value, target)

    def show(self):
        c = rpyc.connect("localhost", 18861)
        return c.root.show()

    def clear(self, index = None):
        c = rpyc.connect("localhost", 18861)
        return c.root.clear(index)

