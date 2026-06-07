# 🪙 Emercoin Coin Control CLI

Ein benutzerfreundliches Kommandozeilen-Programm zur Erstellung von Emercoin-Transaktionen mit **manueller UTXO-Auswahl** (Coin Control).

## 🎯 Features

- **Interaktive Benutzeroberfläche** – Schritt-für-Schritt Abfrage aller benötigten Parameter
- **UTXO-Management** – Wähle **mehrere UTXOs** auf einmal aus! (Einzeln, alle, oder nach Betrag)
- **Intelligente Gebührenberechnung** – Automatische Schätzung der Transaktionsgröße und Gebühren
- **Change-Management** – 3 flexible Optionen:
  - Standard-Notfall-Adresse (nie die Adresse vergessen!)
  - Quell-Adresse
  - Benutzerdefinierte Adresse
- **Sicherheit** – Bestätigungsdialog vor dem Signieren und Senden
- **Fehlerbehandlung** – Validierung aller Eingaben und aussagekräftige Fehlermeldungen

## 📋 Voraussetzungen

1. **Emercoin Full-Node läuft** mit RPC aktiviert
2. **Dashboard-Skript läuft** (`emer-testchain_dashboard.py`) – liefert RPC-Zugriff
3. **Python 3.7+** installiert
4. **requests Library** installiert:
   ```bash
   pip install requests
   ```

## 🚀 Verwendung

### Start

```bash
./emercoin_coincontrol_cli.py
```

oder

```bash
python3 emercoin_coincontrol_cli.py
```

### Workflow

Das Programm führt dich interaktiv durch folgende Schritte:

#### 1️⃣ Verbindung zur Wallet
- Automatische Verbindung zum Emercoin-Daemon
- Anzeige des Guthaben und der verfügbaren Adressen

#### 2️⃣ Quell-Adresse wählen
- Zeigt alle Wallet-Adressen mit Guthaben
- Wähle die Adresse, von der Geld gesendet werden soll

#### 3️⃣ Ziel-Adresse eingeben
- Gib die Emercoin-Adresse des Empfängers ein
- Wird validiert bevor die Transaktion erstellt wird

#### 4️⃣ Sendebetrag definieren
- Gib den zu sendenden Betrag in EMC ein
- Die maximale Obergrenze ist das Guthaben der Quell-Adresse

#### 5️⃣ UTXOs manuell wählen (Mehrere möglich!)
Das Programm zeigt alle verfügbaren UTXOs für die Quell-Adresse an. Du kannst **mehrere UTXOs auswählen** und kombinieren:

**Modus 1: Einzelne UTXOs auswählen**
- Wähle jedes UTXO einzeln nach Nummer
- Bestätigung mit "fertig" wenn genug ausgewählt
- ✨ **Mehrere UTXOs auf einmal!**

**Modus 2: Alle UTXOs verwenden**
- Nutze sofort alle verfügbaren UTXOs
- ✨ **Automatisch alle Münzen in einer Transaktion kombiniert**

**Modus 3: Nach Betrag filtern**
- Gib einen Zielbetrauf an
- Das Programm sortiert UTXOs und nimmt die größten zuerst
- ✨ **Intelligente Kombinationen mehrerer UTXOs**

#### 6️⃣ Change-Adresse konfigurieren (Mit Notfall-Default!)
Das Programm bietet jetzt **3 Optionen** für das Wechselgeld:

- **Option 1:** Standard-Notfall-Adresse verwenden (automatisch vorausgefüllt)
  - `te1q5h863l5llty665rnhz2a6vttjgjqpyjhgy3h29`
  - Perfekt falls du die Adresse vergisst einzutragen
  
- **Option 2:** Change geht zurück auf die Quell-Adresse (schnell)
  - Wechselgeld kommt da an, wo es herkommt
  
- **Option 3:** Change-Adresse manuell eingeben (fortgeschrittene Nutzung)
  - Mit Standard-Vorschlag zum schnellen Überschreiben

#### 7️⃣ Transaktion bestätigen
- Überblick über alle Transaktionsdetails
- **Eingaben:** Anzahl und Betrag
- **Gebühren:** Automatisch geschätzt
- **Change:** Rückbetrag nach Gebührenabzug

#### 8️⃣ Signieren und Senden
- Finale Bestätigungsdialog
- Transaktion wird signiert mit privatem Schlüssel
- Transaktion ins Netzwerk gesendet
- **TXID** wird angezeigt zum Tracking

## ⚙️ Konfiguration

Die RPC-Einstellungen und Standard Change-Adresse befinden sich oben im Skript:

```python
RPC_USER = "emma"
RPC_PASS = "testnetemma"
RPC_URL = "http://127.0.0.1:16662"  # Standard-Testnet-Port

# Standard Change-Adresse (Notfall/Fallback für Wechselgeld)
DEFAULT_CHANGE_ADDRESS = "te1q5h863l5llty665rnhz2a6vttjgjqpyjhgy3h29"
```

Diese sollten mit den Einstellungen in `emer-testchain_dashboard.py` übereinstimmen.

### Die Standard Change-Adresse anpassen

Falls du eine andere Notfall-Adresse verwenden möchtest, ändere die `DEFAULT_CHANGE_ADDRESS`:

