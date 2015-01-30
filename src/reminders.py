import logging
import os
from subprocess import call

logger = logging.getLogger('rmw_service')
handler = logging.FileHandler('/var/log/rmw/rmw_service.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Reminder(object):
    '''
    Types of reminders:
        file [file_name]
            OPTIONS:
            None: Created
            -gt: Greater than (size)
            -lt size: Smaller than (size)
            -m: Modified
            -n age: Newer than (age)
            -o age: Older than (age)

        process [proc_name]
            OPTIONS:
            None: Created
            -s: Stopped
            -n age: Newer than (age)
            -o age: Older than (age)

        time []
            OPTIONS:
            -e secs: Elapsed (seconds)
            -a time: After (time)

        custom []
            OPTIONS:
            -e secs: Elapsed (secs)
                -m str: Optional message
            -a time: After (ttime)
                -m str: Optional message
    '''

    def __str__(self):
        return '{} for {}, with {}'.format(
                type(self).__name__, self.target, str(self.flags))

    def valid_flags(self, flags):
        return False

    def handle(self):
        return False

class FileReminder(Reminder):

    def __init__(self, flags, target):
        self.flags = []
        for flag in flags:
            self.flags.append(flag)
        self.target = target

    def valid_flags(self, flags):
        pass

    def handle(self):
        for flag in self.flags:
            option, value = flag

            if option == '-gt':
                try:
                    size = os.path.getsize(self.target)

                    if size > int(value):
                        call("echo \'rmw: {} size greater than {}\' | wall ".format(self.target, value), shell=True) 
                        return True
                except Exception, e:
                    logger.error(e)
        return False

class ProcessReminder(Reminder):

    def __init__(self, flags, target):
        Reminder.__init__(self, flags, target)

    def handle(self):
        pass

class TimeReminder(Reminder):

    def __init__(self, flags, target):
        Reminder.__init__(self, flags, target)

    def handle(self):
        pass

class CustomReminder(Reminder):

    def __init__(self, flags, target):
        Reminder.__init__(self, flags, target)

    def handle(self):
        pass

