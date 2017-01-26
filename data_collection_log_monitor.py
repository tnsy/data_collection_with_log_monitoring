#!/usr/bin/env python

import sys, time, socket, os

if len(sys.argv) < 2:
    sys.exit('\nUSAGE: script <log_file_to_monitor> <output_file>\n\nEXITING\n')

##### FILL IN BELOW WITH DESIRED SETTINGS
commands_to_run = [''] #type in commands as a list: 'command_1', 'command_2'
time_interval = int() #in seconds
log_message = '' #type in what log message should break this from running
##### 

log_file = sys.argv[1]
output_file = sys.argv[2]
run = 0
switch = 0
border = '\n%s\n\n' % ('<>' * 25)
border1 = '\n%s\n\n' % ('=' * 50)
hostname = socket.gethostname()

def initial_check(log_file): 
    with open(log_file, 'r') as f:
        f.seek (0,2)
        return f.tell()

def check_file(log_file):
    global last_position
    with open(log_file, 'r') as f:
        f.seek(last_position)
        fo = f.readlines()
        f.seek (0,2)
        last_position = f.tell()
        return fo


last_position = initial_check(sys.argv[1])

of = open(output_file, 'w') 
of.write('Hostname: %s\n' % hostname)
of.write('Below file is an output of commands: %r\n' % commands_to_run)
of.write(border)

while switch == 0:
    run += 1
    current_time = time.ctime()
    universal_time = str(time.time())
    of.write('\tRun: %s' % run)
    of.write('\n\nCollected at: %s' % current_time)
    of.write('\nEpoch time: %s\n\n' % universal_time)
    for cmd in commands_to_run:
        c = os.popen('%s' % cmd)
        command = c.read()
        of.write(command)
        of.write(border1)
    of.write(border)
    time.sleep(time_interval)
    last_read = check_file(sys.argv[1])
    for i in last_read:
        if log_message in i:
            of.write('EXIT MESSAGE DETECTED:\n\n')
            of.write(i)
            switch = 1

of.close()
