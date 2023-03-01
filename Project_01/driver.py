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
    #NOTE: history should prepend, and then only show recent 20
    #TODO: history should remove stuff older than 20
    #TODO: all input()s should be validated
    for line in sys.stdin:
        line = line[:-1] # the 'better' approach is probably still using rstrip
        #TODO: quit doesn't work if it's not the first command
        if line == 'quit':
            #send QUIT to enc & log
            logps.stdin.write('QUIT\n')
            encps.stdin.write('QUIT\n')
            break
        elif line == 'password':
            pkinp = usehistory(history)
            #usehistory will return empty string if user doesn't want to use history, or if history is empty
            if pkinp == '':
                pkinp = input('Please enter password: ')
                history.insert(0, pkinp) # don't store if history used
            encps.stdin.write('PASSKEY ' + pkinp + '\n')
            logps.stdin.write('PASSKEY' + ' New passkey set.\n') # i believe encryption program writes to logps, not driver.. T-T not sure
        elif line == 'encrypt':
            print()
        elif line == 'decrypt':
            print()
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
    choiche = input('Would you like to use history?\n1. Yes, I would\n2. No, I wouldn\'t\n') # newline is already stripped w input()
    if choiche == '1':
        printhistory(history)
        seli = input('Please indicate item number: ')
        #TODO: check if seli is an int
        return history[int(seli) - 1]
    if choiche == '2':
        return ''


if __name__ == '__main__':
    main()