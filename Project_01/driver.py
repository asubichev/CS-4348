import sys
from subprocess import Popen, PIPE

def main():
    tempvar = len(sys.argv)
    if len(sys.argv) != 2:
        raise Exception('Log file as argument required')
    ff = sys.argv[1]

    # make ps for logger program
    logps = Popen(['python3', 'logger.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')
    # make ps for encryption program
    encps = Popen(['python3', 'encrypt.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')

    history = []
    print('Please enter a command:')

    #TODO: include 'help' functionality
    #TODO: include a menu that shows possible commands
    #TODO: history should remove stuff older than 20
    #TODO: all input()s should be validated
    #TODO: inputs should either all be on same line as prompt, or all be after newline
    #FIXME: what happens if you try to encrypt without setting a password?
    for line in sys.stdin:
        line = line[:-1] # the 'better' approach is probably still using rstrip
        if line == 'quit':
            # send QUIT to enc & log
            logps.stdin.write('QUIT\n')
            encps.stdin.write('QUIT\n')

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
            logps.stdin.write('PASSKEY New passkey set.\n') # i believe encryption program writes to logps, not driver.. T-T not sure
        elif line == 'encrypt':
            usrarg = usehistory(history)
            if usrarg == '':
                usrarg = input('Please enter string to encrypt: ')
                history.insert(0, usrarg)
            elif usrarg == None:
                print('Please enter a command:')
                continue
            else:
                #we pull this used string to most recent
                history.remove(usrarg)
                history.insert(0, usrarg)
            #FIXME: store encrypted string in history as well
            encps.stdin.write('ENCRYPT ' + usrarg + '\n')
            logps.stdin.write('ENCRYPT Message encrypted.\n')
        elif line == 'decrypt':
            usrarg = usehistory(history)
            if usrarg == '':
                usrarg = input('Please enter string to decrypt: ')
                history.insert(0,usrarg)
            elif usrarg == None:
                print('Please enter a command:')
                continue
            else:
                #we pull this used string to most recent
                history.remove(usrarg)
                history.insert(0, usrarg)
            #FIXME: store decrypted string in history as well
            encps.stdin.write('DECRYPT ' + usrarg + '\n')
            logps.stdin.write('DECRYPT Message decrypted.\n')
        elif line == 'history':
            printhistory(history)
        else:
            print('--Invalid Commmand--')
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