import sys
from subprocess import Popen, PIPE

def main():
    if len(sys.argv) > 2:
        raise Exception('Only argument should be log file')
    ff = sys.argv[1]

    #make ps for logger program
    logps = Popen(['python', 'logger.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')
    #make ps for encryption program
    encps = Popen(['python', 'encrypt.py'], stdout=sys.stdout, stdin=PIPE, encoding='utf8')

    history = []
    print('Please enter a command:')

    #TODO: include 'help' functionality
    #TODO: include a menu that shows possible commands
    #NOTE: history should prepend, and then only show recent 20
    #TODO: history should remove stuff older than 20
    for line in sys.stdin:
        line = line[:-1] #the 'better' approach is probably still using rstrip
        if line == 'quit':
            #send QUIT to enc & log
            logps.stdin.write('QUIT')
            encps.stdin.write('QUIT')
            break
        elif line == 'password':
            print()
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
    for i in range(min(len(history), 20)): #min 20 bc no need to show entire history of mankind
        print(str(i+1) + '. ' + str(history[i]))


if __name__ == '__main__':
    main()