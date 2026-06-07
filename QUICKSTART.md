# 🚀 Emercoin Coin Control CLI - Quick Start

## Installation (einmalig)

```bash
# 1. Repository-Verzeichnis öffnen
cd ~/Projekte/VisualStudioCode/Emercoin-Testnet

# 2. requests Library installieren (falls noch nicht geschehen)
pip install requests

# 3. Skripte ausführbar machen (falls noch nicht geschehen)
chmod +x emercoin_coincontrol_cli.py coincontrol.sh
```

## Verwendung

### Option 1: Direkt mit Python (schnell)
```bash
./emercoin_coincontrol_cli.py
```

### Option 2: Mit Launcher-Menü (empfohlen)
```bash
./coincontrol.sh
```
Dies bietet ein Menü mit zusätzlichen Optionen.

### Option 3: Mit GUI-Menü (im Desktop-Umgebung)
- Doppelklick auf `emercoin-coincontrol-cli.desktop`
- Oder über Anwendungs-Menü → "Emercoin Coin Control CLI"

## 📋 Ablauf-Übersicht

```
1. Starten             → Program startet und verbindet zur Wallet
2. Quell-Adresse       → Wähle Adresse von der Geld gesendet wird
3. Ziel-Adresse        → Gib Empfänger-Adresse ein
4. Betrag              → Gib zu sendenden Betrag ein
5. UTXO-Auswahl        → Wähle Münzen (manual, alle, oder nach Betrag)
6. Change-Adresse      → Wohin kommt das Rückgeld?
7. Bestätigung         → Überprüfe Transaktions-Details
8. Signieren & Senden  → Finale Bestätigung, dann ab ins Netzwerk
9. TXID                → Transaktion erledigt! 🎉
```

## ⚙️ Vorbedingungen (MUSS erfüllt sein!)

✅ **Emercoin-Daemon läuft**
```bash
# Prüfen ob Daemon läuft:
ps aux | grep emercoind
```

✅ **Dashboard-Skript läuft**
```bash
# In separatem Terminal starten:
./emer-testchain_dashboard.py
```

✅ **Wallet ist entsperrt** (min. für Transaktionen)
```bash
# Im Dashboard oder über CLI:
walletpassphrase <Passphrase> <Sekunden>
```

## 🎯 Typisches Szenario

Sagen wir, du möchtest:
- **Von:** Adresse A (Gesamtbestand: 100 EMC)
- **An:** Adresse B
- **Betrag:** 25 EMC
- **Change:** zurück zu Adresse A

Schritt-für-Schritt:

1. Starte das Programm
2. System zeigt deine 3 Adressen, du wählst Adresse A
3. Gib Adresse B als Empfänger ein
4. Gib 25 EMC als Sendebetrag ein
5. System zeigt all deine UTXOs in Adresse A (z.B. 5 Münzen à 20 EMC)
6. Wähle "Modus 3" → gib 25 ein → System nimmt die erste beste 20-EMC-Münze
7. Bestätige Change auf Adresse A
8. Überblick: 20 EMC rein, 25 EMC raus = unmöglich? 
   - **Wait!** Dann musst du mehr UTXOs nehmen oder weniger senden

Das ist genau der Sinn von **Coin Control** – du siehst jeden Schritt!

## 🔧 Konfiguration (falls nötig)

Falls deine RPC-Einstellungen unterschiedlich sind, ändere diese in der Python-Datei:

```python
# emercoin_coincontrol_cli.py, Zeile 20-22:
RPC_USER = "emma"           # Ändere wenn nötig
RPC_PASS = "testnetemma"    # Ändere wenn nötig  
RPC_URL = "http://127.0.0.1:16662"  # Ändere wenn nötig
```

## ❓ FAQ

**F: "Fehler: Kann keine Verbindung zum Emercoin-Daemon herstellen"**
A: Prüfe ob der Daemon läuft: `ps aux | grep emercoind`

**F: "Fehler bei getbalance"**
A: Die Wallet ist wahrscheinlich gesperrt. Speichere sie auf: `walletpassphrase <Passphrase> 999999`

**F: "Nicht genug Guthaben!"**
A: Die ausgewählten UTXOs reichen nicht für Betrag + Gebühren. Wähle mehr UTXOs.

**F: Kann ich abbrechen?**
A: Ja! Mit `Ctrl+C` jederzeit beenden.

**F: Kann ich Transaktionen vorher testen?**
A: Das Programm zeigt alle Details vor dem Signieren. Du kannst noch abbrechen!

## 🎓 Lernziele

Dieses Tool hilft dir zu verstehen:
- Wie UTXOs funktionieren (Unspent Transaction Outputs)
- Transaktionsgebühren und deren Berechnung
- Change-Management in Blockchain
- Raw-Transaction Creation & Broadcasting

## 📞 Hilfe

- Lese die vollständige [COINCONTROL_README.md](./COINCONTROL_README.md)
- Checke die Logs des Daemons: `tail -f ~/.emercoin/testnet3/debug.log`
- Dashboard für Wallet-Status: `./emer-testchain_dashboard.py`

---

**Viel Erfolg beim Testen! 🪙**
