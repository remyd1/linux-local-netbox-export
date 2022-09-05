#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import BoundedSemaphore
import subprocess
import json
import csv
from os.path import exists
import re

#IFACE_TYPE = {"ether": "1000base-t", }


def retrieve_json_for_netbox_fields():
    """
    basic function to retrieve appropriate fields for netbox
    """
    hostname = ""
    file_exists = exists("/sys/class/net/bonding_masters")
    bonds_name = []
    if file_exists:
        bond_file = open("/sys/class/net/bonding_masters",'r')
        bonds = bond_file.readlines()
        bond_file.close()
        bonds_name = bonds.split(" ")
    cmd = subprocess.Popen(["hostname", "-s"], stdout=subprocess.PIPE)
    hostname = cmd.stdout.read().rstrip()
    with open("interfaces.json",'r') as interface_json_file:
        interfaces_in_json = json.load(interface_json_file)
    interfaces = []
    for current_interface in interfaces_in_json:
        # loopback interface
        if current_interface['link_type'] == "loopback":
            continue
        cur_iface = {"name": "", "device": hostname, "label": "", "enabled": "", \
                     "type": "", "mgmt_only": "", "mtu": "", "mode": "", \
                     "mac_address": "", "wwn": "", "rf_role": "", \
                     "rf_channel": "", "rf_channel_frequency": "", \
                     "rf_channel_width": "", "tx_power": "", \
                     "description": "", "mark_connected": ""}
        
        cur_iface["name"] = current_interface['ifname']
        cur_iface["label"] = ""
        if current_interface['operstate'] == "UP":
            cur_iface["enabled"] = "True"
        else:
            cur_iface["enabled"] = "False"
        bond_found = False
        for bond_name in bonds_name:
            if re.search(bond_name, current_interface['ifname']):
                cur_iface["type"] = "lga"
            bond_found = True
        if not bond_found:
            cur_iface["type"] = current_interface['link_type']
        cur_iface["mgmt_only"] = "False"
        cur_iface["mtu"] = current_interface['mtu']
        cur_iface["mode"] = ""
        if "address" in current_interface:
            cur_iface["mac_address"] = current_interface['address']
        else:
            cur_iface["mac_address"] = ""
        cur_iface["wwn"] = ""
        cur_iface["rf_role"] = ""
        cur_iface["rf_channel"] = ""
        cur_iface["rf_channel_frequency"] = ""
        cur_iface["rf_channel_width"] = ""
        cur_iface["tx_power"] = ""
        cur_iface["description"] = ""
        cur_iface["mark_connected"] = ""
        # keeping the IPv4 address
        #cur_iface["ip"] = current_interface['addr_info'][0]['local'] + "/" + \
        #    current_interface['addr_info'][0]['prefixlen']
        interfaces.append(cur_iface)
    return interfaces

def write_to_csv(json_data):
    data_file = open('interfaces.csv', 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for iface in json_data:
        if count == 0:
            header = iface.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(iface.values())
    data_file.close()

if __name__ == "__main__":
    """
    Basic exporter interfaces    
    """
    fname = "interfaces.json"
    with open(fname,'w') as interface_json_file:
        subprocess.run(["ip", "-j", "a"], stdout=interface_json_file, stderr=subprocess.STDOUT)
    json_data = retrieve_json_for_netbox_fields()
    #debug purpose
    #print(repr(json_data))
    write_to_csv(json_data)
