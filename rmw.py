#!/usr/bin/python

import sys

from rmw_server import RMWDaemon
from rmw_cli import RMWClient


if __name__ == "__main__":
    ''' 
    The control module for both rmw's server and client 
    TODO: better argument parsing and error checking (find a way to better organize this)
    '''

    command = sys.argv[1]
    debug = False

    if '-debug' in sys.argv:
        debug = True
        sys.argv.remove('-debug')

    # commands that require the server
    if (command in ['start', 'stop', 'restart']):
        daemon = RMWDaemon(debug = debug)

        print("Remind me service: " + command)
        if command == 'start':
            print 'Debug mode: ' + str(debug)
            daemon.start()
        elif command == 'stop':
            daemon.stop()
        elif command == 'restart':
            daemon.restart()

        sys.exit(0)

    # commands that require the client
    elif (command in ['clear', 'show', 'process', 'file', 'time']) :
        cli = RMWClient()

        if command == 'clear':
            if len(sys.argv[2:]) == 2 and sys.argv[2] == '-n':
                print(cli.clear(int(sys.argv[3])))
            else:
                print(cli.clear())

        if command == 'show':
            print(cli.show())

        if command == 'file':
            print(cli.file_reminder(sys.argv[2:]))

