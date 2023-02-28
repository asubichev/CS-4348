import sys
import re

def main():
    passkey = ''
    for line in sys.stdin:
        result = [None, None]
        msg = line.split(" ", 1) #msg[0] = cmd, msg[1] = arg
        #TODO: make cmd accept anycase
        cmd = msg[0]
        if cmd.rstrip() == 'QUIT':
            break
        arg = msg[1].upper().rstrip() #to get rid of possible newline after argument
        if not re.fullmatch('[A-Z]+', arg):
            result = [-1, 'Argument not included']

        
        if result[0] != -1 and cmd == 'PASSKEY':
            if re.fullmatch('[A-Z]*', arg):
                passkey = msg[1]
                result = [0, '']
            else:
                result = [-1, '']
        elif cmd == 'ENCRYPT':
            result = encrypt(arg, passkey)
        elif cmd == 'DECRYPT':
            result = decrypt(arg, passkey)

        if result[0] == -1:
            print('ERROR ' + result[1])
        else:
            print('RESULT ' + result[1])
    #program end

#will return encrypted key, or return error
#returns list with exit code and string, where arr[0] == -1 is an error, and arr[0] == 0 is success
def encrypt(msg, key):
    if key == '': return [-1, 'Password not set']

    #first, make key as long as msg
    #next, iterate through msg and key together to find enc string
    ogkeylen = len(key)
    if len(msg) > ogkeylen:
        key = (len(msg) // ogkeylen) * key
        for kk in range(len(msg) - len(key)):
            key += key[kk]
    
    outputstr = ''
    for i in range(len(msg)):
        #number of characters to shift
        nmshift = ord(key[i]) - 65
        newpos = ord(msg[i]) - 65 + nmshift
        if newpos > 26: newpos -= 26
        newchar = chr(newpos + 65)
        outputstr += newchar
    
    return [0, outputstr]


#will return decrypted key, or return error
def decrypt(msg, key):
    if key == '': return [-1, 'Password not set']

    #make key as long as message again
    ogkeylen = len(key)
    if len(msg) > ogkeylen:
        key = (len(msg) // ogkeylen) * key
        for kk in range(len(msg) - len(key)):
            key += key[kk]

    #reverse steps of encryption
    outputstr = ''
    for i in range(len(msg)):
        nmshift = ord(key[i]) - 65
        newpos = ord(msg[i]) - 65 - nmshift
        if newpos < 0: newpos += 26
        newchar = chr(newpos + 65)
        outputstr += newchar

    return [0, outputstr]

if __name__ == "__main__":
    main()