rmw (Remind Me When)
==

A service that uses RPC commands to set reminders for certain events.

## Status

NOT READY FOR PRODUCTION

## Dependencies

pip

rpyc

## Usage

rmw file -gt 3000 log.txt (Remind me when log.txt is greater than 3KB)

rmw show (Show all open reminders)

rmw clear -n 1 (Clears the reminder at index 1)

## TODO:

#### General

allow pip build and install

find another way to do notifications besides 'wall'

port configurations

### Features

rmw file -lt 3000 log.txt (Remind me when log.txt is less than 3MB)

rmw process -c someprocess (Remind me when someprocess is closed)

rmw process -o someprocess (Remind me when someprocess is open)

rmw time -a 201501011159 (Remind me when the time is past 1/1/15 11:59)

rmw time -e 1000 (Remind me when 1000 seconds have elapsed)
