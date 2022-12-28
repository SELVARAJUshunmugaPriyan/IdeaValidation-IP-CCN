#!/usr/bin/python3
import socket
import sys
#import time
import binascii
import logging
import datetime
import select
import random

def emptySocket(sock):
    # Remove the data present on the socket
    _input = [sock]
    while True:
        _inputReady, o, e = select.select(_input,[],[], 0.0)
        if not _inputReady.__len__(): 
            break
        for _sck in _inputReady:
            try:
                _sck.recv(123)
            except BlockingIOError:
                pass
    return

if __name__ == "__main__" :

    _cache   = {
        'nod': None,    # Node number
        'sat': False,   # Device Status
        'cnt': {},      # Contains actual topic:value pair
        'com': False,   # Start Flag
    }
    _rcvPkt = None
    _sndBfr = b'\x41\xc8\x00\xff\xff\xff\xff'   # Preceeding IEEE 802154 Broadcast Format
                                                # Incomplete without CRC trailer (avoided for prototyping)

    try:
        _cache['nod'] = int(sys.argv[1])
        _cache['_x'] = int(sys.argv[2])
        _cache['drp'] = int(sys.argv[4])
        _cache['x_x'] = _cache['_x'] * _cache['_x'] # Identifying the communicating node
        _cache['cnt']['{0:02d}'.format(_cache['x_x'])] = []
    except ValueError :
        raise Exception("Incorrect value for number of nodes")
    except IndexError :
        raise Exception("No value for number of nodes")
        
    if not _cache['nod'] :
        logging.basicConfig(
            filename='/home/wifi/Downloads/simple/Idea-validation-ip-ccn/log/wpan{}.log'.
                format(_cache['nod']),
            filemode='a',
            level=logging.INFO,
            format=("%(asctime)s-%(levelname)s-%(filename)s-%(lineno)d "
            "%(message)s"),
            datefmt='%d/%m/%Y %H:%M:%S'
        )

    l2_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    l2_sock.bind(('wpan{}'.format(_cache['nod']), 0, socket.PACKET_BROADCAST))
    l2_sock.setblocking(0)
    logging.info('l2_socket established')

    with open('/sys/class/net/wpan{}/address'.format(_cache['nod']), 'r') as f :
            _strng = f.readline()
            _strng = b''.join(binascii.unhexlify(x) for x in _strng[:-1].split(':'))
            _sndBfr += _strng                   # Appending Device MAC address

    if _cache['nod'] == _cache['x_x'] :
        logging.info(_cache['nod'])
        _cache['com'] = True
        _sndBfr += b'>' + bytes('{0:02d}'.format(_cache['x_x']), 'utf8') + b'>'

    try:
        if sys.argv[3] == 'a' :  # Adhoc or mesh
            _intermediateNodes = [0,1]
            for i in range(2,_cache['_x']):
                _intermediateNodes.append(_intermediateNodes[-1] + _cache['_x'] + 1)
            _intermediateNodes.append(_cache['x_x'])

            if _cache['nod'] in _intermediateNodes :
                _cache['sat'] = True
        else:
            _cache['sat'] = True
    except ValueError :
        raise Exception("Incorrect value for number of nodes")
    except IndexError :
        raise Exception("No value for number of nodes")

    logging.info(_cache['sat'])
    while True and _cache['sat'] :
        try:
            _rcvPkt = None
            if round(random.random() * 100) > _cache['drp'] :
                _rcvPkt = l2_sock.recv(123)
            emptySocket(l2_sock)
        except BlockingIOError:
            pass
        if _cache['com'] and round(random.random() * 100) > _cache['drp']: # Generating New content
            _sndBfr = _sndBfr[:19] + bytes(str(datetime.datetime.now()), 'utf8')
            _tBytes = l2_sock.send(_sndBfr)
            logging.debug("Total sent bytes {}".format(_tBytes))
        elif _rcvPkt :
            _top = _rcvPkt[16:18].decode('utf-8')
            _jmp = _rcvPkt[18:].decode('utf-8').split('>')
            _val = _jmp[-1]
            if _top in _cache['cnt'].keys() and _val not in _cache['cnt'][_top]:
                logging.info(_rcvPkt.__len__())
                logging.info(_jmp[:-1])
                logging.info(datetime.datetime.now() - datetime.datetime.strptime(_val, "%Y-%m-%d %H:%M:%S.%f")) # 2022-02-24 15:02:45.860661
                # Update cache if new value
                _cache['cnt'][_top].append(_val)
                _cache['cnt'][_top] = _cache['cnt'][_top][-20:]
                if _cache['nod'] and round(random.random() * 100) > _cache['drp'] :
                    _sndBfr = _sndBfr[:15] + _rcvPkt[15:19] + bytes('{0:02d}'.format(_cache['nod']), 'utf8') + b'>' + _rcvPkt[19:]
                    logging.debug(_sndBfr)
                    _tBytes = l2_sock.send(_sndBfr)
                    logging.debug("Total sent bytes {}".format(_tBytes))

        #time.sleep(0.001)