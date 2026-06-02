Da deine Node auf der Version **v0.8.5emc** läuft und somit auf der klassischen Berkeley-DB-Architektur (BDB) ohne Deskriptoren basiert, hast du dennoch über die RPC-Schnittstelle einige mächtige Optionen, um das Verhalten, die Struktur und die Sicherheitsfeatures einer neuen Wallet zu steuern.  
Hier ist die detaillierte Aufschlüsselung, wie du eine weitere Wallet erstellst, welche Typen dir zur Verfügung stehen und wie du direkt Adressen generierst.

## **1\. Eine weitere Wallet erstellen (Der Befehl)**

Der grundlegende Befehl lautet createwallet. Da du mehrere Wallets parallel betreiben kannst (Multi-Wallet), musst du dem Kind einen Namen geben.

Bash  
emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet createwallet "Name\_der\_Wallet" \[disable\_private\_keys\] \[blank\] \[passphrase\] \[avoid\_reuse\]

## **2\. Die verschiedenen Wallet-Typen und ihre Eigenschaften**

Durch die Kombination der optionalen booleschen Parameter (true / false) beim Erstellen, bestimmst du die "Art" und die Features der Wallet:

### **Typ A: Die Standard-HD-Wallet (Hierarchical Deterministic)**

Das ist der Allrounder. Sie generiert automatisch einen Master-Seed (HD-Seed), aus dem mathematisch alle zukünftigen Keys abgeleitet werden. Du musst nur einmalig die wallet.dat sichern.

* **Befehl:**  
  Bash  
  emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet createwallet "HD\_Standard\_Wallet" false false

* **Eigenschaften:** Besitzt Private Keys, generiert automatisch einen Keypool von 100 Adressen im Voraus, ist unverschlüsselt.

### **Typ B: Die "Watch-Only" / "Sicherheits"-Wallet**

Dieser Typ besitzt *keine* Private Keys. Du nutzt ihn, um Adressen und Guthaben zu überwachen (z. B. auf einem ungesicherten Server), ohne dass Angreifer die Coins stehlen können.

* **Befehl:**  
  Bash  
  emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet createwallet "Watch\_Only\_Wallet" true

* **Eigenschaften:** disable\_private\_keys=true. Du musst Public Keys oder Adressen manuell via importaddress oder importpubkey hinzufügen. Mining oder Senden ist mit dieser Wallet nicht möglich.

### **Typ C: Die "Blank" (Leere) Wallet**

Eine normale HD-Wallet wird beim Erstellen sofort mit einem Pool aus frischen Schlüsseln befüllt. Eine "Blank Wallet" hingegen ist komplett leer.

* **Befehl:**  
  Bash  
  emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet createwallet "Leere\_Wallet" false true

* **Eigenschaften:** blank=true. Nützlich, wenn du ein mathematisch sauberes Backup direkt nach der Erstellung machen willst, bevor überhaupt die erste Adresse existiert, oder wenn du gezielt Keys aus externen Quellen (z. B. Paper-Wallets) via importprivkey migrieren möchtest.

### **Typ D: Die verschlüsselte Wallet (Direkt beim Erstellen)**

Du kannst der Wallet direkt beim Erzeugen ein Passwort mitgeben.

* **Befehl:**  
  Bash  
  emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet createwallet "Sichere\_Wallet" false false "MeinSuperSicheresPasswort123\!"

* **Eigenschaften:** Die Private Keys werden AES-256 verschlüsselt auf der Festplatte abgelegt. Für jedes Mining (generatetoaddress) oder Senden musst du die Wallet temporär mit walletpassphrase entsperren.

## **3\. Das Feature: "Avoid Reuse" (Vermeidung von Adress-Wiederholung)**

Der letzte Parameter bei createwallet heißt avoid\_reuse (ein boolescher Wert).  
Wenn du eine Wallet mit true am Ende erstellst:

Bash  
emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet createwallet "Privacy\_Wallet" false false "" true

* **Feature-Erklärung:** Die Wallet-Logik ändert sich fundamental bei der Coin-Selection. Wenn du Coins von einer Adresse ausgiebst, versucht die Node aktiv, *alle* UTXOs dieser spezifischen Adresse aufzubrauchen und das Wechselgeld auf eine brandneue Adresse zu legen. Es verhindert, dass auf alten Adressen "Restbestände" verbleiben. Das erhöht die Privatsphäre auf der Blockchain massiv, da es die Verknüpfung von Transaktionen erschwert.

## **4\. Schritt-für-Schritt: Neue Wallet laden und Adressen erzeugen**

Wenn du eine neue Wallet erstellt hast, musst du der CLI bei den Folge-Befehlen mitteilen, *welche* Wallet du meinst (sofern sie nicht als Standard in der .conf definiert ist). Das geschieht über den Parameter \-rpcwallet.

### **Schritt A: Informationen der neuen Wallet prüfen**

Bash  
emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet \-rpcwallet=HD\_Standard\_Wallet getwalletinfo

### **Schritt B: Neue Adressen generieren**

Jetzt erzeugen wir die unterschiedlichen Adresstypen innerhalb dieser spezifischen Wallet:

1. **Legacy-Adresse (P2PKH \- startet mit m/n):**  
   Bash  
   emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet \-rpcwallet=HD\_Standard\_Wallet getnewaddress "mein\_label" "legacy"

2. **Native SegWit (Bech32 \- startet mit emt1):**  
   Bash  
   emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet \-rpcwallet=HD\_Standard\_Wallet getnewaddress "mein\_label" "bech32"

3. **P2SH-SegWit (Nested SegWit \- startet mit 2):**  
   Bash  
   emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet \-rpcwallet=HD\_Standard\_Wallet getnewaddress "mein\_label" "p2sh-segwit"

### **Schritt C: Adressen auflisten**

Um zu sehen, was du erzeugt hast:

Bash  
emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet \-rpcwallet=HD\_Standard\_Wallet getaddressesbylabel "mein\_label"

### **Ein nützlicher Befehl zum Beenden/Wechseln:**

Wenn du eine Wallet nicht mehr im Arbeitsspeicher der Node haben willst, kannst du sie entladen:

Bash  
emercoin-cli \-testnet \-datadir=/mnt/hdd/sdb2/.emercoin\_testnet unloadwallet "HD\_Standard\_Wallet"  
