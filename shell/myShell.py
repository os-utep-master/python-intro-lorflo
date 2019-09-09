#! /usr/bin/env python3

import os, sys, re

#executes the given program
def exe(prog):
    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, prog)
        try:
            os.execve(program, [prog], os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass
    os.write(1,(prog + ":command not found\n").encode())
    sys.exit()

while (1):
    inp = input(os.getcwd() + "$ ")
    args = re.split('[ ]',inp)
    #print(args)

    if args[0] == "exit":
        sys.exit(0)
    if args[0] == "cd" and len(args) >= 2:
        try:
            os.chdir(args[1])
        except FileNotFoundError:             # ...expected
            os.write(1,(args[1] + " :file not found\n").encode())
        continue
    
    child_pid = os.fork()  
    if child_pid == 0:
        if args[0] == "ls":
            if len(args) >= 2:
                if args[1] == ">":
                    os.close(1)
                    fd = os.open( args[2], os.O_RDWR|os.O_CREAT )
                    sys.stdout = fd
                    os.set_inheritable(fd, True)
                    exe(args[0])
                    os.close(fd)
                if args[1] == "|":
                    pass
            exe(args[0])
            

    elif child_pid < 0:
        os.write(2, ("Program terminated with exit code %d.\n" % rc).encode())
        sys.exit(2)

    else:
        os.wait()
    
        