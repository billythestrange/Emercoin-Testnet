# Emercoin Testnet Dashboard

Ein leichtgewichtiges Python-basiertes Dashboard zur Überwachung und Verwaltung einer Emercoin Full-Node im Testnetz. Dieses Tool bietet eine grafische Benutzeroberfläche (GUI) für Nutzer, die den Emercoin-Daemon (`emercoind`) ohne die vollständige Qt-Wallet-GUI betreiben, aber dennoch wichtige Statusinformationen auf einen Blick sehen möchten.

## Funktionen

Das Dashboard ist in mehrere spezialisierte Tabs unterteilt:

- **Übersicht:** 
    - Echtzeit-Guthaben und Verbindungsstatus.
    - Blockchain-Metriken: Aktuelle Blockhöhe, Alter des letzten Blocks (mm:ss) und die durchschnittliche Blockzeit (basierend auf den letzten 10 Blöcken).
    - Speicherplatzverbrauch der Testnet-Blockchain auf der Festplatte.
- **Adressen & TX:** 
    - Auflistung aller Wallet-Adressen.
    - Anzeige der Transaktionshistorie für eine ausgewählte Adresse.
    - **Detaillierte TX-Info:** Per Klick lassen sich technische Details einer Transaktion (Size, vSize, Weight, Inputs/Outputs) sowie der rohe JSON-Output anzeigen.
- **Peers:** 
    - Übersicht aller aktuell verbundenen Netzwerkknoten.
    - Anzeige von IP, Datenübertragung (Up/Down), Verbindungsdauer, Ping und beworbenen Netzwerk-Services.
- **Logs:** 
    - Integrierter Viewer für die `debug.log`.
    - Filtert automatisch Dashboard-eigenen RPC-Traffic heraus.
    - **Farb-Highlighting:** Visuelle Unterscheidung von Fehlern (Rot), neuen Blöcken (Grün), Verbindungen (Blau) und Mempool-Aktivitäten.

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
testnet=1
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

 ![alt text](<Screenshot EMC-Testnet-App for Readme.png>)

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht.
