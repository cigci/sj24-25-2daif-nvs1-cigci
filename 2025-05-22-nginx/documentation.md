<!-- HINWEIS: Überall wo 'umut.com' oder 'umut' steht, bitte durch deinen eigenen Usernamen und Domainnamen ersetzen! -->
# 🚀 Eigene CA & SSL-Zertifikate für Nginx: Schritt-für-Schritt-Anleitung

## Inhaltsverzeichnis
1. [Voraussetzungen](##voraussetzungen)
2. [Nginx installieren](#nginx-installieren)
3. [CA-Zertifikat erstellen](#ca-zertifikat-erstellen)
4. [Server-Zertifikat generieren](#server-zertifikat-generieren)
5. [Nginx konfigurieren](#nginx-konfigurieren)
6. [Zertifikate testen](#zertifikate-testen)
7. [Fehlerbehebung](#fehlerbehebung)
8. [FAQs & Tipps](#faqs--tipps)

---

## Voraussetzungen
- Ubuntu Server (oder andere Linux-Distribution)
- Root-Rechte (`sudo`)
- Grundkenntnisse im Terminal

---

## 1️⃣ Nginx installieren
```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl enable --now nginx
```

---

## 2️⃣ CA-Zertifikat erstellen
**Ordnerstruktur anlegen:**
```bash
mkdir -p ~/myCA/server
cd ~/myCA
```

**Root-CA-Schlüssel & Zertifikat erzeugen:**
```bash
openssl genrsa -out private/ca.key 4096
openssl req -x509 -new -nodes -key private/ca.key -sha256 -days 3650 -out certs/ca.crt
```
> Beispiel für Eingaben:
> - Country Name: AU
> - State: Wien
> - Organization: Cigci
> - Common Name: Umut

---

## 3️⃣ Server-Zertifikat generieren
**Konfigurationsdatei erstellen (`~/myCA/server/san.cnf`):**
```ini
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = umut.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = umut.com
IP.1 = 172.20.10.4
```

**Server-Zertifikat erzeugen:**
```bash
cd ~/myCA/server
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config san.cnf
openssl x509 -req -in server.csr -CA ../certs/ca.crt -CAkey ../private/ca.key -CAcreateserial -out server.crt -days 825 -sha256 -extfile san.cnf -extensions v3_req
```

---

## 4️⃣ Nginx konfigurieren
**Konfiguration anpassen (`/etc/nginx/sites-available/default`):**
```nginx
server {
    listen 443 ssl;
    server_name umut.com;

    ssl_certificate /home/umut/myCA/server/server.crt;
    ssl_certificate_key /home/umut/myCA/server/server.key;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    server_name umut.com;
    return 301 https://$host$request_uri;
}
```

**Nginx neu starten:**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 5️⃣ Zertifikate testen
**Verbindung prüfen:**
```bash
curl -vk --cacert ~/myCA/certs/ca.crt umut.com
```

**Zertifikatsdetails anzeigen:**
```bash
openssl x509 -in server.crt -text -noout
```

---

## 6️⃣ Fehlerbehebung
| Fehler                           | Lösung                                    |
|----------------------------------|-------------------------------------------|
| SSL_ERROR_BAD_CERT_DOMAIN        | `subjectAltName` in `san.cnf` prüfen      |
| nginx: [emerg] cannot load cert  | Pfade in Nginx-Konfig prüfen              |
| ERR_CERT_AUTHORITY_INVALID       | CA-Zertifikat im Browser importieren      |

---

## 7️⃣ FAQs & Tipps

**Wo installiere ich die CA auf Clients?**
- **Windows:** `.crt`-Datei doppelklicken → "Zertifikat installieren"
- **Linux:**
  ```bash
  sudo cp ca.crt /usr/local/share/ca-certificates/
  sudo update-ca-certificates
  ```
- **macOS:** Schlüsselbundverwaltung → Zertifikat importieren

**Wie lange sind die Zertifikate gültig?**
- CA: 10 Jahre (`-days 3650`)
- Server: 2 Jahre (`-days 825`)

> **Tipp:**
> - Für Produktivumgebungen: Nutze [Let's Encrypt](https://letsencrypt.org/) statt selbstsignierter Zertifikate.
> - Bewahre deinen CA-Schlüssel (`ca.key`) sicher und offline auf.
> - Immer `nginx -t` vor dem Neustart ausführen!