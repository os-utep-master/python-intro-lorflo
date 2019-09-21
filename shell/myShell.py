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
    #ps = os.environ['PS1']
    inp = input( os.getcwd() + "$ ")
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
        if len(args) >= 2:
            for arg in range(len(args)):
                if arg == len(args):
                    break
                if args[arg] == ">":
                    newCHPID = os.fork()
                    if newCHPID == 0:
                        os.close(1)
                        fd = open( args[arg +1],"w+")
                        sys.stdout = fd
                        os.set_inheritable(1, True)
                        exe(args[arg -1])
                        os.close(fd)
                    else:
                        os.wait()
                    continue
                elif args[arg] == "<":
                    newCHPID = os.fork()
                    if newCHPID == 0:
                        os.close(0)
                        fd = open( args[arg - 1],"w+")
                        sys.stdin = fd
                        os.set_inheritable(0, True)
                        exe(args[arg + 1])
                        os.close(0)
                    else:
                        os.wait()
                    continue
                elif args[arg] == "|":
                    (pr,pw) = os.pipe()
                    for f in (pr, pw):       #setting and remeber ing pipe fd's
                        os.set_inheritable(f, True) 
                    newCHPID = os.fork()
                    if newCHPID == 0:
                        os.close(1)          #close stdout
                        os.dup(pr)           # new stdout is pipe input
                        exe(args[arg -1])
                        os.close(pr)
                    else:
                        os.wait()
                        os.close(0)          #close stdin
                        os.dup(pw)           #new stdin is pipe out
                        exe(args[arg + 1])
                        os.close(pw)
                    continue
        else:               
            exe(args[0])
            

    elif child_pid < 0:
        os.write(2, ("Program terminated with exit code %d.\n" % rc).encode())
        sys.exit(2)

    else:
        os.wait()
    
        