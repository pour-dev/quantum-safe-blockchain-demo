"""
Project: Quantum-Safe Blockchain Demonstrator
Module: gui_app.py

Author: Davood Ziaeian-Pour
GitHub: https://github.com/pour-dev
Created: 2026-03-15
License: MIT

Description:
    Graphical user interface for the Quantum-Safe Blockchain demonstration.

    This module implements an interactive dashboard using Tkinter to
    visualize classical blockchain cryptography and post-quantum
    alternatives. It allows users to explore:

    • Classical ECDSA signatures on elliptic curves
    • Simulated quantum attacks based on the Shor principle
    • Post-quantum hash-based Merkle signature schemes
    • Conceptual comparison between classical and quantum-safe systems

Features:
    - Interactive GUI using Tkinter
    - Visualization of ECDSA key generation
    - Simulation of quantum attacks on elliptic curves
    - Demonstration of Merkle signature schemes
    - Educational blockchain security simulation

Dependencies:
    - tkinter
    - pillow (PIL)
    - internal modules:
        elliptic_curve
        quantum_attack
        merkle_signatures

Notes:
    This implementation uses simplified cryptographic models intended
    purely for educational and demonstration purposes. The elliptic
    curve parameters and security assumptions are intentionally reduced
    to make the concepts easier to visualize.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk

from .elliptic_curve import ToyEllipticCurve
from .quantum_attack import QuantumECDLPSimulator
from .merkle_signatures import ToyMerkleSignatureScheme


class QuantumBlockchainDashboard(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master: tk.Tk = master
        self.master.title("Quantum-Safe Blockchain")
        self.master.geometry("1100x700")
        self.master.minsize(1000, 650)

        # Core logic
        self.curve = ToyEllipticCurve()
        self.G = (2, 1)
        self.private_key = None
        self.public_key = None

        self.merkle: ToyMerkleSignatureScheme | None = None
        self.last_sig: dict | None = None

        # Layout
        self._build_layout()

    # ---------------- Layout ----------------
    def _build_layout(self):
        self.master.configure(bg="#f4f6fb")

        # Main grid layout
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=0)
        self.master.columnconfigure(0, weight=0)
        self.master.columnconfigure(1, weight=1)

        # Sidebar (left)
        self.sidebar = tk.Frame(self.master, bg="#1f3b5d", width=220)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        # Content area (right side)
        self.content = tk.Frame(self.master, bg="#ffffff")
        self.content.grid(row=0, column=1, sticky="nswe")
        self.content.grid_propagate(True)
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

        # Output console (bottom)
        self.console_frame = tk.Frame(self.master, bg="#e9edf5", height=180)
        self.console_frame.grid(row=1, column=0, columnspan=2, sticky="nswe")
        self.console_frame.grid_propagate(False)

        self._build_sidebar()
        self._build_console()
        self._build_views()

        # Default view
        self.show_view("overview")

    def _build_sidebar(self):
        title = tk.Label(
            self.sidebar,
            text="QUANTUM-SAFE\nBLOCKCHAIN DEMO",
            bg="#1f3b5d",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            justify="left",
        )
        title.pack(padx=20, pady=(20, 10), anchor="w")

        subtitle = tk.Label(
            self.sidebar,
            text="Interactive\nCryptography Simulation",
            bg="#1f3b5d",
            fg="#c7d4e8",
            font=("Segoe UI", 9),
            justify="left",
        )
        subtitle.pack(padx=20, pady=(0, 20), anchor="w")

        self.nav_buttons = {}

        def add_btn(key, text):
            btn = tk.Button(
                self.sidebar,
                text=text,
                bg="#1f3b5d",
                fg="white",
                activebackground="#27476f",
                activeforeground="white",
                relief="flat",
                anchor="w",
                font=("Segoe UI", 10),
                command=lambda k=key: self.show_view(k),
                padx=20,
                pady=8,
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        add_btn("overview", "🏠 Introduction")
        add_btn("ecdsa", "🔐 ECDSA Signatures")
        add_btn("quantum", "⚛️ Quantum Attack (Shor Principle)")
        add_btn("merkle", "🌲 Merkle Signatures (Post-Quantum)")
        add_btn("compare", "⚖️ Comparison")

    # ---------------- Konsole ----------------
    def _build_console(self):
        label = tk.Label(
            self.console_frame,
            text="Output / Log:",
            bg="#e9edf5",
            fg="#333333",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        )
        label.pack(anchor="w", padx=15, pady=(8, 2))

        self.console_text = scrolledtext.ScrolledText(
            self.console_frame,
            height=10,
            bg="#f7f9ff",
            fg="#222222",
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
        )
        self.console_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self._log("System started. Please select a section from the menu.")

    def _log(self, msg: str):
        self.console_text.insert("end", msg + "\n")
        self.console_text.see("end")

    # ---------------- Views-Container ----------------
    def _build_views(self):
        self.views = {}

        overview = tk.Frame(self.content, bg="white")
        self.views["overview"] = overview
        self._build_overview_view(overview)

        ecdsa = tk.Frame(self.content, bg="white")
        self.views["ecdsa"] = ecdsa
        self._build_ecdsa_view(ecdsa)

        quantum = tk.Frame(self.content, bg="white")
        self.views["quantum"] = quantum
        self._build_quantum_view(quantum)

        merkle = tk.Frame(self.content, bg="white")
        self.views["merkle"] = merkle
        self._build_merkle_view(merkle)

        compare = tk.Frame(self.content, bg="white")
        self.views["compare"] = compare
        self._build_compare_view(compare)

    def show_view(self, key: str):
        for k, frame in self.views.items():
            frame.grid_forget()
        view = self.views.get(key)
        if view:
            view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for k, btn in self.nav_buttons.items():
            btn.configure(bg="#27476f" if k == key else "#1f3b5d")

    # ---------------- Overview  ----------------
    def _build_overview_view(self, frame):
        frame.configure(bg="white")

        # --- TITLE ---
        title = tk.Label(
            frame,
            text="Quantum-Safe Blockchain Demonstration",
            font=("Segoe UI", 24, "bold"),
            bg="white"
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            frame,
            text="Classical ECDSA • Quantum Attacks • Merkle Signatures",
            font=("Segoe UI", 14),
            fg="#444444",
            bg="white"
        )
        subtitle.pack(pady=(0, 20))

        # --- HERO SECTION (two columns) ---
        hero = tk.Frame(frame, bg="white")
        hero.pack(fill="both", expand=True, padx=40, pady=20)

        # LEFT SIDE (TEXT)
        left = tk.Frame(hero, bg="white")
        left.pack(side="left", fill="both", expand=True, padx=(0, 40))

        intro_text = (
            "This application demonstrates the difference between classical and\n"
            "quantum‑safe digital signatures.\n\n"
            "You will explore:\n"
            " • Classical ECDSA and how quantum computers can break it\n"
            " • Quantum attacks simulated with Qiskit, Cirq, and classical methods\n"
            " • Quantum‑safe Merkle signature schemes\n\n"
            "The goal is to understand why post‑quantum cryptography is essential\n"
            "for future blockchain and security systems."
        )

        text_label = tk.Label(
            left,
            text=intro_text,
            bg="white",
            justify="left",
            font=("Segoe UI", 12)
        )
        text_label.pack(anchor="w")
        
        # RIGHT SIDE (IMAGE)
        right = tk.Frame(hero, bg="white")
        right.pack(side="right", fill="both", expand=False)

        from PIL import Image, ImageTk
        img = Image.open("img/intro.jpg")  # image
        img = img.resize((178, 200), Image.LANCZOS)
        self.intro_img = ImageTk.PhotoImage(img)

        img_label = tk.Label(right, image=self.intro_img, bg="white")
        img_label.pack(anchor="e")
        

    # ---------------- ECDSA ----------------
    def _build_ecdsa_view(self, frame):
        tk.Label(
            frame,
            text="ECDSA Signatures - Foundations of Classical Blockchain Cryptography",
            bg="white",
            fg="#1f3b5d",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        text = (
            "Modern blockchains use elliptic curve cryptography (ECDSA) to sign transactions.\n"
            "Security relies on the discrete logarithm problem: given Q = d·G, the private key d cannot be feasibly computed.\n"
            "Hash functions such as SHA-256 link blocks and ensure integrity.\n\n"
            "→ Strong security against classical attackers, but vulnerable to future quantum attacks.\n\n"
            "Note:\n"
            "This simulation uses a highly simplified elliptic curve with order 5.\n"
            "Private keys must therefore be between 1 and 4.\n"
            "This is purely for educational visualization.\n"
        )

        tk.Label(
            frame,
            text=text,
            bg="white",
            fg="#444444",
            font=("Segoe UI", 11),
            justify="left",
            wraplength=800,
        ).pack(anchor="w", pady=(10, 20))

        top = tk.Frame(frame, bg="white")
        top.pack(anchor="w", pady=(0, 10))

        tk.Label(top, text="Private key d:", bg="white", fg="#333333", font=("Segoe UI", 11)).pack(
            side="left", padx=(0, 5)
        )
        self.ecdsa_d_var = tk.StringVar(value="3")
        tk.Entry(top, textvariable=self.ecdsa_d_var, width=8, font=("Segoe UI", 11)).pack(side="left")
        tk.Button(
            top,
            text="Set key",
            command=self._ecdsa_set_key,
            bg="#1f3b5d",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=4,
        ).pack(side="left", padx=10)

        self.ecdsa_q_var = tk.StringVar(value="Q = ( ?, ? )")
        tk.Label(frame, textvariable=self.ecdsa_q_var, bg="white", fg="#222222", font=("Consolas", 11)).pack(
            anchor="w", pady=(5, 10)
        )

    def _ecdsa_set_key(self):
        try:
            d = int(self.ecdsa_d_var.get())
            if d <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer.")
            return
        
        # Warnung bei zu großem Schlüssel (Toy-Kurve hat Ordnung 5)
        if d >= self.curve.order:
            self._log("[HINT] This simulation uses a very small elliptic curve with order 5.")
            self._log("→ Private keys must be between 1 and 4.")
            self._log("→ Larger values are mathematically identical modulo 5 and therefore invalid.")


        self.private_key = d
        self.public_key = self.curve.mul(self.G, d)
        self.ecdsa_q_var.set(f"Q = {self.public_key}")
        self._log(f"[ECDSA] Key set: d = {d}, Q = {self.public_key}")

        self._log(f"[INFO] ECDSA key set.")
        self._log(f"-> This corresponds to the standard used in blockchain systems (e.g., Bitcoin, Ethereum).")
        self._log(f"-> Strong against classical attacks, but NOT against quantum computers.")


    # ---------------- Quantenangriff ----------------
    def _build_quantum_view(self, frame):
        tk.Label(
            frame,
            text="Quantum Attack - Recovering the Private Key (Shor Principle)",
            bg="white",
            fg="#b3261e",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        # Backend indicator label
        self.backend_var = tk.StringVar(value="Backend: Not initialized")
        self.backend_var_label = tk.Label(
            frame,
            textvariable=self.backend_var,
            bg="white",
            fg="#1b5e20",
            font=("Segoe UI", 12, "bold")
        )
        self.backend_var_label.pack(anchor="w", pady=(5, 10))
        
        text = (
            "Quantum computers use superposition, entanglement, "
            "and interference to solve certain problems exponentially faster.\n"
            "The Shor algorithm can efficiently solve the discrete logarithm problem.\n\n"
            "→ A sufficiently powerful quantum computer could completely break ECDSA.\n"
            "→ Private keys would become recoverable.\n\n"
            "This simulation demonstrates the mathematical principle of the Shor algorithm using a simplified elliptic curve."
        )
        tk.Label(
            frame,
            text=text,
            bg="white",
            fg="#444444",
            font=("Segoe UI", 11),
            justify="left",
            wraplength=800,
        ).pack(anchor="w", pady=(10, 20))

        tk.Button(
            frame,
            text="Simulate Quantum Attack",
            command=self._run_quantum_attack,
            bg="#b3261e",
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=6,
        ).pack(anchor="w", pady=(0, 10))

        self.quantum_result_var = tk.StringVar(value="No attack performed yet.")
        tk.Label(
            frame,
            textvariable=self.quantum_result_var,
            bg="white",
            fg="#222222",
            font=("Segoe UI", 11),
            wraplength=800,
        ).pack(anchor="w", pady=(10, 10))

    def _run_quantum_attack(self):
        if self.private_key is None or self.public_key is None:
            messagebox.showerror("Error", "Please set an ECDSA key first.")
            return

        sim = QuantumECDLPSimulator(self.curve, self.G, self.public_key)
        d_found, backend = sim.run_attack()

        # Update backend indicator
        self.backend_var.set(f"Backend: {backend}")

        # Optional: color coding
        if backend == "Qiskit":
            color = "#0b8043"   # green
        elif backend == "Cirq":
            color = "#f9a825"   # yellow
        else:
            color = "#616161"   # gray

        self.backend_var_label.config(fg=color)

        if d_found == self.private_key:
            msg = (
                f"Quantum attack successful!\n"
                f"Recovered private key: d = {d_found}\n"
                f"→ In this simulation, the security is broken."
            )
            self.quantum_result_var.set(msg)
            self._log(f"[QUANTUM] Attack successful, d = {d_found}")

            self._log(f"[SECURITY] ECDSA was broken by the simulated quantum attack.")
            # Mini blockchain simulation for ECDSA
            self._simulate_ecdsa_block(d_found)

        else:
            msg = (
                "Attack failed.\n"
                "In real systems, a sufficiently large quantum computer would break ECDSA."
            )
            self.quantum_result_var.set(msg)
            self._log("[QUANTUM] Attack not successful.")

            self._log("[INFO] Attack failed in this simulation.")
            self._log("-> In real systems, a sufficiently large quantum computer would break ECDSA.")


    def _simulate_ecdsa_block(self, d_found: int):
        self._log("[BLOCKCHAIN] Simulating ECDSA block.")
        self._log(" • Transaction was signed using classical ECDSA.")
        self._log(f" • Quantum attack recovered the private key: d = {d_found}")
        self._log(" • → Block is compromised and would be rejected in a blockchain.")
        self._log(" • Classical signatures are NOT quantum-safe.")


    def _enter_quantum_safe_mode(self):
        self._log("[MODE] Quantum-Safe Mode activated.")
        self._log(" • Classical ECDSA signatures are vulnerable to quantum attacks.")
        self._log(" • Hash-based Merkle signatures provide post-quantum-oriented security.")
        self._log(" • All signed transactions are now protected against Shor-type attacks.")


    # ---------------- Merkle signatures ----------------
    def _build_merkle_view(self, frame):
        tk.Label(
            frame,
            text="Quantum-Safe Signatures - Hash-Based Merkle Signatures",
            bg="white",
            fg="#1b5e20",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        text = (
        "Hash-based signatures are considered post-quantum secure "
        "because no efficient quantum attacks on hash functions are known.\n\n"
        "Merkle trees enable the scaling of many one-time signature (OTS) keys "
        "into a single compact public key (the Merkle root).\n\n"
        "→ Suitable for quantum-safe blockchain designs\n"
        "→ No elliptic curves involved\n"
        "→ Not vulnerable to Shor-like attacks"
        )

        tk.Label(
            frame,
            text=text,
            bg="white",
            fg="#444444",
            font=("Segoe UI", 11),
            justify="left",
            wraplength=800,
        ).pack(anchor="w", pady=(10, 20))

        # Number of OTS keys
        top = tk.Frame(frame, bg="white")
        top.pack(anchor="w", pady=(0, 10))

        tk.Label(top, text="Number of OTS keys:", bg="white", fg="#333333", font=("Segoe UI", 11)).pack(
            side="left", padx=(0, 5)
        )
        self.merkle_num_var = tk.StringVar(value="4")
        tk.Entry(top, textvariable=self.merkle_num_var, width=6, font=("Segoe UI", 11)).pack(side="left")
        tk.Button(
            top,
            text="Generate system",
            command=self._init_merkle,
            bg="#1b5e20",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=4,
        ).pack(side="left", padx=10)

        # Root
        self.merkle_root_var = tk.StringVar(value="Merkle Root: (not generated yet)")
        tk.Label(
            frame,
            textvariable=self.merkle_root_var,
            bg="white",
            fg="#222222",
            font=("Consolas", 10),
            wraplength=800,
        ).pack(anchor="w", pady=(5, 10))

        # Message
        msg_row = tk.Frame(frame, bg="white")
        msg_row.pack(anchor="w", pady=(5, 5))
        tk.Label(msg_row, text="Message:", bg="white", fg="#333333", font=("Segoe UI", 11)).pack(
            side="left", padx=(0, 5)
        )

        # Single-line text field (Text widget)
        self.merkle_msg_text = tk.Text(
            msg_row,
            width=50,
            height=1,
            font=("Segoe UI", 10),
            wrap="none",
        )
        self.merkle_msg_text.pack(side="left")

        # Buttons
        btn_row = tk.Frame(frame, bg="white")
        btn_row.pack(anchor="w", pady=(5, 10))
        tk.Button(
            btn_row,
            text="Sign",
            command=self._merkle_sign,
            bg="#1b5e20",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=4,
        ).pack(side="left", padx=(0, 10))
        tk.Button(
            btn_row,
            text="Verify",
            command=self._merkle_verify,
            bg="#1b5e20",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=4,
        ).pack(side="left")

        # Signature info
        self.merkle_sig_info_var = tk.StringVar(value="")
        tk.Label(
            frame,
            textvariable=self.merkle_sig_info_var,
            bg="white",
            fg="#222222",
            font=("Segoe UI", 10),
            wraplength=800,
        ).pack(anchor="w", pady=(10, 5))

        # Verification
        self.merkle_verify_var = tk.StringVar(value="No verification performed yet.")
        tk.Label(
            frame,
            textvariable=self.merkle_verify_var,
            bg="white",
            fg="#222222",
            font=("Segoe UI", 10, "bold"),
            wraplength=800,
        ).pack(anchor="w", pady=(5, 0))

    def _init_merkle(self):
        try:
            n = int(self.merkle_num_var.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer.")
            return

        # Create new Merkle system
        self.merkle = ToyMerkleSignatureScheme(n)
        self.last_sig = None

        # Update root display
        self.merkle_root_var.set(f"Merkle-Root: {self.merkle.root.hex()}")

        # Reactivate the Sign button
        for child in self.views["merkle"].winfo_children():
            if isinstance(child, tk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, tk.Button) and btn.cget("text") == "Sign":
                        btn.config(state="normal", bg="#1b5e20", fg="white")

        self._log(f"[MERKLE] New system generated with {n} OTS keys.")
        self._log(f"[MERKLE] Merkle-Root: {self.merkle.root.hex()}")

        self._enter_quantum_safe_mode()



    def _merkle_sign(self):
        if self.merkle is None:
            messagebox.showerror("Error", "Please generate the Merkle system first.")
            return

        msg = self.merkle_msg_text.get("1.0", "end").strip().encode("utf-8")
        if not msg:
            messagebox.showerror("Error", "Please enter a message.")
            return

        try:
            sig = self.merkle.sign(msg)

        except IndexError:
            # All OTS keys used → disable button + popup
            messagebox.showwarning(
                "OTS Keys Exhausted",
                "All one-time signature keys have been used.\n"
                "Please generate a new Merkle system."
            )

            self._log("[MERKLE] ERROR: All OTS keys have been used.")
            self._log("→ Please generate a new Merkle system.")

            # Disable Sign button visually
            for child in self.views["merkle"].winfo_children():
                if isinstance(child, tk.Frame):
                    for btn in child.winfo_children():
                        if isinstance(btn, tk.Button) and btn.cget("text") == "Sign":
                            btn.config(state="disabled", bg="#777777", fg="#cccccc")
            return

        # Save last signature
        self.last_sig = sig

        # Log signature details
        pk0, pk1 = sig["pk"]
        self._log("[MERKLE] Message signed:")
        self._log(f"  • OTS index: {sig['index']}")
        self._log(f"  • OTS public key: ({pk0.hex()},{pk1.hex()})")
        self._log(f"  • Signature fragments: {len(sig['sig'])} revealed values")

        # If last OTS key was used → disable button
        if sig["index"] + 1 >= self.merkle.num_keys:
            self._log("[MERKLE] Note: All OTS keys are now used.")
            self._log("→ Please generate a new Merkle system.")

            messagebox.showwarning(
                "OTS Keys Exhausted",
                "All one-time signature keys have now been used.\n"
                "Please generate a new Merkle system."
            )

            # Disable Sign button visually
            for child in self.views["merkle"].winfo_children():
                if isinstance(child, tk.Frame):
                    for btn in child.winfo_children():
                        if isinstance(btn, tk.Button) and btn.cget("text") == "Sign":
                            btn.config(state="disabled", bg="#777777", fg="#cccccc")

    def _merkle_verify(self):
        if self.merkle is None or self.last_sig is None:
            messagebox.showerror("Error", "No signature available yet.")
            return

        msg = self.merkle_msg_text.get("1.0", "end").strip().encode("utf-8")
        if not msg:
            messagebox.showerror("Error", "Please enter a message.")
            return

        root_text = self.merkle_root_var.get().replace("Merkle-Root:", "").strip()
        try:
            root = bytes.fromhex(root_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid Merkle root.")
            return

        ok = ToyMerkleSignatureScheme.verify(root, msg, self.last_sig)

        if ok:
            self._log("[MERKLE] Verification SUCCESSFUL - signature is valid.")
            self._simulate_blockchain_transaction(msg)
        else:
            self._log("[MERKLE] Verification FAILED - invalid signature or Merkle path.")

    def _simulate_blockchain_transaction(self, msg_bytes: bytes):
        try:
            msg_text = msg_bytes.decode("utf-8")
        except Exception:
            msg_text = repr(msg_bytes)

        self._log("[BLOCKCHAIN] Simulating new block.")
        self._log(f" • Transaction: {msg_text}")
        self._log(" • Signature valid → Block accepted.")
        self._log(" • This transaction would be protected in a quantum-safe blockchain.")

    # ---------------- Comparison ----------------
    def _build_compare_view(self, frame):
        tk.Label(
            frame,
            text="Comparison: Classical ECDSA vs. Quantum Attack vs. Merkle",
            bg="white",
            fg="#1f3b5d",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        text = (
            "This view compares three cryptographic approaches:\n"
            "• Classical ECDSA signatures\n"
            "• Quantum attacks based on the Shor principle\n"
            "• Hash-based Merkle signatures as a post-quantum alternative\n\n"
            "The visualization shows why classical signatures are at long-term risk\n"
            "and how Merkle signatures provide a quantum-resistant solution."
        )
        tk.Label(
            frame,
            text=text,
            bg="white",
            fg="#444444",
            font=("Segoe UI", 11),
            justify="left",
            wraplength=800,
        ).pack(anchor="w", pady=(10, 20))

        # Container für Canvas + Scrollbars
        canvas_container = tk.Frame(frame, bg="white")
        canvas_container.pack(fill="both", expand=True)

        # Scrollbars
        x_scroll = tk.Scrollbar(canvas_container, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll = tk.Scrollbar(canvas_container, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        # Canvas
        canvas = tk.Canvas(
            canvas_container,
            bg="white",
            highlightthickness=0,
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set,
        )
        canvas.pack(side="left", fill="both", expand=True)

        x_scroll.config(command=canvas.xview)
        y_scroll.config(command=canvas.yview)

        # Inhalt zeichnen
        width, height = 800, 500
        canvas.configure(scrollregion=(0, 0, width, height))

        # Linke Seite: Klassische ECDSA
        canvas.create_rectangle(40, 60, 320, 280, outline="#1f3b5d", width=2)
        canvas.create_text(180, 75, text="Classical ECDSA", font=("Segoe UI", 11, "bold"), fill="#1f3b5d")
        canvas.create_text(
            180,
            120,
            text="Q = d · G\nElliptic curve\nClassical attacker:\n'd' infeasible to compute",
            font=("Segoe UI", 9),
            fill="#333333",
        )
        canvas.create_rectangle(70, 190, 290, 260, fill="#9e9e9e", outline="#616161")
        canvas.create_text(180, 225, text="Massive wall\n(Classical security)", font=("Segoe UI", 9), fill="white")

        # Rechte Seite: Quantum attack
        canvas.create_rectangle(380, 60, 660, 280, outline="#b3261e", width=2)
        canvas.create_text(520, 75, text="Quantum Attack (Shor)", font=("Segoe UI", 11, "bold"), fill="#b3261e")
        canvas.create_text(
            520,
            120,
            text="Wavefunction over many states\nShor finds period 'r'\nFrom 'r' → compute d",
            font=("Segoe UI", 9),
            fill="#333333",
        )
        canvas.create_oval(430, 190, 610, 260, outline="#b3261e", width=2)
        canvas.create_text(520, 225, text="Period 'r' found!\n→ d compromised", font=("Segoe UI", 9), fill="#b3261e")

        # Untere Box: Merkle
        canvas.create_rectangle(120, 300, 580, 380, outline="#1b5e20", width=2)
        canvas.create_text(
            350,
            315,
            text="Merkle / Hash-Based Signatures",
            font=("Segoe UI", 11, "bold"),
            fill="#1b5e20",
        )
        canvas.create_text(
            350,
            345,
            text="No elliptic curve, only hashes (SHA-256)\n→ Post-quantum-oriented security",
            font=("Segoe UI", 9),
            fill="#333333",
        )


# ---------------- run_app ----------------
def run_app():
    root = tk.Tk()
    app = QuantumBlockchainDashboard(root)
    root.mainloop()
