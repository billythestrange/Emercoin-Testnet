# Emercoin Testnet Dashboard

Ein leichtgewichtiges Python-basiertes Dashboard zur Überwachung und Verwaltung einer Emercoin Full-Node im Testnetz. Dieses Tool bietet eine grafische Benutzeroberfläche (GUI) für Nutzer, die den Emercoin-Daemon (`emercoind`) ohne die vollständige Qt-Wallet-GUI betreiben, aber dennoch wichtige Statusinformationen auf einen Blick sehen möchten.

## Funktionen

- **Echtzeit-Guthaben:** Zeigt den aktuellen Kontostand (EMC) der Wallet an.
- **Blockchain-Status:** Anzeige der aktuellen Blockhöhe.
- **Versionsinfo:** Anzeige der installierten Emercoin-Core Version.
- **Verbindungsprüfung:** Visualisierung des Verbindungsstatus zum lokalen Daemon.
- **Aktualisierung:** Manueller Refresh-Button zum Abrufen der neuesten Daten via RPC.

## Voraussetzungen

Bevor du das Dashboard startest, stelle sicher, dass folgende Komponenten installiert und konfiguriert sind:

### 1. Emercoin Core (Testnet)
Der Daemon muss im Testnet-Modus laufen. Deine `emercoin.conf` sollte RPC-Verbindungen erlauben:
```conf
testnet=1
server=1
rpcuser=dein_benutzername
rpcpassword=dein_passwort
rpcport=16662
```

### 2. System-Abhängigkeiten (Ubuntu)
Das Tool nutzt Python 3 und Tkinter für die Oberfläche. Installiere die notwendigen Pakete unter Ubuntu mit:
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip
```

### 3. Python Bibliotheken
Installiere die `requests` Bibliothek für die Kommunikation mit der RPC-Schnittstelle:
```bash
pip install requests
```

## Installation & Konfiguration

1. Klone dieses Repository oder lade die Datei `emer-testchain_dashboard.py` herunter.
2. Öffne die Datei und passe die RPC-Konfigurationsvariablen am Anfang des Skripts an deine `emercoin.conf` an:

```python
# --- KONFIGURATION ---
RPC_USER = "dein_benutzername"
RPC_PASS = "dein_passwort"
RPC_URL = "http://127.0.0.1:16662"
```

## Nutzung

Starte das Dashboard einfach über das Terminal:

```bash
python3 emer-testchain_dashboard.py 
```

## Screenshot
 ![alt text](<Screenshot EMC-App for Testnet.png>)
## Lizenz

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht.