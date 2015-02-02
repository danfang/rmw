#!/usr/bin/python

import sys
import argparse

from rmw_server import RMWDaemon
from rmw_cli import RMWClient

def main():
    ''' 
    The control module for both rmw's server and client 
    '''
    def start_daemon(args):
        if args.port != None:
            print 'Running on port ' + str(args.port)
            RMWDaemon(port = args.port, debug = args.debug).start()
        else:
            RMWDaemon(debug = args.debug).start()


    def stop_daemon(args):
        RMWDaemon(debug = args.debug).stop()
        print 'Reminder service stopped'

    def restart_daemon(args):
        status = 'Reminder service restarted'
        if args.port != None:
            RMWDaemon(port = args.port, debug = args.debug).restart()
            print status + ' on port ' + str(args.port)
        else:
            RMWDaemon(debug = args.debug).restart()
            print status

    def clear_reminders(args):
        cli = RMWClient()

        if args.index:
            print(cli.clear())
        else:
            print(cli.clear(index = args.index))

    def show_reminders(args):
        cli = RMWClient()
        print(cli.show())

    def file_reminder(args):
        cli = RMWClient()

        if args.sizegt:
            print(cli.file_reminder(('sizegt', args.sizegt), args.file))
        elif args.sizelt:
            print(cli.file_reminder(('sizelt', args.sizegt), args.file))
        else:
            print(cli.file_reminder(None, args.file))

    def process_reminder(args):
        cli = RMWClient()

        if args.stopped:
            print(cli.process_reminder(('stopped', True), args.process))
        elif args.newer:
            pass
        elif args.older:
            pass
        else:
            print(cli.process_reminder(None, args.process))
            pass

    def time_reminder(args):
        print args
        pass

    parser = argparse.ArgumentParser(prog='rmw')
    sp = parser.add_subparsers()

    # server side commands
    sp_start = sp.add_parser('start', help='Starts %(prog)s daemon')
    sp_start.set_defaults(func=start_daemon)

    sp_stop = sp.add_parser('stop', help='Stops %(prog)s daemon')
    sp_stop.set_defaults(func=stop_daemon)

    sp_restart = sp.add_parser('restart', help='Restarts %(prog)s daemon')
    sp_restart.set_defaults(func=restart_daemon)

    parser.add_argument('-d', '--debug', action='store_true',
            help='do not run the program as a daemon')
    
    parser.add_argument('-p', '--port', type=int,
            help='Choose what port the rmw service runs on')

    # client-side non reminders
    sp_show = sp.add_parser('show', help='Shows all open reminders')
    sp_show.set_defaults(func=show_reminders)

    sp_clear = sp.add_parser('clear', help='Clear all or specified open reminders')
    sp_clear.add_argument('-n', '--index', type=int, help='clear the reminder at ' +
            'the specified index')
    sp_clear.set_defaults(func=clear_reminders)

    # client-side reminders
    sp_file = sp.add_parser('file', help='set a reminder for a file')
    file_group = sp_file.add_mutually_exclusive_group()
    file_group.add_argument('-gt', '--sizegt', type=int, metavar='bytes')
    file_group.add_argument('-lt', '--sizelt', type=int, metavar='bytes')
    sp_file.add_argument('file', nargs='+')
    sp_file.set_defaults(func=file_reminder)

    sp_process = sp.add_parser('process', help='set a reminder for a process')
    process_group = sp_process.add_mutually_exclusive_group()
    process_group.add_argument('-s', '--stopped', action='store_true')
    process_group.add_argument('-n', '--newer', type=int, metavar='timestr')
    process_group.add_argument('-o', '--older', type=int, metavar='timestr')
    sp_process.set_defaults(func=process_reminder)
    sp_process.add_argument('process', nargs='+')

    sp_time = sp.add_parser('time', help='set a time-based reminder')
    time_group = sp_time.add_mutually_exclusive_group()
    time_group.add_argument('-e', '--elapsed', type=int, metavar='secs')
    time_group.add_argument('-a', '--after', type=int, metavar='secs')
    sp_time.set_defaults(func=time_reminder)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
