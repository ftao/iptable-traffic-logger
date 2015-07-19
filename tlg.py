#!/usr/bin/env python
'''
Usage: 
  tlg.py enable  <port>
  tlg.py disable <port> 
  tlg.py show    <port>

Options:

'''

import docopt
import shlex
import subprocess
import iptc
from collections import defaultdict
IPTABLES="/sbin/iptables"

def set_port(port, flag):
    action = '-A' if flag else '-D'
    rule = [
        "%s %s INPUT  -p tcp --dport %s" %(IPTABLES, action, port),
        "%s %s OUTPUT -p tcp --sport %s" %(IPTABLES, action, port)
    ]
    for cmd in  rule:
        subprocess.call(shlex.split(cmd))

def view_port(port):
    table = iptc.Table(iptc.Table.FILTER)
    table.refresh()
    in_chain = iptc.Chain(table, 'INPUT')
    out_chain = iptc.Chain(table, 'OUTPUT')
    result = defaultdict(lambda : {'in' : 0, 'out' : 0})
    for rule in in_chain.rules:
        for match in rule.matches:
            (packets, bytes) = rule.get_counters()
            result[(match.name, match.dport)]['in'] += bytes
            #print 'in', packets, bytes, match.name, match.dport

    for rule in out_chain.rules:
        for match in rule.matches:
            (packets, bytes) = rule.get_counters()
            result[(match.name, match.sport)]['out'] += bytes
            #print 'out', packets, bytes, match.name, match.sport

    for (name, port),value in result.items():
        print name, port, value['in'], value['out']

def main():
    args = docopt.docopt(__doc__)
    if args['enable']:
        set_port(args['<port>'], True)
    elif args['disable']:
        set_port(args['<port>'], False)
    elif args['show']:
        view_port(args['<port>'])

if __name__ == "__main__":
    main()
