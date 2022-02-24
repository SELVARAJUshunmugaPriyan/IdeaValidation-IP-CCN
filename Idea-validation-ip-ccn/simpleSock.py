#!/usr/bin/python3
from socket import *
from sys import argv
from time import sleep
from binascii import unhexlify

if __name__ == "__main__" :
    _cache   = {
        'nod': None, # Node number
        'ctn': {}    # Contains actual topic:value pair
    }

    try:
        _cache['nod'] = int(argv[1])
    except ValueError :
        raise Exception("Incorrect value for number of nodes")
    except IndexError :
        raise Exception("No value for number of nodes")

    l2_sock = socket(AF_PACKET, SOCK_RAW, ntohs(0x0003))
    l2_sock.bind(('wpan{}'.format(_cache['nod']), 0, PACKET_BROADCAST))
    l2_sock.setblocking(0)
    print('l2_socket established')
    rcvdPkt = None
    strng = None
    sendBuffer = b'\x41\xc8\x00\xff\xff\xff\xff'
    with open('/sys/class/net/wpan{}/address'.format(_cache['nod']), 'r') as f :
            strng = f.readline()
            strng = b''.join(unhexlify(x) for x in strng[:-1].split(':'))
            print(strng)

    while True:
        if _cache['nod'] == 1 :
            try:
                rcvdPkt = None
                rcvdPkt = l2_sock.recv(123)
            except BlockingIOError:
                print(rcvdPkt)
        
        if _cache['nod'] == 4 :
            print(l2_sock.send(sendBuffer + strng + bytes('ok', 'utf8')))
        sleep(1)