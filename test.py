from netfilterqueue import NetfilterQueue
from scapy.all import *
import time
from collections import namedtuple
import MySQLdb

# global dictionary to store live connections
conns={}
# and dictionary to store DNS lookups make (in case of interest)
dns={}

def get_conn_details(pkt):
    # format of scapy packet data structure is discussed here:
    # https://thepacketgeek.com/scapy-p-04-looking-at-packets/
    scapy_pkt = IP(pkt.get_payload())
    #print scapy_pkt.summary()
    #print scapy_pkt.show()
    # extract the src address/port and dest address/port of the new connection
    c=namedtuple('pkt',['src', 'sport', 'dst', 'dport', 'dns_query', 'dns_ans'])
    c.src = scapy_pkt[IP].src
    c.dst = scapy_pkt[IP].dst
    if (scapy_pkt.haslayer(TCP)):
        c.proto = 'TCP'
        c.sport = scapy_pkt[TCP].sport
        c.dport = scapy_pkt[TCP].dport
    elif (scapy_pkt.haslayer(UDP)):
        c.proto = 'UDP'
        c.sport = scapy_pkt[UDP].sport
        c.dport = scapy_pkt[UDP].dport
    # there's also ICMP etc ?
    c.dns_query=''
    c.dns_ans=''
    if (scapy_pkt.haslayer(DNS)):
        c.dns_query = scapy_pkt[DNS].qd.qname
        if (scapy_pkt[DNS].ancount > 0):
           # we have a DNS answer in this packet
           for i in range(scapy_pkt[DNS].ancount):
              ans = scapy_pkt[DNSRR][i]
	      print ans.type, ans.rdata
              if ans.type==1 or ans.type==28: # 1 is A, 28 is AAAA
                 c.dns_ans = ans.rdata 
                 break  # we use the first one
        print scapy_pkt.show()
    #print('%s %s:%d %s:%d %s' % (c.proto,c.src,c.sport,c.dst,c.dport,c.dns_query))
    # unique id for this connection.  can be split on the spaces to recover the connectiond details
    # we check with src and dest flipped to lump forward and reverse 
    # directions together
    conn_id_rev = c.proto+' '+c.dst+' '+str(c.dport)+' '+c.src+' '+str(c.sport)
    if (conn_id_rev in conns): 
       return (conn_id_rev, c)
    conn_id = c.proto+' '+c.src+' '+str(c.sport)+' '+c.dst+' '+str(c.dport)
    return (conn_id, c)

def log_new(pkt):
    # log the time when connection started and initialise packet count
    # for this connection
    (conn_id, c) = get_conn_details(pkt)
    print('NEW: %s %s:%d %s:%d' % (c.proto,c.src,c.sport,c.dst,c.dport))
    conns[conn_id] = [time.time(),'open',0] 
    pkt.accept()

def log_close(pkt):
    # log end of a connection
    (conn_id,c) = get_conn_details(pkt)
    conns[conn_id][1]='closed'
    print('CLOSED: %s %s:%d %s:%d count=%d' % (c.proto,c.src,c.sport,c.dst,c.dport,conns[conn_id][2]))
    pkt.accept()

def log_pkt(pkt):
    # log packets during body of connection
    # note: this is also called for DNS packets and for TCP/UDP packets
    # from before this script was run (so with no entry in conns[], so we
    # need to check for packets which are not in conns[]
    (conn_id,c) = get_conn_details(pkt)
    if conn_id in conns: # pkt from existing connection
       conns[conn_id][2] += 1 # increase pkt count
       print('PKT: %s %s:%d %s:%d count=%d' % (c.proto,c.src,c.sport,c.dst,c.dport,conns[conn_id][2]))
    elif (len(c.dns_query)>0): #DNS
       dns[c.dns_query] = [time.time(),c.dns_ans] 
       print ("DNS %s %s" % (c.dns_query,c.dns_ans)) 
    else: # stray packet outside of a connection, start a new connection
       conns[conn_id] = [time.time(),'open',0]
       print('STRAY: %s %s:%d %s:%d' % (c.proto,c.src,c.sport,c.dst,c.dport))
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, log_new, 100)
nfqueue.bind(2, log_close, 100)
nfqueue.bind(3, log_pkt, 100)

try:
    nfqueue.run()  # use nfqueue.run(False) to make this non-blocking
except KeyboardInterrupt:
    print('done.')

nfqueue.unbind()
