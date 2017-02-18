from collections import namedtuple
import datetime
import logging
import MySQLdb
from netfilterqueue import NetfilterQueue
import pdb
from scapy.all import *
import time

# global dictionary to store live connections
conns={}
# and dictionary to store DNS lookups make (in case of interest)
dns={}
db_conn = None

def get_conn_details(pkt):
    scapy_pkt = IP(pkt.get_payload())

    # extract the src address/port and dest address/port of the new connection
    c=namedtuple('pkt',['src', 'sport', 'dst', 'dport', 'dns_query', 'dns_ans','timestmp', 'tcp_flag'])
    c.src = scapy_pkt[IP].src
    c.dst = scapy_pkt[IP].dst
    if (scapy_pkt.haslayer(TCP)):
        c.proto = 'TCP'
        c.sport = scapy_pkt[TCP].sport
        c.dport = scapy_pkt[TCP].dport
        c.tcp_flag = scapy_pkt[TCP].flags
    elif (scapy_pkt.haslayer(UDP)):
        c.proto = 'UDP'
        c.sport = scapy_pkt[UDP].sport
        c.dport = scapy_pkt[UDP].dport

    c.dns_query=''
    c.dns_ans=''
    if (scapy_pkt.haslayer(DNS)):
        c.dns_query = scapy_pkt[DNS].qd.qname
        if (scapy_pkt[DNS].ancount > 0):
           # we have a DNS answer in this packet
            for i in range(scapy_pkt[DNS].ancount):
                ans = scapy_pkt[DNSRR][i]
                #print ans.type, ans.rdata
                if ans.type==1 or ans.type==28: # 1 is A, 28 is AAAA
                    c.dns_ans = ans.rdata
                    break  # we use the first one

    epoch_time = scapy_pkt.time
    c.timestmp = datetime.datetime.fromtimestamp(epoch_time) #.strftime('%c')

    # unique id for this connection.  can be split on the spaces to recover the connectiond details
    # we check with src and dest flipped to lump forward and reverse
    # directions together
    conn_id_rev = c.proto+' '+c.dst+' '+str(c.dport)+' '+c.src+' '+str(c.sport)
    if (conn_id_rev in conns):
        return (conn_id_rev, c)
    conn_id = c.proto+' '+c.src+' '+str(c.sport)+' '+c.dst+' '+str(c.dport)
    return (conn_id, c)


def pkt_received(pkt):
    SYN = 0x02
    FIN = 0x01
    RST = 0x04

    (c_id, pkt_info) = get_conn_details(pkt)

    # Check if packet has already been logged in conns
    if c_id in conns:
        conns[c_id][2] += 1 # increase pkt counter for connection

    # Add new connection to conns and database
    # Note: not checking for SYN value, as connection is new
    else:
        conns[c_id] = [time.time(),'open',0]
        add_to_db(pkt_info, 'new', 0)

    # Check if end of TCP connection
    if pkt_info.proto == "TCP" and (pkt_info.tcp_flag == RST or pkt_info.tcp_flag == FIN):
        add_to_db(pkt_info, 'closed', conns[c_id][2])

    pkt.accept()


def add_to_db(pkt_info, status, pkt_count):
    sql = ("INSERT INTO packet_info (`id`,`proto`, `srcIP`, `sport`, `destIP`, `dport`, `conn_status`, `dns_query`,`timestmp`, `pkt_count`)"
           "VALUES (NULL, '%s','%s','%s','%s','%s','%s','%s','%s', '%d')" \
            % (pkt_info.proto, pkt_info.src, pkt_info.sport, pkt_info.dst, pkt_info.dport, status, pkt_info.dns_query, pkt_info.timestmp, pkt_count))

    try:
        cursor.execute(sql)
        db_conn.commit()
    except:
        print "Error in inserting into database"
        db_conn.rollback()




# Connect to database
try:
    db_conn = MySQLdb.connect('localhost', 'root', '', 'packets')
    cursor = db_conn.cursor()
except:
    print "Error in connecting to database"
    sys.exit(1)


nfqueue = NetfilterQueue()
nfqueue.bind(3, pkt_received, 100)

try:
    nfqueue.run()  # use nfqueue.run(False) to make this non-blocking
except KeyboardInterrupt:
    print('done.')

nfqueue.unbind()
db_conn.close()