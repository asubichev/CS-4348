import sys
from datetime import datetime

def main():
    #towrite formats a log message
    #writelog takes formatted message and logs it
    towrite = processinput('START Logging Started.\n', tm = datetime.now()) 
    writelog(towrite)

    #TODO: make 'QUIT' accept anycase
    for line in sys.stdin:
        if 'QUIT' == line.rstrip():
            break
        #print('Input processed')
        towrite = processinput(line, tm = datetime.now())
        writelog(towrite)
    towrite = processinput('STOP Logging Stopped.\n', tm = datetime.now())
    writelog(towrite)
    #program end

def processinput(str, tm):
    timestamp = tm.strftime("%Y-%m-%d %H:%M") #reformat to get rid of seconds
    msg = str.split(" ", 1) #splits string 1 times at " " character
    if len(msg) == 1:
        raise Exception('Message has to have 1 command and 1 argument')
    out = timestamp + " [" + msg[0] + "] " + msg[1]
    return out

def writelog(message):
    f = open('./log.dat', 'a')
    f.write(message)
    f.close()
    

if __name__ == "__main__":
    main()