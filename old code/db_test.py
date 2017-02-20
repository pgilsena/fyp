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
    c=namedtuple('pkt',['src', 'sport', 'dst', 'dport', 'dns_query', 'dns_ans','timestmp','tcp_flag'])
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
    # there's also ICMP etc ?
    c.dns_query=''
    c.dns_ans=''
    if (scapy_pkt.haslayer(DNS)):
        c.dns_query = scapy_pkt[DNS].qd.qname
        if (scapy_pkt[DNS].ancount > 0):
           # we have a DNS answer in this packet
            for i in range(scapy_pkt[DNS].ancount):
                ans = scapy_pkt[DNSRR][i]
                #print ans.type, ans.rdata TODO
                if ans.type==1 or ans.type==28: # 1 is A, 28 is AAAA
                    c.dns_ans = ans.rdata
                    break  # we use the first one
        #print scapy_pkt.show()

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


def log_new(pkt,conn_id, c):
    # log the time when connection started and initialise packet count
    # for this connection
    #(conn_id, c) = get_conn_details(pkt)
    print('NEW: %s %s:%d %s:%d' % (c.proto,c.src,c.sport,c.dst,c.dport))
    conns[conn_id] = [time.time(),'open',0]
    write_to_db(conn_id, c, 'new')
    pkt.accept()

def log_close(pkt,conn_id, c):
    # log end of a connection
    #(conn_id,c) = get_conn_details(pkt)
    conns[conn_id][1]='closed'
    print('CLOSED: %s %s:%d %s:%d count=%d' % (c.proto,c.src,c.sport,c.dst,c.dport,conns[conn_id][2]))
    write_to_db(conn_id, c, 'closed')
    pkt.accept()


def log_pkt(pkt):
    # log packets during body of connection
    (conn_id,c) = get_conn_details(pkt)
    SYN = 0x02
    FIN = 0x01
    RST = 0x04

    # PKT: from existing connection, add to count
    if conn_id in conns:
       conns[conn_id][2] += 1

    elif (len(c.dns_query)>0): #DNS
        dns[c.dns_query] = [time.time(),c.dns_ans]
        print ("Resolved DNS %s %s" % (c.dns_query,c.dns_ans))

    # TCP PACKETS
    elif (c.proto == 'TCP'):
        if c.tcp_flag == SYN:
            log_new(pkt,conn_id,c)
        elif c.tcp_flag == RST or c.tcp_flag == FIN:
            log_close(pkt,conn_id,c)

    # NEW UDP CONNECTION: log packet
    elif c.proto == 'UDP' and conn_id not in conns:
        log_new(pkt,conn_id,c)

    # TODO: CLOSED UDP CONNECTION: log packet

    # PACKET NOT GRABBED
    else: # stray packet outside of a connection, start a new connection
        pdb.set_trace()
        #conns[conn_id] = [time.time(),'open',0]
        print('STRAY: %s %s:%d %s:%d' % (c.proto,c.src,c.sport,c.dst,c.dport))

    pkt.accept()


def write_to_db(conn_id, c, status):
    #(conn_id,c) = get_conn_details(pkt)
    #pdb.set_trace()

    if status == "closed":
        num_of_pkts = conns[conn_id][2]
        pkt_info = "INSERT INTO packet_info (`id`,`proto`, `srcIP`, `sport`, `destIP`, `dport`, `conn_status`, `dns_query`,`timestmp`, `pkt_count`) VALUES (NULL, '%s','%s','%s','%s','%s','%s','%s','%s','%d')" \
        % (c.proto, c.src, c.sport, c.dst, c.dport,status,c.dns_query,c.timestmp, num_of_pkts)

    else:
        pkt_info = "INSERT INTO packet_info (`id`,`proto`, `srcIP`, `sport`, `destIP`, `dport`, `conn_status`, `dns_query`,`timestmp`) VALUES (NULL, '%s','%s','%s','%s','%s','%s','%s','%s')" \
        % (c.proto, c.src, c.sport, c.dst, c.dport,status,c.dns_query,c.timestmp)

    try:
        cursor.execute(pkt_info)
        db_conn.commit()
    except:
        print "Error in inserting into database"
        db_conn.rollback()

try:
    db_conn = MySQLdb.connect('localhost', 'root', '', 'packets')
    cursor = db_conn.cursor()

except:
    print "Error in connecting to database"
    sys.exit(1)

nfqueue = NetfilterQueue()
nfqueue.bind(1, log_new, 100)
nfqueue.bind(2, log_close, 100)
nfqueue.bind(3, log_pkt, 100)

try:
    nfqueue.run()  # use nfqueue.run(False) to make this non-blocking
except KeyboardInterrupt:
    print('done.')

nfqueue.unbind()
db_conn.close()