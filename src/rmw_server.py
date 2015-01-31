#!/usr/bin/python

import time
import logging
import threading
import rpyc
import os
from subprocess import call
from util.daemon import Daemon
from reminders import *

logger = logging.getLogger('rmw_service')
handler = logging.FileHandler('/var/log/rmw/rmw_service.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RMWDaemon(Daemon):
    '''
    Sets up ports and logging of Rpyc services.
    Additionally, will daemonize the process if debugging is off
    '''
    def __init__(self, port = 18861, debug = False):
        Daemon.__init__(self, '/tmp/rmw.pid', debug)

        self.port = port;

    def run(self):
        from rpyc.utils.server import ThreadedServer
        t = ThreadedServer(RMWService, logger = logger, port = self.port)
        t.start()

class EventLoop(threading.Thread):
    ''' Thread that continually checks for reminder updates '''

    def __init__(self):
        threading.Thread.__init__(self)

        self.started = False
        self.reminders = []
        self.stop = threading.Event()

    def __len__(self):
        return len(self.reminders)
       
    def run(self):
        ''' Checks reminders in order with a 2 second interval '''
        logger.info('Starting event loop')

        while True and not self.stop.isSet():
            for reminder in self.reminders:
                if reminder.handle():
                    self.reminders.remove(reminder)
                    logger.info('Completed and removed reminder')

            self.stop.wait(2)

    def get_reminders(self):
        return self.reminders

    def clear(self):
        self.reminders = []

    def add_reminder(self, reminder):
        self.reminders.append(reminder)

class RMWService(rpyc.Service):
    '''
    An Rpyc service that keeps track of a list of tasks, where each task
    is a check for updates (err, resolution, status change) to existing
    reminders.
    '''
    
    jobs = EventLoop()

    def __init__(self, conn):
        ''' 
        Creates a single class Event Loop to keep track of reminders 
        TODO: Fix and prevent the creation of multiple threads from multiple
        Service processes
        '''
        if not self.jobs.started:
            self.jobs.setDaemon(True)
            self.jobs.start()
            self.jobs.started = True
        
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def exposed_file_reminder(self, flags, target):
        ''' Creates a reminder pertaining to a file '''
        reminder = FileReminder(logger, flags, target)
        self.jobs.add_reminder(reminder)
        logger.info('Reminder set: ' + str(reminder))

        return str(reminder)

    def exposed_show(self):
        ''' Returns a formatted string of all open orders'''

        if (len(self.jobs) == 0):
            return 'No reminders set yet.'

        res = ''
        index = 1
        for reminder in self.jobs.get_reminders():
            res += '{}. {}'.format(index, reminder)

        return res

    def exposed_clear(self, index = None):
        ''' 
        If index is not set, clears the entire list of reminders to check for.
        Otherwise, remove the reminder at index (index - 1)
        '''
        if index:

            if index <= len(self.jobs) and index > 0:
                del self.jobs.reminders[index - 1]
                return 'Reminder {} cleared'.format(index)

            return 'Not a valid reminder index'

        self.jobs.clear()
        return 'All reminders cleared'
