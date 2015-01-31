rmw (Remind Me When)
==

A service that uses RPC commands to set reminders for certain events.

## Status

NOT READY FOR PRODUCTION

## Dependencies

pip

rpyc

## Usage

```
rmw file foo.txt bar.txt other.txt (Remind me when log.txt is greater than 3KB)

Created FileReminder for foo.txt
Created FileReminder for bar.txt
Created FileReminder for other.txt

touch foo.txt

...

Broadcast Message from user@host (somewhere) at 22:12 ...                            
                                                                    
Reminder for foo.txt: has been created  

```

Other quick reminders

```
rmw file {-lt,-gt} 3000 log.txt (Remind me when log.txt is less than or greater than 3MB)
rmw process {-s} someprocess (Remind me when someprocess is started or stopped)
```

Control commands

```
rmw {start,stop,restart} 

...

rmw show
1. FileReminder for bar.txt
2. FileReminder for other.txt

...

rmw clear
All reminders cleared
```

## TODO:

#### General

allow pip build and install

find another way to do notifications besides 'wall'

add 'sticky' reminders

### Features

rmw process -o someprocess (Remind me when someprocess is open)

rmw time -a 201501011159 (Remind me when the time is past 1/1/15 11:59)

rmw time -e 1000 (Remind me when 1000 seconds have elapsed)
