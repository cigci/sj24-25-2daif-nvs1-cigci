// Server
// SSH-Dienst und aktivieren
sudo systemctl start ssh
sudo systemctl enable ssh

// Port 22 in der Firewall
sudo ufw allow ssh

// Status überprüfen 
sudo systemctl status ssh


// User
// SHH connection
ssh benutzername@server-ip

// Gen key
ssh-keygen

// Save key to server
ssh-copy-id benutzername@server-ip




// SSH verlassen
exit


:: Partner -> Fahd Douihech