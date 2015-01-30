#!/usr/bin/python

import time
import logging
import threading
import rpyc
import os
from subprocess import call
from daemon import Daemon

class RMWDaemon(Daemon):
    def __init__(self, port = 18861):
        Daemon.__init__(self, '/tmp/rmw.pid')

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

    reminders = []
    started_jobs = False

    def __init__(self, conn):
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
        self.reminders.append({'command': 'file', 'type': r_type, 'value': value, 'target': target})
        return ('Added new reminder for {}: {} {}'.format(target, r_type, value))

    def exposed_show(self):
        if (len(self.reminders) == 0):
            return 'No reminders set!'

        res = ''
        index = 1
        for reminder in self.reminders:
            res += ('{}. When {} {} {}\n'.format(
                index, reminder['target'], reminder['type'], reminder['value']))

        return res

    def exposed_clear(self, index = None):
        if index:

            if index <= len(self.reminders) and index > 0:
                del self.reminders[index - 1]
                return 'Reminder {} cleared'.format(index)

            return 'Not a valid reminder index'

        self.reminders = []
        return 'All reminders cleared'


    class EventLoop(threading.Thread):

        def __init__(self, reminders):
            threading.Thread.__init__(self)
            self.reminders = reminders
            self.stop = threading.Event()
            
        def stop(self):
            self.stop.set()

        def run(self):
            while True and not self.stop.isSet():
                print('Checking status of reminders')
                for reminder in self.reminders:
                    self.handle_reminder(reminder)

                time.sleep(2)

        def handle_reminder(self, reminder):
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
