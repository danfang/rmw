rmw
==

rmw is short for "remind me when".

It's a small service that uses RPC commands to set reminders for certain events.

## Status

In-progress

## Dependencies

pip

rpyc

## Installation

In-progress

## Usage

### Basic

```
rmw file foo.txt bar.txt other.txt 

Created FileReminder for foo.txt
Created FileReminder for bar.txt
Created FileReminder for other.txt

touch foo.txt

...

Broadcast Message from user@host (somewhere) at 22:12 ...                            
                                                                    
Reminder for foo.txt: has been created  

```

### Other quick reminders

```
rmw file {-lt,-gt} 3000 log.txt (Remind me when log.txt is less than or greater than 3MB)
rmw process {-s} someprocess (Remind me when someprocess is started or stopped)
```

### Control commands

```
rmw {start,stop,restart} (Control the port, daemonization, status of the rpc server)

...

rmw show
1. FileReminder for bar.txt
2. FileReminder for other.txt

...

rmw clear
All reminders cleared
```

## TODO

#### General

allow pip build and install

find another way to do notifications besides 'wall'

add 'sticky' reminders

### Features

rmw time -a 201501011159 (Remind me when the time is past 1/1/15 11:59)

rmw time -e 1000 (Remind me when 1000 seconds have elapsed)

rmw custom -e 500 -m "Don't forget to commit your changes!" (Remind me after 500 seconds to commit changes)