```python
DEFAULT_CHANGE_ADDRESS = "deine-adresse-hier"
```

Diese wird als **Option 1** während der Transaktionserstellung angeboten und kann jederzeit überschrieben werden.

## 🔍 Beispiel-Workflow

```
🪙 Emercoin Coin Control CLI
============================================================

📊 Verbindung zur Wallet
----
ℹ️  Verbinde zum Emercoin-Daemon...
✅ Verbunden! Guthaben: 50.12345678 EMC
ℹ️  Lade Wallet-Adressen...
✅ Geladen: 3 Adressen

📌 Verfügbare Adressen
----
 1. EZnEi9nEm1jQR2C1v2pV3xYmZ4aBbC5d6eF
    Guthaben: 50.12345678 EMC
 2. EGa9hB8c7D6e5f4g3h2i1j0K1l2M3n4o5p
    Guthaben: 25.50000000 EMC
 3. EQ3wX8yZ2a1b0C9d8e7f6g5h4i3j2k1L0m
    Guthaben: 10.00000000 EMC

📌 Quell-Adresse auswählen
Adresse (Nummer): 1

Ziel-Adresse eingeben: EGa9hB8c7D6e5f4g3h2i1j0K1l2M3n4o5p
Sendebetrag (max. 50.12345678 EMC): 10.5

📌 UTXO-Auswahl für EZnEi9nEm1jQR2C1v2pV3xYmZ4aBbC5d6eF
----
 1. TXID: abc123...
    Vout: 0
    Betrag: 25.00000000 EMC
    Bestätigungen: 102
 
 2. TXID: def456...
    Vout: 1
    Betrag: 15.12345678 EMC
    Bestätigungen: 95
 
 3. TXID: ghi789...
    Vout: 0
    Betrag: 10.00000000 EMC
    Bestätigungen: 50

💰 Gesamtverfügbar: 50.12345678 EMC

🔧 Auswahl-Modi:
  1 = Einzelne UTXOs auswählen
  2 = Alle UTXOs verwenden
  3 = UTXOs nach Betrag (Summe)

Modus (1-3): 3
Benötigter Betrag (Coins werden nach Größe sortiert): 15

✅ Ausgewählt: 2 UTXOs, Gesamtbetrag: 40.12345678 EMC

📌 Change-Adresse (Wechselgeld)
Optionen:
  1 = Standard-Notfall-Adresse verwenden
  2 = Quell-Adresse verwenden
  3 = Andere Adresse eingeben

Wahl (1-3): 1
✅ Nutze Standard: te1q5h863l5llty665rnhz2a6vttjgjqpyjhgy3h29

📝 Transaktionsdetails:
   Inputs: 2
   Input-Gesamtbetrag: 40.12345678 EMC
   Empfänger: EGa9hB8c7D6e5f4g3h2i1j0K1l2M3n4o5p
   Sendebetrag: 10.50000000 EMC
   Geschätzte Gebühr: 0.00000400 EMC
   Change: 29.61344878 EMC

⚠️  Bestätigung erforderlich!
Transaktion mit diesen Einstellungen erstellen? (j/n): j

ℹ️  Erstelle Transaktion...
✅ Raw-Transaktion erstellt!
TX (Hex): 0200000002abc...

ℹ️  Transaktion signieren und senden?
Transaktion signieren und senden? (j/n): j

ℹ️  Signiere Transaktion...
ℹ️  Sende Transaktion...
✅ Transaktion gesendet!

🎉 TXID: 7f8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e

============================================================
✅ Transaktion erfolgreich abgesendet!
============================================================
```

## 🛡️ Sicherheit

- Alle Eingaben werden validiert
- Transaktionen benötigen Bestätigung vor dem Senden
- Der private Schlüssel wird **nie** das Programm verlassen
- Die Wallet muss **unverschlüsselt** sein (normale RPC-Anforderung)

## 🐛 Fehlerbehebung

### "Fehler: Kann keine Verbindung zum Emercoin-Daemon herstellen"
- Stelle sicher, dass `emer-testchain_dashboard.py` läuft
- Prüfe RPC_URL, RPC_USER und RPC_PASS in beiden Dateien
- Prüfe Firewall-Einstellungen

### "Nicht genug Guthaben!"
- Die Summe der UTXOs + Gebühren reicht nicht aus
- Wähle mehr/größere UTXOs
- oder verringere den Sendebetrag

### "ist keine gültige Emercoin-Adresse"
- Prüfe die Adresse auf Tippfehler
- Stelle sicher, dass es eine Testnet-Adresse ist
- Testnet-Adressen beginnen üblicherweise mit "E"

## 📚 Weitere Ressourcen

- [Emercoin Official](https://emercoin.com)
- [Emercoin Testnet Anleitung](./Emercoin%20Testnet%20-%20Anleitung%20Wallet%20erstellen.md)
- [Dashboard README](./README.md)

## 📝 Lizenz

MIT – Frei verwendbar und modifizierbar

---

**Hinweis:** Dieses Tool ist für Testnet entwickelt. Nutze es vorsichtig und teste es gründlich, bevor du es mit echtem Geld (Mainnet) verwendest!
