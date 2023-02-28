import sys

def main():
    if len(sys.argv) > 2:
        raise Exception('Only argument should be log file')
    ff = sys.argv[1]

    #make ps for logger program
    #make ps for encryption program

    print('Exiting now --')

if __name__ == '__main__':
    main()