import sys
from subprocess import Popen, PIPE

def main():
    if len(sys.argv) > 2:
        raise Exception('Only argument should be log file')
    ff = sys.argv[1]

    #make ps for logger program
    logps = Popen(['python', 'logger.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')
    #make ps for encryption program
    encps = Popen(['python', 'encrypt.py'], stdout=PIPE, stdin=PIPE, encoding='utf8')

    history = []
    print('Please enter a command: ', end='')
    for line in sys.stdin:
        if line == 'quit':
            #send QUIT to enc & log
            break
        elif line == 'password':
            print()
        elif line == 'encrypt':
            print()
        elif line == 'decrypt':
            print()
        elif line == 'history':
            print()
        else:
            print('Invalid Commmand')
        print()

    print('Program Quit')

if __name__ == '__main__':
    main()