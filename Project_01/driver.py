import sys
import re
from subprocess import Popen, PIPE

def main():
    if len(sys.argv) != 2:
        raise Exception('Log file as argument required')
    filename = sys.argv[1]

    # make ps for logger program
    logps = Popen(['python3', 'logger.py', filename], stdout=PIPE, stdin=PIPE, encoding='utf8')
    # make ps for encryption program
    encps = Popen(['python3', 'encrypt.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')

    history = []
    print('Please enter a command:')
    
    for line in sys.stdin:
        line = line[:-1] # the 'better' approach is probably still using rstrip
        if line == 'quit':
            # send QUIT to enc & log
            logps.stdin.write('QUIT\n')
            logps.stdin.flush()
            encps.stdin.write('QUIT\n')
            encps.stdin.flush()

            # i'm not sure why i have to close these, but they prevent Broken Pipe error
            logps.stdin.close()
            encps.stdin.close()
            break
        elif line == 'password':
            usrarg = usehistory(history)
            # usehistory will return empty string if user doesn't want to use history, or if history is empty
            if usrarg == '':
                usrarg = input('Please enter password: ')
                # history.insert(0, pkinp) # don't store if history used, SIKE we don't even store passwords
            elif usrarg == None: # if user wants to not use history, but just go back
                print('Please enter a command:')
                continue
            encps.stdin.write('PASSKEY ' + usrarg + '\n')
            encps.stdin.flush()
            logps.stdin.write(encps.stdout.readline())
            logps.stdin.flush()
        elif line == 'encrypt':
            usrarg = usehistory(history)
            if usrarg == '':
                usrarg = input('Please enter string to encrypt: ').upper()
                history.insert(0, usrarg)
            elif usrarg == None:
                print('Please enter a command:')
                continue
            else:
                #we pull this used string to most recent
                history.remove(usrarg)
                history.insert(0, usrarg)
            encps.stdin.write('ENCRYPT ' + usrarg + '\n')
            encps.stdin.flush()
            output = encps.stdout.readline()
            if 'RESULT' in output: # encryption didn't return an error
                sprtstr = output.split(" ")
                if len(sprtstr) > 1:
                    history.insert(0, sprtstr[1].rstrip())
            logps.stdin.write(output)
            logps.stdin.flush()
        elif line == 'decrypt':
            usrarg = usehistory(history)
            if usrarg == '':
                usrarg = input('Please enter string to decrypt: ').upper()
                history.insert(0, usrarg)
            elif usrarg == None:
                print('Please enter a command:')
                continue
            else:
                #we pull this used string to most recent
                history.remove(usrarg)
                history.insert(0, usrarg)
            encps.stdin.write('DECRYPT ' + usrarg + '\n')
            encps.stdin.flush()
            output = encps.stdout.readline()
            if 'RESULT' in output:
                sprtstr = output.split(" ")
                if len(sprtstr) > 1:
                    history.insert(0, sprtstr[1].rstrip())
            logps.stdin.write(output)
            logps.stdin.flush()
        elif line == 'history':
            printhistory(history)
        else:
            print('--Invalid Commmand--')
        listcomp = []
        [listcomp.append(x) for x in history if x not in listcomp]
        history = listcomp # remove dupes
        print('Please enter a command:')

    print('Program Quit')

def printhistory(history):
    if len(history) == 0: 
        print('History Empty!')
        return ''
    print('History:')
    for i in range(min(len(history), 20)): # min 20 bc no need to show entire history of mankind
        print(str(i+1) + '. ' + str(history[i]))

def usehistory(history):
    if len(history) == 0: return ''
    choiche = input('Would you like to use history?\n1. Yes, I would\n2. No, I wouldn\'t\n3. Go back\n') # newline is already stripped w input()
    if choiche == '1':
        printhistory(history)
        seli = input('Please indicate item number: ')
        #TODO: check if seli is an int
        return history[int(seli) - 1]
    if choiche == '2':
        return ''
    elif choiche == '3':
        return None


if __name__ == '__main__':
    main()