import sys
from datetime import datetime

def main():
    for line in sys.stdin:
        if 'Quit' == line.rstrip():
            break
        print('Input processed')
        processinput(line, tm = datetime.now())
    print("Exit")

def processinput(str, tm):
    timestamp = tm.strftime("%Y-%m-%d %H:%M") #reformat to get rid of seconds
    

if __name__ == "__main__":
    main()