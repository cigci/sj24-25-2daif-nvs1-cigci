#!/bin/bash

# Funktion zur Ermittlung der eigenen Netzwerkdaten
get_network_info() {
    echo "🖥️ Eigene Netzwerkinformationen:"
    echo "---------------------------------"
    
    # MAC-Adresse
    mac=$(ifconfig en0 | grep "ether" | awk '{print $2}')
    echo "MAC-Adresse: $mac"
    
    # IPv4-Adresse
    ipv4=$(ipconfig getifaddr en0)
    echo "IPv4-Adresse: $ipv4"
    
    # IPv6-Adresse (nur link-lokal)
    ipv6=$(ifconfig en0 | grep "inet6" | grep -v "autoconf" | awk '{print $2}')
    echo "IPv6-Adresse: $ipv6"
    echo ""
}

# Funktion für erweiterten Netzwerk-Scan
scan_network() {
    echo "🔍 Scanne Geräte im Netzwerk (IP + MAC-Adressen)..."
    echo "---------------------------------"
    
    # 1. Subnetz ermitteln
    interface=$(route -n get default | grep 'interface:' | awk '{print $2}')
    subnet=$(ipconfig getifaddr $interface | cut -d'.' -f1-3).0/24

    # 2. ARP-Scan (priorisiert)
    if command -v arp-scan &> /dev/null; then
        echo "📡 Verwende arp-scan (zuverlässigste Methode)..."
        sudo arp-scan --localnet --interface=$interface | awk '/192.168/{print "Gerät:", $1, "| MAC:", $2}'
    else
        echo "⚠️ arp-scan nicht installiert. Installiere es mit:"
        echo "   brew install arp-scan"
        echo "   (Verwende nmap als Fallback)"
    fi

    # 3. Nmap-Scan (zusätzlich)
    if command -v nmap &> /dev/null; then
        echo ""
        echo "📡 Zusätzlicher Scan mit nmap..."
        sudo nmap -sn $subnet | awk '/Nmap scan/{ip=$NF} /MAC Address/{mac=$3; print "Gerät:", ip, "| MAC:", mac}'
    else
        echo "ℹ️ Tipp: Installiere nmap mit 'brew install nmap'"
    fi
}

# Hauptprogramm
clear
echo "🔄 Starte Netzwerk-Analyse..."
echo "================================"
get_network_info
scan_network
echo "================================"
echo "✅ Scan abgeschlossen."