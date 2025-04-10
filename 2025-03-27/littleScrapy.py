#!/usr/bin/env python3
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp, sr1
import netifaces
from mac_vendor_lookup import MacLookup
import socket
import time
from datetime import datetime
from prettytable import PrettyTable

def get_default_interface():
    return netifaces.gateways()['default'][netifaces.AF_INET][1]

def get_device_analysis(mac, ip):
    analysis = {
        'device_type': "Unbekannt",
        'services': [],
        'ping': "❌"
    }

    try:
        # Vendor-Information
        vendor = MacLookup().lookup(mac)
        
        # Gerätetyp
        device_types = {
            'intel': '💻 Computer',
            'apple': '🍎 Apple',
            'liteon': '📶 Router',
            'azurewave': '📱 Smart Device',
            'wistron': '🖧 Netzwerk'
        }
        for key in device_types:
            if key in vendor.lower():
                analysis['device_type'] = device_types[key]
                break

        # Ping-Check
        if sr1(ARP(pdst=ip), timeout=1, verbose=0):
            analysis['ping'] = "✅"

        # Service-Check
        ports = {80: '🌐 HTTP', 443: '🔒 HTTPS', 22: '🛡️ SSH'}
        for port, icon in ports.items():
            with socket.socket() as s:
                s.settimeout(0.2)
                if s.connect_ex((ip, port)) == 0:
                    analysis['services'].append(icon)

    except Exception as e:
        pass
    
    return analysis

def scan_network():
    table = PrettyTable()
    table.field_names = ["IP", "MAC", "Typ", "Ping", "Dienste"]
    table.align = "l"

    interface = get_default_interface()
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'].rsplit('.',1)[0]+".0/24"), 
                timeout=2, verbose=0)

    for _, recv in ans:
        ip = recv.psrc
        mac = recv.hwsrc
        analysis = get_device_analysis(mac, ip)
        
        table.add_row([
            ip,
            mac,
            analysis['device_type'],
            analysis['ping'],
            ' '.join(analysis['services'])
        ])

    return table

if __name__ == "__main__":
    try:
        print("\n🔎 Network Scan")
        print(f"⏱️ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        result = scan_network()
        print(result)
        
        print("\n🔚 Scan beendet - Keine Daten gespeichert")

    except KeyboardInterrupt:
        print("\n🛑 Scan abgebrochen")