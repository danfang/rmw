#!/usr/bin/python

import threading
import rpyc
import os

class RMWClient(object):
    def file_reminder(self, flags, files):
        try:
            c = rpyc.connect("localhost", 18861)
            total = ''

            for file_name in files:
                file_name = os.path.abspath(file_name)
                total += 'Created ' + c.root.file_reminder(flags, file_name) + '\n'

            return total

        except Exception, e:
            print e
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


