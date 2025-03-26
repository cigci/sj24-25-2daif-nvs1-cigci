#!/bin/bash

# Funktion zur Abfrage mit Fehlerbehandlung
run_dig_query() {
  result=$(dig "$@" +short)
  if [ -z "$result" ]; then
    echo "  ❌ Keine Einträge gefunden."
  else
    echo "$result" | sed 's/^/  /'
  fi
}

# MX-Records für whitehouse.gov
echo "🔍 MX-Records für whitehouse.gov:"
run_dig_query MX whitehouse.gov

echo

# IPv4-Adressen für zdf.de
echo "🔍 IPv4-Adressen (A-Records) für zdf.de:"
run_dig_query A zdf.de

echo

# IPv6-Adressen für zdf.de
echo "🔍 IPv6-Adressen (AAAA-Records) für zdf.de:"
run_dig_query AAAA zdf.de