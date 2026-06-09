#!/usr/bin/env python3
"""
Emercoin Coin Control CLI
Erstellt Transaktionen mit manueller UTXO-Auswahl (Coin Control) für Emercoin Testnet
Kommuniziert über JSON-RPC mit der emer-testchain_dashboard.py Instanz
"""

import requests
import sys
from decimal import Decimal
from typing import Dict, List, Optional

# --- KONFIGURATION ---
RPC_USER = "emma"
RPC_PASS = "testnetemma"
RPC_URL = "http://127.0.0.1:16662"  # Standard-Testnet-Port

# Standard Change-Adresse (Notfall/Fallback für Wechselgeld)
# Falls beim Transaktionsprozess keine Change-Adresse eingegeben wird, wird diese verwendet
DEFAULT_CHANGE_ADDRESS = "te1q5h863l5llty665rnhz2a6vttjgjqpyjhgy3h29"


class EmercoinRPC:
    """Wrapper für Emercoin JSON-RPC Kommunikation"""

    def __init__(self, url: str, user: str, password: str):
        self.url = url
        self.user = user
        self.password = password

    def call(self, method: str, params: Optional[List] = None) -> Optional[Dict]:
        """Führt einen RPC-Aufruf aus"""
        if params is None:
            params = []

        payload = {
            "jsonrpc": "1.0",
            "id": "coincontrol-cli",
            "method": method,
            "params": params,
        }

        try:
            response = requests.post(
                self.url, auth=(self.user, self.password), json=payload, timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("error"):
                print(f"❌ RPC Fehler: {result['error']}")
                return None

            return result.get("result")
        except requests.exceptions.ConnectionError:
            print("❌ Fehler: Kann keine Verbindung zum Emercoin-Daemon herstellen")
            print(f"   URL: {self.url}")
            return None
        except Exception as e:
            print(f"❌ Fehler bei RPC-Aufruf: {e}")
            return None


class CoinControlCLI:
    """Interaktives CLI für Transaktionen mit Coin Control"""

    def __init__(self):
        self.rpc = EmercoinRPC(RPC_URL, RPC_USER, RPC_PASS)
        self.wallet_balance = Decimal("0")
        self.addresses = {}
        self.utxos = []

    def print_header(self, text: str):
        """Druckt einen formatierten Header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)

    def print_section(self, text: str):
        """Druckt einen Section-Header"""
        print(f"\n📌 {text}")
        print("-" * 60)

    def print_error(self, text: str):
        """Druckt eine Fehlermeldung"""
        print(f"❌ {text}")

    def print_success(self, text: str):
        """Druckt eine Erfolgsmeldung"""
        print(f"✅ {text}")

    def print_info(self, text: str):
        """Druckt eine Info-Meldung"""
        print(f"ℹ️  {text}")

    def format_amount(self, amount: Decimal) -> str:
        """Formatiert einen EMC-Betrag"""
        return f"{amount:.8f} EMC"

    def prompt_address(
        self, prompt_text: str, default: Optional[str] = None
    ) -> Optional[str]:
        """Fragt eine Adresse ab und validiert sie (mit optionalem Default)"""
        while True:
            if default:
                prompt = f"{prompt_text}\n[Default: {default}] (Enter = Standard, oder neue Adresse eingeben)"
                addr = input(f"\n{prompt}: ").strip()

                # Wenn Benutzer nur Enter drückt, nutze Default
                if not addr:
                    # Validiere den Default
                    result = self.rpc.call("validateaddress", [default])
                    if result and result.get("isvalid"):
                        self.print_success(f"Nutze Standard: {default}")
                        return default
                    else:
                        self.print_error(
                            "Standard-Adresse ist ungültig! Bitte gib eine Adresse ein"
                        )
                        continue
            else:
                addr = input(f"\n{prompt_text}: ").strip()

            if not addr:
                self.print_error("Adresse ist erforderlich!")
                continue

            # Validiere mit Emercoin-RPC
            result = self.rpc.call("validateaddress", [addr])
            if result and result.get("isvalid"):
                return addr
            else:
                self.print_error(f"'{addr}' ist keine gültige Emercoin-Adresse")

    def prompt_amount(
        self, prompt_text: str, max_amount: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Fragt einen Betrag ab und validiert ihn"""
        while True:
            amount_str = input(f"\n{prompt_text}: ").strip()

            if not amount_str:
                self.print_error("Betrag ist erforderlich!")
                continue

            try:
                amount = Decimal(amount_str)

                if amount <= 0:
                    self.print_error("Betrag muss größer als 0 sein!")
                    continue

                if max_amount and amount > max_amount:
                    self.print_error(
                        f"Betrag darf maximal {self.format_amount(max_amount)} sein!"
                    )
                    continue

                return amount
            except (ValueError, decimal.InvalidOperation):
                self.print_error("Ungültiger Betrag! Verwende Format: 10.5")

    def prompt_yes_no(self, prompt_text: str) -> bool:
        """Fragt eine Ja/Nein-Frage"""
        while True:
            response = input(f"\n{prompt_text} (j/n): ").strip().lower()
            if response in ("j", "ja", "y", "yes"):
                return True
            elif response in ("n", "nein", "no"):
                return False
            else:
                self.print_error("Bitte antworte mit 'j' oder 'n'")

    def connect_to_wallet(self) -> bool:
        """Verbindet sich mit der Wallet und lädt Daten"""
        self.print_header("📊 Verbindung zur Wallet")

        self.print_info("Verbinde zum Emercoin-Daemon...")

        # Prüfe Verbindung
        balance = self.rpc.call("getbalance")
        if balance is None:
            return False

        self.wallet_balance = Decimal(str(balance))
        self.print_success(
            f"Verbunden! Guthaben: {self.format_amount(self.wallet_balance)}"
        )

        # Lade Adressen
        self.print_info("Lade Wallet-Adressen...")
        addresses = self.rpc.call("listreceivedbyaddress", [0])

        if not addresses:
            self.print_error("Keine Adressen gefunden!")
            return False

        # Filtere nur Adressen mit Empfängen
        for addr_info in addresses:
            if addr_info.get("amount", 0) > 0:
                self.addresses[addr_info["address"]] = Decimal(str(addr_info["amount"]))

        if self.addresses:
            self.print_success(f"Geladen: {len(self.addresses)} Adressen")
        else:
            self.print_error("Keine Adressen mit Guthaben gefunden!")
            return False

        return True

    def load_utxos_for_address(self, address: str) -> List[Dict]:
        """Lädt alle UTXOs für eine bestimmte Adresse"""
        self.print_info(f"Lade UTXOs für {address}...")

        utxos_raw = self.rpc.call("listunspent", [0, 9999999, [address]])

        if not utxos_raw:
            return []

        utxos = []
        for utxo in utxos_raw:
            utxos.append(
                {
                    "txid": utxo["txid"],
                    "vout": utxo["vout"],
                    "address": utxo["address"],
                    "amount": Decimal(str(utxo["amount"])),
                    "confirmations": utxo.get("confirmations", 0),
                    "scriptPubKey": utxo.get("scriptPubKey", ""),
                }
            )

        return utxos

    def display_addresses(self):
        """Zeigt alle Adressen mit Guthaben an"""
        self.print_section("Verfügbare Adressen")

        for idx, (addr, balance) in enumerate(self.addresses.items(), 1):
            print(f"{idx:2}. {addr}")
            print(f"    Guthaben: {self.format_amount(balance)}")

    def select_source_address(self) -> Optional[str]:
        """Benutzer wählt Quell-Adresse"""
        self.print_section("Quell-Adresse auswählen")

        self.display_addresses()

        while True:
            try:
                choice = int(input("\nAdresse (Nummer): ").strip())
                addr_list = list(self.addresses.keys())

                if 1 <= choice <= len(addr_list):
                    selected = addr_list[choice - 1]
                    self.print_success(f"Ausgewählt: {selected}")
                    return selected
                else:
                    self.print_error(f"Bitte wähle eine Nummer von 1-{len(addr_list)}")
            except ValueError:
                self.print_error("Ungültige Eingabe!")

    def select_utxos(self, address: str) -> List[Dict]:
        """Benutzer wählt UTXOs manuell"""
        self.print_section(f"UTXO-Auswahl für {address}")

        utxos = self.load_utxos_for_address(address)

        if not utxos:
            self.print_error("Keine UTXOs gefunden!")
            return []

        # Zeige alle UTXOs
        total_available = Decimal("0")
        for idx, utxo in enumerate(utxos, 1):
            print(f"\n{idx:2}. TXID: {utxo['txid']}")
            print(f"    Vout: {utxo['vout']}")
            print(f"    Betrag: {self.format_amount(utxo['amount'])}")
            print(f"    Bestätigungen: {utxo['confirmations']}")
            total_available += utxo["amount"]

        print(f"\n💰 Gesamtverfügbar: {self.format_amount(total_available)}")

        # Auswahl-Modus
        print("\n🔧 Auswahl-Modi:")
        print("  1 = Einzelne UTXOs auswählen")
        print("  2 = Alle UTXOs verwenden")
        print("  3 = UTXOs nach Betrag (Summe)")

        mode = input("\nModus (1-3): ").strip()

        selected = []

        if mode == "1":
            selected = self._select_individual_utxos(utxos)
        elif mode == "2":
            selected = utxos
            self.print_success(f"Alle {len(utxos)} UTXOs ausgewählt")
        elif mode == "3":
            selected = self._select_by_amount(utxos, total_available)
        else:
            self.print_error("Ungültige Auswahl!")
            return []

        return selected

    def _select_individual_utxos(self, utxos: List[Dict]) -> List[Dict]:
        """Benutzer wählt einzelne UTXOs"""
        selected: list[Dict] = []
        selected_idx = set()

        while True:
            try:
                idx_str = input("\nUTXO-Nummer (oder 'fertig'): ").strip().lower()

                if idx_str == "fertig":
                    if selected:
                        break
                    else:
                        self.print_error("Bitte wähle mindestens ein UTXO!")
                        continue

                idx = int(idx_str)
                if 1 <= idx <= len(utxos):
                    if idx not in selected_idx:
                        selected.append(utxos[idx - 1])
                        selected_idx.add(idx)
                        self.print_success(f"UTXO {idx} hinzugefügt")
                    else:
                        self.print_info(f"UTXO {idx} bereits ausgewählt")
                else:
                    self.print_error(f"Bitte wähle eine Nummer von 1-{len(utxos)}")
            except ValueError:
                self.print_error("Ungültige Eingabe!")

        return selected

    def _select_by_amount(
        self, utxos: List[Dict], total_available: Decimal
    ) -> List[Dict]:
        """Benutzer wählt UTXOs nach Gesamtbetrag"""
        target = self.prompt_amount(
            "Benötigter Betrag (Coins werden nach Größe sortiert)", total_available
        )

        if not target:
            return []

        # Sortiere nach Betrag absteigend
        sorted_utxos = sorted(utxos, key=lambda u: u["amount"], reverse=True)

        selected = []
        accumulated = Decimal("0")

        for utxo in sorted_utxos:
            selected.append(utxo)
            accumulated += utxo["amount"]
            if accumulated >= target:
                break

        self.print_success(
            f"Ausgewählt: {len(selected)} UTXOs, "
            + f"Gesamtbetrag: {self.format_amount(accumulated)}"
        )

        return selected

    def create_transaction(
        self,
        selected_utxos: List[Dict],
        recipient_address: str,
        send_amount: Decimal,
        change_address: str,
        fee_per_kb: Decimal = Decimal("0.001"),
    ) -> Optional[str]:
        """Erstellt eine Transaktion mit ausgewählten UTXOs"""

        self.print_section("Transaktionserstellung")

        # Inputs vorbereiten
        inputs = []
        total_input = Decimal("0")

        for utxo in selected_utxos:
            inputs.append({"txid": utxo["txid"], "vout": utxo["vout"]})
            total_input += utxo["amount"]

        # Geschätzte Gebühr berechnen
        # Faustregel: ~200 Byte pro Input + ~34 Byte pro Output + ~10 Byte Overhead
        estimated_size = len(inputs) * 180 + 2 * 34 + 10
        estimated_fee = (Decimal(estimated_size) / Decimal("1000")) * fee_per_kb

        # Change berechnen
        change = total_input - send_amount - estimated_fee

        print("📝 Transaktionsdetails:")
        print(f"   Inputs: {len(inputs)}")
        print(f"   Input-Gesamtbetrag: {self.format_amount(total_input)}")
        print(f"   Empfänger: {recipient_address}")
        print(f"   Sendebetrag: {self.format_amount(send_amount)}")
        print(f"   Geschätzte Gebühr: {self.format_amount(estimated_fee)}")

        if change < 0:
            self.print_error(
                f"Nicht genug Guthaben! Fehlbetrag: {self.format_amount(abs(change))}"
            )
            return None

        # Outputs vorbereiten
        outputs = {recipient_address: float(send_amount)}

        if change > Decimal("0.00000001"):  # Nur wenn Dust-Schwelle überschritten
            print(f"   Change: {self.format_amount(change)}")
            outputs[change_address] = float(change)
        else:
            print(
                f"   Change: {self.format_amount(change)} (unter Dust-Schwelle, wird vernichtet)"
            )

        # Bestätigungsdialog
        print("\n⚠️  Bestätigung erforderlich!")
        if not self.prompt_yes_no("Transaktion mit diesen Einstellungen erstellen?"):
            self.print_info("Abgebrochen")
            return None

        # Erstelle Transaktion
        self.print_info("Erstelle Transaktion...")

        tx_raw = self.rpc.call("createrawtransaction", [inputs, outputs])

        if not tx_raw or not isinstance(tx_raw, str):
            self.print_error("Fehler bei Transaktionserstellung!")
            return None

        self.print_success("Raw-Transaktion erstellt!")
        print(f"TX (Hex): {tx_raw}")

        return tx_raw

    def sign_and_send_transaction(self, tx_hex: str) -> Optional[str]:
        """Signiert und sendet die Transaktion"""

        if not self.prompt_yes_no("Transaktion signieren und senden?"):
            self.print_info("Abgebrochen")
            return None

        self.print_info("Signiere Transaktion...")

        sign_result = self.rpc.call("signrawtransaction", [tx_hex])

        if not sign_result or not sign_result.get("complete"):
            self.print_error("Fehler beim Signieren der Transaktion!")
            if sign_result:
                print(f"Fehler: {sign_result.get('errors', [])}")
            return None

        signed_tx = sign_result.get("hex")

        self.print_info("Sende Transaktion...")

        txid = self.rpc.call("sendrawtransaction", [signed_tx])

        # rpc.call may return a dict/error object; ensure we return a string or None
        if isinstance(txid, dict):
            # try common keys that might contain the txid
            for key in ("result", "txid", "hex"):
                if key in txid and isinstance(txid[key], str):
                    txid = txid[key]
                    break
            else:
                # fallback: cannot extract string txid
                txid = None

        if not txid:
            self.print_error("Fehler beim Senden der Transaktion!")
            return None

        self.print_success("Transaktion gesendet!")
        print(f"\n🎉 TXID: {txid}")

        return txid

    def run(self):
        """Hauptprogramm"""
        self.print_header("🪙 Emercoin Coin Control CLI")

        # Verbinde zur Wallet
        if not self.connect_to_wallet():
            sys.exit(1)

        # Quell-Adresse
        source_addr = self.select_source_address()
        if not source_addr:
            sys.exit(1)

        # Ziel-Adresse
        recipient_addr = self.prompt_address("Ziel-Adresse eingeben")
        if not recipient_addr:
            sys.exit(1)

        # Sendebetrag
        max_send = self.addresses[source_addr]
        send_amt = self.prompt_amount(
            f"Sendebetrag (max. {self.format_amount(max_send)})", max_send
        )
        if send_amt is None:
            sys.exit(1)

        # UTXO-Auswahl
        selected_utxos = self.select_utxos(source_addr)
        if not selected_utxos:
            sys.exit(1)

        # Change-Adresse
        self.print_section("Change-Adresse (Wechselgeld)")
        print("Optionen:")
        print("  1 = Standard-Notfall-Adresse verwenden")
        print("  2 = Quell-Adresse verwenden")
        print("  3 = Andere Adresse eingeben")

        while True:
            choice = input("\nWahl (1-3): ").strip()

            if choice == "1":
                change_addr = DEFAULT_CHANGE_ADDRESS
                self.print_success(f"Nutze Standard: {change_addr}")
                break
            elif choice == "2":
                change_addr = source_addr
                self.print_success(f"Nutze Quell-Adresse: {source_addr}")
                break
            elif choice == "3":
                change_addr = self.prompt_address(
                    "Change-Adresse eingeben", default=DEFAULT_CHANGE_ADDRESS
                )
                if not change_addr:
                    sys.exit(1)
                break
            else:
                self.print_error("Bitte wähle 1, 2 oder 3!")

        # Transaktion erstellen
        tx_hex = self.create_transaction(
            selected_utxos, recipient_addr, send_amt, change_addr
        )

        if not tx_hex:
            sys.exit(1)

        # Signieren und senden
        txid = self.sign_and_send_transaction(tx_hex)

        if txid:
            print("\n" + "=" * 60)
            print("✅ Transaktion erfolgreich abgesendet!")
            print("=" * 60)
        else:
            sys.exit(1)


def main():
    """Entry Point"""
    try:
        cli = CoinControlCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programm abgebrochen durch Benutzer")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Kritischer Fehler: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
