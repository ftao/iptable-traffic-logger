#!/usr/bin/env python
'''
Send Accounting data to radius server
Usage: 
  send2radius.py <server> <secret> [options]

Options:
  --nas-ip NAS_IP          radius nas ip address
  --dict <dict_file>       radius dictionary file path [default: /etc/radiusclient/dictionary]

'''
import sys
import json
import hashlib
import docopt
import time
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

def main():
    args = docopt.docopt(__doc__)
    srv = Client(server=args['<server>'], secret=args['<secret>'],
                 dict=Dictionary(args['--dict']))
    inf = sys.stdin
    nas_ip = args['--nas-ip'] or '127.0.0.1'
    for line in inf:
        port,in_bytes,out_bytes = json.loads(line)
        data = {
            'username' : str(port),
            'in_bytes' : in_bytes,
            'out_bytes' : out_bytes,
        }
        send_acct(srv, data, nas_ip)


def send_acct(srv, data, nas_ip):
    username = data['username']
    session_id = hashlib.md5("%s-%s" % (username, time.time())).hexdigest()
    
    def send_start():
        req = srv.CreateAcctPacket()
        req['User-Name'] = data['username']
        req['NAS-IP-Address'] = nas_ip
        req['Acct-Session-Id'] = session_id
        req['Acct-Status-Type'] = 1  # Start

        reply = srv.SendPacket(req)
        if not reply.code == pyrad.packet.AccountingResponse:
            raise Exception("Unexpected response from RADIUS server for acct start")

    def send_stop():
        req = srv.CreateAcctPacket()
        req['User-Name'] = username
        req['NAS-IP-Address'] = nas_ip
        req['Acct-Session-Id'] = session_id
        req['Acct-Status-Type'] = 2  # Stop
        req['Acct-Output-Octets'] = data['out_bytes']
        req['Acct-Input-Octets'] = data['in_bytes']

        reply = srv.SendPacket(req)
        if not reply.code == pyrad.packet.AccountingResponse:
            raise Exception("Unexpected response from RADIUS server for acct stop")

    send_start()
    send_stop()


if __name__ == "__main__":
    main()
