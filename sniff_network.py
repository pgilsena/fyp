#!/usr/bin/python

import collections
import csv
import datetime
import jinja2
import logging
import os
import pandas
import pdb
from scapy.all import *
import sys

RECENT_IPS = deque([],20)
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = jinja2.Environment(
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

def parseInfo(writer):
    def subFunction(pkt):
        SYN = 0x02
        TCP_val = 6
        UDP_val = 17

        # TCP
        if pkt[IP].proto == TCP_val and pkt[TCP].flags == SYN:
            try:
                epoch_time = pkt.time
                time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
            except:
                time = 0
            info = [pkt[IP].dst, pkt[IP].proto, time]
            writer.writerow(info)
            RECENT_IPS.appendleft(info)
            df = queueToDataframe()
            show_unique_addresses(df)
    return subFunction

def queueToDataframe():
    q_to_list = list(RECENT_IPS)
    df = pandas.DataFrame(q_to_list)
    df.columns = ['dest_ip', 'proto', 'time']
    return df

def show_unique_addresses(df):
    output_file = 'recent_ips.html'
    context = {'ips': df['dest_ip'], 'proto':df['proto'], 'time':df['time']}

    with open(output_file, 'w') as f:
        html = render_template('ip_temp.html', context)
        f.write(html)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def main():
    with open('ips.csv', 'a') as f:
        writer = csv.writer(f)
        sniff(filter="ip", prn=parseInfo(writer)) # (and dst port ####), iface="wlp7s0"

if __name__ == "__main__":
    main()
