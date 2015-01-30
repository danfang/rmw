#!/usr/bin/python

import time
import logging
import threading
import rpyc
import os
from subprocess import call
from daemon import Daemon

class RMWDaemon(Daemon):
    '''
    Sets up ports and logging of Rpyc services.
    Additionally, will daemonize the process if debugging is off
    '''
    def __init__(self, port = 18861, debug = False):
        Daemon.__init__(self, '/tmp/rmw.pid', debug)

        logger = logging.getLogger('rmw_service')
        handler = logging.FileHandler('/var/log/rmw/rmw_service.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        self.port = port;
        self.logger = logger

    def run(self):
        from rpyc.utils.server import ThreadedServer
        t = ThreadedServer(RMWService, logger = self.logger, port = self.port)
        t.start()

class RMWService(rpyc.Service):
    '''
    An Rpyc service that keeps track of a list of tasks, where each task
    is a check for updates (err, resolution, status change) to existing
    reminders.
    '''
    reminders = []
    started_jobs = False

    def __init__(self, conn):
        ''' 
        Creates a single class Event Loop to keep track of reminders 
        TODO: Fix and prevent the creation of multiple threads from multiple
        Service processes
        '''
        if not self.started_jobs:
            jobs = self.EventLoop(self.reminders)
            jobs.start()
            print('Starting event loop')
            self.started_jobs = True
        
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def exposed_file_reminder(self, r_type, value, target):
        ''' Creates a reminder pertaining to a file '''

        self.reminders.append({'command': 'file', 'type': r_type, 'value': value, 'target': target})
        return ('Added new reminder for {}: {} {}'.format(target, r_type, value))

    def exposed_show(self):
        ''' Returns a formatted string of all open orders'''

        if (len(self.reminders) == 0):
            return 'No reminders set!'

        res = ''
        index = 1
        for reminder in self.reminders:
            res += ('{}. When {} {} {}\n'.format(
                index, reminder['target'], reminder['type'], reminder['value']))

        return res

    def exposed_clear(self, index = None):
        ''' 
        If index is not set, clears the entire list of reminders to check for.
        Otherwise, remove the reminder at index (index - 1)
        '''
        if index:

            if index <= len(self.reminders) and index > 0:
                del self.reminders[index - 1]
                return 'Reminder {} cleared'.format(index)

            return 'Not a valid reminder index'

        # TODO: Fix this
        self.reminders = []
        return 'All reminders cleared'


    class EventLoop(threading.Thread):
        ''' Thread that continually checks for reminder updates '''

        def __init__(self, reminders):
            threading.Thread.__init__(self)
            self.reminders = reminders
            self.stop = threading.Event()
            
        def stop(self):
            ''' Stops the event loop '''

            self.stop.set()

        def run(self):
            ''' Checks reminders in order with a 2 second interval '''

            while True and not self.stop.isSet():
                print('Checking status of reminders')
                for reminder in self.reminders:
                    self.handle_reminder(reminder)

                time.sleep(2)

        def handle_reminder(self, reminder):
            ''' Handles the necessary tasks for any particular reminder '''

            print('Checking reminder: ' + str(reminder))
            if reminder['command'] == 'file':
                if reminder['type'] == '-gt':
                    target = reminder['target']
                    value = reminder['value']

                    try:
                        size = os.path.getsize(target)

                        if size > int(value):
                            call("echo \'rmw: {} size greater than {}\' | wall ".format(
                                target, value), shell=True)

                            self.reminders.remove(reminder)
                    except:
                        pass
