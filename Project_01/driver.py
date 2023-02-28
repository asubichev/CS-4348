import sys

def main():
    if len(sys.argv) > 2:
        raise Exception('Only argument should be log file')
    ff = sys.argv[1]

    history = []
    print('Please enter a command: ', end='')
    for line in sys.stdin:
        if line == 'quit':
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

    #make ps for logger program
    #make ps for encryption program

    print('Exiting now --')

if __name__ == '__main__':
    main()