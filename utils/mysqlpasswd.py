#!/usr/bin/python
def mysql_hash_password(password):
    nr = 1345345333
    add = 7
    nr2 = 0x12345671

    for c in (ord(x) for x in password if x not in (' ', '\t')):
        nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF
        nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
        add= (add + c) & 0xFFFFFFFF

    return "%08x%08x" % (nr & 0x7FFFFFFF,nr2 & 0x7FFFFFFF)

import hashlib

def mysql_password(str):
    pass1 = hashlib.sha1(str).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return "*" + pass2.upper()
if __name__ == '__main__':
    passwd ="admin"
    print mysql_hash_password(passwd)
    print mysql_password(passwd)