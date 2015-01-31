import logging
import os
from subprocess import call

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
    def __init__(self, logger, flags, target):
        self.logger = logger
        self.target = target
        self.flags = flags

    def __str__(self):
        total = '{} for {}'.format(type(self).__name__, self.target)
        
        if self.flags != None:
            total += ' with ' + str(self.flags)

        return total

    def handle(self):
        return False

    def success(self, target, quality, value):
        if value != None:
            to_call = "echo \'Reminder for {}: {} {}\' | wall".format(
                    self.target, quality, value)
        else:
            to_call = "echo \'Reminder for {}: {}\' | wall".format(
                    self.target, quality)

        call(to_call, shell=True) 

        return True

class FileReminder(Reminder):

    def __init__(self, logger, flags, target):
        Reminder.__init__(self, logger, flags, target)

    def handle(self):
        if self.flags != None:
            option, value = self.flags

            if option == 'sizegt' or option == 'sizelt':
                try:
                    size = os.path.getsize(self.target)

                    if size > int(value) and option == 'sizegt':
                        return self.success(self.target, 'is greater than', value)

                    elif size < int(value) and option == 'sizelt':
                        return self.success(self.target, 'is less than', value)

                except Exception, e:
                    logger.error(e)

        elif os.path.isfile(self.target):

            return self.success(self.target, 'has been created', None)

        return False

class ProcessReminder(Reminder):

    processes = []

    def __init__(self, logger, flags, target):
        Reminder.__init__(self, logger, flags, target)

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

