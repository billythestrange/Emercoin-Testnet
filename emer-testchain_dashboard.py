import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import time
import datetime
import os

# --- KONFIGURATION ---
RPC_USER = "emma"
RPC_PASS = "testnetemma"
RPC_URL = "http://127.0.0.1:16662"  # Standard-Testnet-Port
LOG_PATH = "/mnt/hdd/sdb2/.emercoin_testnet/testnet3/debug.log"


class EmercoinGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emercoin Testnet Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")

        # Icon für das Fenster setzen
        icon_path = "/home/bitkiller/Projekte/VisualStudioCode/Emercoin-Testnet/blockchain_wallet2.png"
        if os.path.exists(icon_path):
            try:
                self.icon_img = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(False, self.icon_img)
            except Exception as e:
                print(f"Fehler beim Laden des Icons: {e}")

        # UI Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TLabel", background="#2c3e50", foreground="white", font=("Arial", 11)
        )
        style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        style.configure("TNotebook", background="#2c3e50", borderwidth=0)
        style.configure(
            "TNotebook.Tab", background="#34495e", foreground="white", padding=[10, 5]
        )
        style.map("TNotebook.Tab", background=[("selected", "#27ae60")])

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_overview = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_addresses = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_peers = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_logs = tk.Frame(self.notebook, bg="#2c3e50")

        self.notebook.add(self.tab_overview, text=" Übersicht ")
        self.notebook.add(self.tab_addresses, text=" Adressen & TX ")
        self.notebook.add(self.tab_peers, text=" Peers ")
        self.notebook.add(self.tab_logs, text=" Logs ")

        # --- TAB 1: ÜBERSICHT ---
        self.header = ttk.Label(
            self.tab_overview, text="Emercoin Wallet Status", style="Header.TLabel"
        )
        self.header.pack(pady=20)

        info_frame = tk.Frame(self.tab_overview, bg="#34495e", padx=20, pady=20)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.balance_label = self.create_info_row(info_frame, "Kontostand:", "Lädt...")
        self.blocks_label = self.create_info_row(info_frame, "Blöcke:", "Lädt...")
        self.age_label = self.create_info_row(info_frame, "Block-Alter:", "Lädt...")
        self.avg_time_label = self.create_info_row(
            info_frame, "Ø Blockzeit:", "Lädt..."
        )
        self.disk_label = self.create_info_row(info_frame, "Speicherplatz:", "Lädt...")
        self.version_label = self.create_info_row(info_frame, "Version:", "Lädt...")
        self.connection_label = self.create_info_row(info_frame, "Status:", "Prüfe...")

        # --- TAB 2: ADRESSEN & TX ---
        addr_frame = tk.Frame(self.tab_addresses, bg="#2c3e50", padx=10, pady=10)
        addr_frame.pack(fill="both", expand=True)

        ttk.Label(addr_frame, text="Deine Adressen (Klick für Details):").pack(
            anchor="w"
        )

        # Address Treeview
        self.addr_tree = ttk.Treeview(
            addr_frame, columns=("Address", "Balance"), show="headings", height=5
        )
        self.addr_tree.heading("Address", text="Adresse")
        self.addr_tree.heading("Balance", text="Empfangen (Gesamt)")
        self.addr_tree.column("Address", width=350)
        self.addr_tree.pack(fill="x", pady=5)
        self.addr_tree.bind("<<TreeviewSelect>>", self.on_address_select)

        ttk.Label(addr_frame, text="Zugehörige Transaktionen:").pack(
            anchor="w", pady=(10, 0)
        )

        # Transactions Treeview
        self.tx_tree = ttk.Treeview(
            addr_frame,
            columns=("Type", "Amount", "Conf", "TXID"),
            show="headings",
            height=8,
        )
        self.tx_tree.heading("Type", text="Typ")
        self.tx_tree.heading("Amount", text="Betrag")
        self.tx_tree.heading("Conf", text="Bestät.")
        self.tx_tree.heading("TXID", text="TXID")
        self.tx_tree.column("Type", width=80)
        self.tx_tree.column("Amount", width=100)
        self.tx_tree.column("Conf", width=60)
        self.tx_tree.column("TXID", width=250)
        self.tx_tree.pack(fill="both", expand=True, pady=5)
        self.tx_tree.bind("<<TreeviewSelect>>", self.on_tx_select)

        # --- TAB 3: PEERS ---
        peer_frame = tk.Frame(self.tab_peers, bg="#2c3e50", padx=10, pady=10)
        peer_frame.pack(fill="both", expand=True)

        ttk.Label(peer_frame, text="Verbundene Netzwerkknoten (Peers):").pack(
            anchor="w"
        )

        # Container für Treeview und Scrollbars
        peer_tree_frame = tk.Frame(peer_frame, bg="#2c3e50")
        peer_tree_frame.pack(fill="both", expand=True, pady=5)

        self.peer_tree = ttk.Treeview(
            peer_tree_frame,
            columns=(
                "ID",
                "Address",
                "Sent",
                "Recv",
                "Since",
                "Height",
                "Services",
                "Ping",
            ),
            show="headings",
        )

        # Scrollbars für die Peer-Liste
        peer_scroll_y = ttk.Scrollbar(
            peer_tree_frame, orient="vertical", command=self.peer_tree.yview
        )
        peer_scroll_x = ttk.Scrollbar(
            peer_tree_frame, orient="horizontal", command=self.peer_tree.xview
        )
        self.peer_tree.configure(
            yscrollcommand=peer_scroll_y.set, xscrollcommand=peer_scroll_x.set
        )

        peer_scroll_y.pack(side="right", fill="y")
        peer_scroll_x.pack(side="bottom", fill="x")
        self.peer_tree.pack(side="left", fill="both", expand=True)

        self.peer_tree.heading("ID", text="ID")
        self.peer_tree.heading("Address", text="Adresse")
        self.peer_tree.heading("Sent", text="Gesendet")
        self.peer_tree.heading("Recv", text="Empfangen")
        self.peer_tree.heading("Since", text="Seit")
        self.peer_tree.heading("Height", text="Starthöhe")
        self.peer_tree.heading("Services", text="Services")
        self.peer_tree.heading("Ping", text="Ping")

        self.peer_tree.column("ID", width=40, stretch=False)
        self.peer_tree.column("Address", width=180, stretch=False)
        self.peer_tree.column("Sent", width=100, stretch=False)
        self.peer_tree.column("Recv", width=100, stretch=False)
        self.peer_tree.column("Since", width=100, stretch=False)
        self.peer_tree.column("Height", width=100, stretch=False)
        self.peer_tree.column("Services", width=400, minwidth=150, stretch=True)
        self.peer_tree.column("Ping", width=80, stretch=False)

        # --- TAB 4: LOGS ---
        log_frame = tk.Frame(self.tab_logs, bg="#2c3e50", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True)

        # Text-Widget für Logs mit Scrollbars
        self.log_text = tk.Text(
            log_frame,
            bg="#1e272e",
            fg="#dcdde1",
            font=("Courier New", 9),
            wrap="none",
            state="disabled",
        )
        self.log_scroll_y = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.log_text.yview
        )
        self.log_scroll_x = ttk.Scrollbar(
            log_frame, orient="horizontal", command=self.log_text.xview
        )
        self.log_text.configure(
            yscrollcommand=self.log_scroll_y.set, xscrollcommand=self.log_scroll_x.set
        )

        self.log_scroll_y.pack(side="right", fill="y")
        self.log_scroll_x.pack(side="bottom", fill="x")
        self.log_text.pack(side="left", fill="both", expand=True)

        # Tag-Konfiguration für Highlighting
        self.log_text.tag_configure("error", foreground="#e62a15")  # Rot
        self.log_text.tag_configure("block", foreground="#06f622")  # Hellgrün
        self.log_text.tag_configure("conn", foreground="#11c4fb")  # Hellblau
        self.log_text.tag_configure("recon", foreground="#ffe20a")  # Gelb
        self.log_text.tag_configure("mempool", foreground="#02880b")  # Dunkelgrün
        self.log_text.tag_configure("comm", foreground="#f97b0c")  # Orange
        self.log_text.tag_configure("sync", foreground="#0063e5")  # Blau

        # Refresh Button
        self.refresh_btn = tk.Button(
            self.root,
            text="Daten aktualisieren",
            command=self.update_data,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=8,
        )
        self.refresh_btn.pack(pady=20)

        # Initialer Datenabruf
        self.update_data()

    def create_info_row(self, parent, label_text, value_text):
        row = tk.Frame(parent, bg="#34495e")
        row.pack(fill="x", pady=5)

        lbl = ttk.Label(row, text=label_text, width=15)
        lbl.pack(side="left")

        val = ttk.Label(row, text=value_text)
        val.pack(side="left")
        return val

    def call_rpc(self, method, params=[]):
        payload = {"jsonrpc": "1.0", "id": "gui", "method": method, "params": params}
        try:
            response = requests.post(
                RPC_URL, auth=(RPC_USER, RPC_PASS), json=payload, timeout=5
            )
            response.raise_for_status()
            return response.json().get("result")
        except Exception as e:
            print(f"Fehler bei {method}: {e}")
            return None

    def update_data(self):
        # Wallet Balance
        balance = self.call_rpc("getbalance")
        if balance is not None:
            self.balance_label.config(text=f"{balance} EMC")
            self.connection_label.config(text="Verbunden", foreground="#2ecc71")
        else:
            self.connection_label.config(
                text="Keine Verbindung zum Daemon", foreground="#e74c3c"
            )

        # Blockchain Info
        blockchain_info = self.call_rpc("getblockchaininfo")
        if blockchain_info:
            height = blockchain_info.get("blocks")
            self.blocks_label.config(text=height)

            # Disk Space (Umrechnung in MB)
            size_bytes = blockchain_info.get("size_on_disk", 0)
            self.disk_label.config(text=f"{size_bytes / (1024 * 1024):.2f} MB")

            # Block-Alter berechnen
            best_hash = blockchain_info.get("bestblockhash")
            block_data = self.call_rpc("getblock", [best_hash])
            if block_data:
                block_time = block_data.get("time")
                age_seconds = int(time.time()) - block_time
                mins, secs = divmod(max(0, age_seconds), 60)
                self.age_label.config(text=f"{mins:02d}:{secs:02d}")

            # Durchschnittliche Blockzeit (letzte 10 Blöcke)
            if height > 10:
                h1_hash = self.call_rpc("getblockhash", [height])
                h2_hash = self.call_rpc("getblockhash", [height - 10])
                t1 = self.call_rpc("getblock", [h1_hash]).get("time")  # type: ignore
                t2 = self.call_rpc("getblock", [h2_hash]).get("time")  # type: ignore
                avg = (t1 - t2) / 10
                self.avg_time_label.config(text=f"{avg:.1f} s")
            else:
                self.avg_time_label.config(text="N/A")

        # Network Info
        network_info = self.call_rpc("getnetworkinfo")
        if network_info:
            self.version_label.config(text=network_info.get("version"))

        # Update Peers
        peers = self.call_rpc("getpeerinfo")
        self.peer_tree.delete(*self.peer_tree.get_children())
        if peers:
            for p in peers:
                # Zeitstempel formatieren
                conn_since = datetime.datetime.fromtimestamp(
                    p.get("conntime", 0)
                ).strftime("%H:%M:%S")

                self.peer_tree.insert(
                    "",
                    "end",
                    values=(
                        p.get("id"),
                        p.get("addr"),
                        f"{p.get('bytesent', 0) / 1024:.1f} KB",
                        f"{p.get('bytesrecv', 0) / 1024:.1f} KB",
                        conn_since,
                        p.get("startingheight", "N/A"),
                        self._get_service_names(p.get("services", "")),
                        f"{p.get('pingtime', 0) * 1000:.1f} ms",
                    ),
                )

        # Update Address List
        self.update_address_list()

        # Update Logs
        self.update_logs()

    def update_logs(self):
        if not os.path.exists(LOG_PATH):
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.insert("end", f"Log-Datei nicht gefunden unter: {LOG_PATH}")
            self.log_text.config(state="disabled")
            return

        try:
            with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
                # Wir lesen die letzten 2MB der Datei für Effizienz
                f.seek(0, os.SEEK_END)
                f.seek(max(0, f.tell() - 2 * 1024 * 1024))
                lines = f.readlines()

            now = datetime.datetime.now()
            thirty_mins_ago = now - datetime.timedelta(minutes=30)

            output_lines = []
            for line in reversed(lines):
                if len(output_lines) >= 3500:
                    break

                # Filtere interne RPC POST Requests heraus (Dashboard-Traffic)
                if "Received a POST request for / from 127.0.0.1" in line:
                    continue

                # Zeitstempel-Extraktion (Emercoin Format: YYYY-MM-DD HH:MM:SS)
                try:
                    ts_str = line[:19]
                    ts = datetime.datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                    if ts < thirty_mins_ago:
                        break
                except:
                    pass  # Zeilen ohne Zeitstempel einbeziehen
                output_lines.append(line)

            self.log_text.config(state="normal")
            self.log_text.delete("1.0", "end")

            for line in reversed(output_lines):
                start_idx = self.log_text.index("end-1c")
                self.log_text.insert("end", line)
                end_idx = self.log_text.index("end-1c")

                # Highlighting Regeln
                l_line = line.lower()
                if "error" in l_line or "disconnecting" in l_line:
                    self.log_text.tag_add("error", start_idx, end_idx)
                elif "updatetip" in l_line:
                    self.log_text.tag_add("block", start_idx, end_idx)
                elif "connection from" in l_line:
                    self.log_text.tag_add("conn", start_idx, end_idx)
                elif "successfully reconstructed block" in l_line:
                    self.log_text.tag_add("recon", start_idx, end_idx)
                elif "accepttomemorypool" in l_line:
                    self.log_text.tag_add("mempool", start_idx, end_idx)
                elif "processsynccheckpoint" in l_line:
                    self.log_text.tag_add("sync", start_idx, end_idx)
                elif "committed" in l_line and "changed transaction outputs" in l_line:
                    self.log_text.tag_add("comm", start_idx, end_idx)

            self.log_text.see("end")
            self.log_text.config(state="disabled")
        except Exception as e:
            print(f"Log Fehler: {e}")

    def update_address_list(self):
        # Hole alle Adressen, die jemals etwas empfangen haben (inkl. 0 Balance)
        addresses = self.call_rpc("listreceivedbyaddress", [0, True])
        self.addr_tree.delete(*self.addr_tree.get_children())

        if addresses:
            for addr in addresses:
                self.addr_tree.insert(
                    "", "end", values=(addr.get("address"), f"{addr.get('amount')} EMC")
                )

    def on_address_select(self, event):
        selected_item = self.addr_tree.selection()
        if not selected_item:
            return

        address = self.addr_tree.item(selected_item[0])["values"][0]
        self.update_transaction_list(address)

    def update_transaction_list(self, address):
        self.tx_tree.delete(*self.tx_tree.get_children())
        # Hole die letzten 100 Transaktionen der Wallet
        txs = self.call_rpc("listtransactions", ["*", 100])

        if txs:
            # Filtere Transaktionen nach der ausgewählten Adresse
            for tx in txs:
                if tx.get("address") == address:
                    self.tx_tree.insert(
                        "",
                        "end",
                        values=(
                            tx.get("category"),
                            f"{tx.get('amount')} EMC",
                            tx.get("confirmations"),
                            tx.get("txid"),
                        ),
                    )

    def on_tx_select(self, event):
        """Zeigt ein vergrößertes Fenster mit allen Transaktionsdetails an."""
        selected_item = self.tx_tree.selection()
        if not selected_item:
            return

        # Die TXID befindet sich in der 4. Spalte (Index 3)
        txid = self.tx_tree.item(selected_item[0])["values"][3]

        # Verschiedene Informationen abrufen
        tx_data = self.call_rpc("gettransaction", [txid])
        # Wir versuchen die rohen Daten inkl. Decodierung (verbose=True) zu bekommen
        raw_tx = self.call_rpc("getrawtransaction", [txid, True])

        if not tx_data and not raw_tx:
            messagebox.showerror(
                "Fehler", "Transaktionsdetails konnten nicht abgerufen werden."
            )
            return

        # Eigenes Fenster statt messagebox erstellen
        tx_win = tk.Toplevel(self.root)
        tx_win.title("Detaillierte Transaktionsinformationen")
        tx_win.geometry("750x650")
        tx_win.configure(bg="#2c3e50")

        # Icon setzen falls vorhanden
        if hasattr(self, "icon_img"):
            tx_win.iconphoto(False, self.icon_img)

        # Frame für Text-Bereich
        frame = tk.Frame(tx_win, bg="#2c3e50")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Text-Widget für die Daten mit kleinerer Schrift (Courier New 9)
        txt_display = tk.Text(
            frame,
            bg="#1e272e",
            fg="#dcdde1",
            font=("Courier New", 9),
            padx=10,
            pady=10,
            wrap="none",
        )

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=txt_display.yview)
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=txt_display.xview)
        txt_display.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        txt_display.pack(side="left", fill="both", expand=True)

        # Inhalt generieren
        content = f"TRANSAKTIONS-ID: {txid}\n"
        content += "=" * 80 + "\n\n"

        if tx_data:
            tx_time = datetime.datetime.fromtimestamp(tx_data.get("time", 0)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            content += f"Zeitpunkt:      {tx_time}\n"
            content += (
                f"Status:         {tx_data.get('confirmations', 0)} Bestätigungen\n"
            )
            content += f"Gesamtbetrag:   {tx_data.get('amount', 0)} EMC\n"
            content += f"Gebühr:         {tx_data.get('fee', '0')} EMC\n"
            content += f"Block-Hash:     {tx_data.get('blockhash', 'N/A')}\n\n"

            content += "Wallet-Details:\n"
            for d in tx_data.get("details", []):
                cat = d.get("category", "N/A").capitalize()
                amt = d.get("amount", 0)
                addr = d.get("address", "N/A")
                content += f"- {cat}: {amt} EMC an {addr}\n"
            content += "\n"

        if raw_tx:
            content += "Technische Daten (getrawtransaction):\n"
            content += "-" * 40 + "\n"
            content += f"Größe (size):   {raw_tx.get('size', 'N/A')} Bytes\n"
            content += f"vSize:          {raw_tx.get('vsize', 'N/A')} vBytes\n"
            content += f"Gewicht:        {raw_tx.get('weight', 'N/A')} units\n"
            content += f"Version:        {raw_tx.get('version', 'N/A')}\n"
            content += f"Locktime:       {raw_tx.get('locktime', 'N/A')}\n\n"

            content += "Vollständiger JSON-Output:\n"
            content += "-" * 40 + "\n"
            content += json.dumps(raw_tx, indent=2)

        txt_display.insert("1.0", content)
        txt_display.config(state="disabled")

        # OK Button zum Schließen
        btn_ok = tk.Button(
            tx_win,
            text="OK",
            command=tx_win.destroy,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
        )
        btn_ok.pack(pady=(0, 15))

    def _get_service_names(self, service_hex_string):
        """
        Konvertiert einen Hex-String der Services (aus getpeerinfo) in eine
        Liste von menschenlesbaren Servicenamen.
        """
        if not service_hex_string:
            return "N/A"

        try:
            services_int = int(service_hex_string, 16)
        except ValueError:
            return "Unknown"

        # Gängige Bitcoin/Emercoin Service-Flags
        service_map = {
            (
                1 << 0
            ): "NODE_NETWORK",  # Full node, kann Blöcke und Transaktionen bereitstellen
            (
                1 << 1
            ): "NODE_GETUTXO",  # Kann UTXOs bereitstellen (deprecated in neueren Bitcoin Core Versionen)
            (
                1 << 2
            ): "NODE_BLOOM",  # Unterstützt Bloom-Filter für Light Clients (deprecated)
            (
                1 << 3
            ): "NODE_WITNESS",  # Unterstützt SegWit (falls relevant für Emercoin)
            (
                1 << 4
            ): "NODE_COMPACT_FILTERS",  # Unterstützt Compact Block Filters (BIP 157/158)
            (
                1 << 5
            ): "NODE_NETWORK_LIMITED",  # Begrenzter Full Node, stellt nur aktuelle Blöcke bereit
            # Hier können weitere Emercoin-spezifische Service-Flags hinzugefügt werden, falls bekannt
        }

        names = [name for flag, name in service_map.items() if services_int & flag]

        if not names and services_int == 0:
            return "None"  # Keine Services beworben
        return (
            ", ".join(names) if names else f"Other ({service_hex_string})"
        )  # Unbekannte Services


if __name__ == "__main__":
    root = tk.Tk()
    app = EmercoinGUI(root)
    root.mainloop()
