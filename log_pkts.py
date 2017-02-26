from collections import namedtuple
import datetime
from geoip import geolite2
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
    SYN = 0x02
    FIN = 0x01
    RST = 0x04
    scapy_pkt = IP(pkt.get_payload())

    # extract the src address/port and dest address/port of the new connectiontc
    c=namedtuple('pkt',['src', 'sport', 'dst', 'dport', 'dns_query', 'dns_ans','timestmp', 'tcp_flag', 'scountry', 'dcountry'])
    c.src = scapy_pkt[IP].src
    c.dst = scapy_pkt[IP].dst
    if (scapy_pkt.haslayer(TCP)):
        c.proto = 'TCP'
        c.sport = scapy_pkt[TCP].sport
        c.dport = scapy_pkt[TCP].dport

        if scapy_pkt[TCP].flags == SYN: c.tcp_flag = 'SYN'
        elif scapy_pkt[TCP].flags == FIN: c.tcp_flag = 'FIN'
        elif scapy_pkt[TCP].flags == RST: c.tcp_flag = 'RST'
        else: c.tcp_flag = scapy_pkt[TCP].flags
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

    # get timestamp
    epoch_time = scapy_pkt.time
    c.timestmp = datetime.datetime.fromtimestamp(epoch_time) #.strftime('%c')

    # get countries
    slocation = geolite2.lookup(c.src)
    if slocation is not None:
        c.scountry = slocation.country
    else:
        c.scountry = "NULL"

    dlocation = geolite2.lookup(c.dst)
    if dlocation is not None: #print geolite2.lookup(c.dst)
        c.dcountry = dlocation.country
    else:
        c.dcountry = 'NULL'

    # unique id for this connection.  can be split on the spaces to recover the connection details
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
        update_pkt_count(pkt_info, conns[c_id][2])

    # Add new connection to conns and database
    # Note: not checking for SYN value, as connection is new
    else:
        conns[c_id] = [time.time(),'open',0]
        add_to_db(pkt_info, 'new', 0)

    # Check if end of TCP connection
    if pkt_info.proto == 'TCP' and (pkt_info.tcp_flag == RST or pkt_info.tcp_flag == FIN):
        add_to_db(pkt_info, 'closed', conns[c_id][2])

    pkt.accept()


def add_to_db(pkt_info, status, pkt_count):
    if pkt_info.proto == "TCP":
        sql = ("INSERT INTO packet_info (`id`,`proto`, `srcIP`, `sport`, `destIP`, `dport`, `conn_status`, `dns_query`,`timestmp`, `pkt_count`, `s_country`, `d_country`, `tcp_flag`)"
               "VALUES (NULL, '%s','%s','%s','%s','%s','%s','%s','%s', '%d', '%s', '%s', '%s')" \
                % (pkt_info.proto, pkt_info.src, pkt_info.sport, pkt_info.dst, pkt_info.dport, status, pkt_info.dns_query, pkt_info.timestmp, pkt_count, pkt_info.scountry, pkt_info.dcountry, pkt_info.tcp_flag))

    else:
        sql = ("INSERT INTO packet_info (`id`,`proto`, `srcIP`, `sport`, `destIP`, `dport`, `conn_status`, `dns_query`,`timestmp`, `pkt_count`, `s_country`, `d_country`)"
               "VALUES (NULL, '%s','%s','%s','%s','%s','%s','%s','%s', '%d', '%s', '%s')" \
                % (pkt_info.proto, pkt_info.src, pkt_info.sport, pkt_info.dst, pkt_info.dport, status, pkt_info.dns_query, pkt_info.timestmp, pkt_count, pkt_info.scountry, pkt_info.dcountry))

    try:
        cursor.execute(sql)
        db_conn.commit()
    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            print pkt_info.timestmp
        except IndexError:
            print "MySQL Error: %s" % str(e)
        db_conn.rollback()


def update_pkt_count(pkt_info, pkt_count):
    sql = ("UPDATE packet_info SET pkt_count = '%s' WHERE srcIP='%s' AND sport='%s' AND destIP='%s' AND dport='%s' ORDER BY `timestmp` DESC LIMIT 1" % (pkt_count,pkt_info.src, pkt_info.sport, pkt_info.dst, pkt_info.dport))
    try:
        cursor.execute(sql)
        db_conn.commit()
    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
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