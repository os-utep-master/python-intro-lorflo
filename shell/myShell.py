#! /usr/bin/env python3

import os, sys, re

while (1):
    inp = input(os.getcwd() + "$ ")

    if inp == "exit":
        sys.exit()
    child_pid = os.fork()

    if child_pid == 0:
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
         program = "%s/%s" % (dir, inp)
         try:
             os.execve(program, [inp], os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
             pass
        os.write(1,(inp + ":command not found\n").encode())
        sys.exit()

    elif child_pid < 0:
        os.write(2, ("Program terminated with exit code %d.\n" % rc).encode())
        sys.exit(1)

    else:
        os.wait()
    
        