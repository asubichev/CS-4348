import sys

def main():
    passkey = ''
    for line in sys.stdin:
        #print('Input processed')
        msg = line[:-1].split(" ", 1) #msg[0] = cmd, msg[1] = arg, [:-1] to not include "\n"
        #TODO: make cmd accept anycase
        cmd = msg[0]
        if cmd == 'QUIT':
            break
        #TODO: convert arg to all uppercase
        arg = msg[1]
        if cmd == 'PASSKEY':
            passkey = msg[1]
        elif cmd == 'ENCRYPT':
            encrypt(msg[1], passkey)
        elif cmd == 'DECRYPT':
            decrypt(msg[1], passkey)
    #program end

#will return encrypted key, or return error
def encrypt(msg, key):
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
    
    return outputstr


#will return decrypted key, or return error
def decrypt():
    print()

if __name__ == "__main__":
    main()