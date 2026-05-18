import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

# --- KONFIGURATION ---
RPC_USER = "emma"
RPC_PASS = "testnetemma"
RPC_URL = "http://127.0.0.1:16662"  # Standard-Testnet-Port


class EmercoinGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emercoin Testnet Dashboard")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")

        # UI Styling
        style = ttk.Style()
        style.configure(
            "TLabel", background="#2c3e50", foreground="white", font=("Arial", 11)
        )
        style.configure("Header.TLabel", font=("Arial", 16, "bold"))

        # Header
        self.header = ttk.Label(
            root, text="Emercoin Wallet Status", style="Header.TLabel"
        )
        self.header.pack(pady=20)

        # Info Frame
        info_frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Datenfelder
        self.balance_label = self.create_info_row(info_frame, "Kontostand:", "Lädt...")
        self.blocks_label = self.create_info_row(info_frame, "Blöcke:", "Lädt...")
        self.version_label = self.create_info_row(info_frame, "Version:", "Lädt...")
        self.connection_label = self.create_info_row(info_frame, "Status:", "Prüfe...")

        # Refresh Button
        self.refresh_btn = tk.Button(
            root,
            text="Daten aktualisieren",
            command=self.update_data,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=5,
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
            self.blocks_label.config(text=blockchain_info.get("blocks"))

        # Network Info
        network_info = self.call_rpc("getnetworkinfo")
        if network_info:
            self.version_label.config(text=network_info.get("version"))


if __name__ == "__main__":
    root = tk.Tk()
    app = EmercoinGUI(root)
    root.mainloop()
