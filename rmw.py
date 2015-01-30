#!/usr/bin/python

import sys

from rmw_server import RMWDaemon
from rmw_cli import RMWClient


if __name__ == "__main__":
    command = sys.argv[1]

    if (command in ['start', 'stop', 'restart']):
        daemon = RMWDaemon()

        print("Remind me service: " + command)
        if command == 'start':
            daemon.start()
        elif command == 'stop':
            daemon.stop()
        elif command == 'restart':
            daemon.restart()

        sys.exit(0)

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

