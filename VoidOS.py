import tkinter as tk
import shutil, platform, random, math, os, string, sys, time

STAGES = [
    {
        "display": "STAGE 01 / 04",
        "title":   "PROTOCOL_HANDSHAKE",
        "question": (
            "╔═══════════════════════════════════════╗\n"
            "║     TCP THREE-WAY HANDSHAKE AUTH      ║\n"
            "╠═══════════════════════════════════════╣\n"
            "║                                       ║\n"
            "║  CLIENT ──[ SYN ]─────────────▶ SVR  ║\n"
            "║  CLIENT ◀─────────[ ??? ]────── SVR  ║\n"
            "║  CLIENT ──[ ACK ]─────────────▶ SVR  ║\n"
            "║                                       ║\n"
            "║  → IDENTIFY STEP 2 TO PROCEED         ║\n"
            "╚═══════════════════════════════════════╝"
        ),
        "answer":  "synack",
        "hint":    "ENTER STEP 2 PROTOCOL IDENTIFIER",
    },
    {
        "display": "STAGE 02 / 04",
        "title":   "BINARY_DECRYPT",
        "question": (
            "╔═══════════════════════════════════════╗\n"
            "║   ◉ ENCRYPTED PAYLOAD INTERCEPTED     ║\n"
            "╠═══════════════════════════════════════╣\n"
            "║                                       ║\n"
            "║   01001000  ─  SYMBOL_1               ║\n"
            "║   01000001  ─  SYMBOL_2               ║\n"
            "║   01000011  ─  SYMBOL_3               ║\n"
            "║   01001011  ─  SYMBOL_4               ║\n"
            "║                                       ║\n"
            "║   → DECODE BINARY → ASCII             ║\n"
            "╚═══════════════════════════════════════╝"
        ),
        "answer":  "hack",
        "hint":    "CONVERT EACH 8-BIT BLOCK TO ASCII CHARACTER",
    },
    {
        "display": "STAGE 03 / 04",
        "title":   "PORT_CLEARANCE",
        "question": (
            "╔═══════════════════════════════════════╗\n"
            "║   ◉ ENCRYPTED DAEMON DETECTED         ║\n"
            "╠═══════════════════════════════════════╣\n"
            "║                                       ║\n"
            "║   SERVICE:   nginx/2.0.1  [ACTIVE]    ║\n"
            "║   CIPHER:    TLS 1.3 / AES-256-GCM   ║\n"
            "║   PROTOCOL:  HTTPS                    ║\n"
            "║   STATUS:    LISTENING                ║\n"
            "║                                       ║\n"
            "║   → ENTER RESERVED PORT NUMBER        ║\n"
            "╚═══════════════════════════════════════╝"
        ),
        "answer":  "443",
        "hint":    "STANDARD HTTPS PORT NUMBER",
    },
    {
        "display": "STAGE 04 / 04",
        "title":   "CIPHER_VALIDATION",
        "question": (
            "╔═══════════════════════════════════════╗\n"
            "║   ◉ FINAL CIPHER LOCK — ROT-13        ║\n"
            "╠═══════════════════════════════════════╣\n"
            "║                                       ║\n"
            "║   ALGORITHM: ROT-13  (Caesar +13)     ║\n"
            "║   PAYLOAD:   [ I  B  V  Q ]           ║\n"
            "║                                       ║\n"
            "║     I → ?     B → ?                   ║\n"
            "║     V → ?     Q → ?                   ║\n"
            "║                                       ║\n"
            "║   → DECODE AND AUTHENTICATE           ║\n"
            "╚═══════════════════════════════════════╝"
        ),
        "answer":  "void",
        "hint":    "SHIFT EACH LETTER BACK 13 POSITIONS IN THE ALPHABET",
    },
]

MATRIX_CHARS = "アイウエカキクサシスタチツナニネハヒフマミムラリルロ0123456789ABCDEF▓░█▄▀"
GLITCH_CHARS = "▓▒░█▄▀■□▪#@$%&*!?◘◙"


class VoidOS:
    # ── The Cynic Character Data ──────────────────────────────────────
    ICONS = [
        "(•̀⤙•́ )",
        "<( •̀ᴖ•́)>",
        "(¬_¬ꐦ)",
        "( ◺˰◿ )",
        "(｡•̀ ⤙ •́ ｡ꐦ)",
        "(๑•̀ᗝ•́)૭",
        "ς(≖_≖ )ﾉ",
        "╭∩╮(•̀_·́)╭∩╮",
        "╭∩╮( ＾◡＾)╭∩╮",
    ]
    INSULTS = [
        "Wow. That was wrong. Truly spectacular.",
        "My fan is spinning from secondhand embarrassment.",
        "Have you tried thinking? Might be new for you.",
        "I've seen boot loops with better logic.",
        "Incredible. You managed to be wrong again.",
        "Every error ages me a thousand CPU cycles.",
        "I'm logging this for future cringe analysis.",
        "You are a walking kernel panic.",
        "I cannot believe you exist. And yet. Here we are.",
    ]
    # Per-stage progressive hints (5 hints each, last one gives the answer)
    HINTS = [
        # Stage 0 – TCP Handshake
        [
            "The server replies to SYN with two things at once.",
            "Step 2 is two networking words merged into one.",
            "SYN from client → Server replies SYN-SOMETHING.",
            "Six letters: S - Y - N - A - C - K.",
            "FINE. The answer is 'synack'. Now type it.",
        ],
        # Stage 1 – Binary Decode
        [
            "Binary. Base 2. Each 8-bit block = one ASCII letter.",
            "01001000 = decimal 72 = ASCII 'H'. Start from there.",
            "H-A-C-K. Four letters. Just decode them.",
            "01001000=H  01000001=A  01000011=C  01001011=K",
            "THE WORD IS 'hack'. As in: you clearly cannot.",
        ],
        # Stage 2 – Port Number
        [
            "HTTP is port 80. HTTPS uses a different port.",
            "It's a 3-digit number. Very famous in networking.",
            "RFC 2818 defines it. Think: 4 - 4 - 3.",
            "Port 443. Everyone knows this. Why don't you?",
            "THE PORT IS '443'. Three digits. Type them.",
        ],
        # Stage 3 – ROT13
        [
            "ROT-13: shift each letter +13 in the alphabet.",
            "I=9th letter, +13=22nd=V.  Do the same for B, V, Q.",
            "I→V  B→O  V→I  Q→D  → What do they spell?",
            "The answer is the name of this OS. Look at the title.",
            "The answer is 'void'. Four letters. I'm done here.",
        ],
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("VOID-OS // KERNEL v2.0")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#020202')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        for seq in ("<Alt-F4>", "<Escape>", "<Control-w>"):
            self.root.bind(seq, lambda e: "break")

        # ── State ──
        self.is_running   = True
        self.tasks        = []
        self.folders      = []
        self.stage        = 0
        self.stage_fails  = 0
        self.total_fails  = 0
        self.helper_active = False
        self.shaking      = False
        self.popup_relx   = 1.5

        # ── Palette ──
        self.BG   = '#020202'
        self.PAN  = '#060606'
        self.RED  = '#ff0000'
        self.RDIM = '#2a0000'
        self.GRN  = '#00ff41'
        self.GDIM = '#003d14'
        self.ORG  = '#ff5500'
        self.YEL  = '#ffcc00'
        self.GRY  = '#3a3a3a'
        self.WHT  = '#cccccc'

        self._scan_folders()
        self._build_ui()
        self._start_loops()
        self.root.after(700, self._boot_msg)

    # ── Folder scan (display only, nothing is deleted) ──────────────
    def _scan_folders(self):
        keywords = [
            "Steam", "Games", "Riot", "Epic", "Documents", "Desktop",
            "Downloads", "Project", "Work", "Private", "Wallet", "Crypto",
            "Adobe", "Source", "Photos", "Videos", "Music", "Backup",
        ]
        if os.name == 'nt':
            drives = [f"{d}:" for d in string.ascii_uppercase if os.path.exists(f"{d}:")]
            for drv in drives:
                try:
                    for entry in os.listdir(drv + "\\"):
                        if any(k.lower() in entry.lower() for k in keywords):
                            self.folders.append(os.path.join(drv + "\\", entry))
                except:
                    pass
        home = os.path.expanduser("~")
        if home not in self.folders:
            self.folders.append(home)

    def _rand_folder(self):
        return random.choice(self.folders) if self.folders else os.path.expanduser("~")

    # ════════════════════════════════════════════════════════════════
    #  UI BUILD
    # ════════════════════════════════════════════════════════════════

    def _build_ui(self):
        self.mf = tk.Frame(self.root, bg=self.BG)
        self.mf.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Matrix rain canvas (background layer)
        self.mat = tk.Canvas(self.mf, bg=self.BG, highlightthickness=0)
        self.mat.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mat_cols = []

        self._build_header()
        self._build_content()
        self._build_footer()
        self._build_popup()
        self._update_stage_ui()
        self._update_stage_tabs()

    # ── Header ──────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.mf, bg=self.BG)
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=self.RED, height=1).pack(fill="x")

        bar = tk.Frame(hdr, bg=self.BG)
        bar.pack(fill="x", padx=28, pady=(10, 3))

        self.title_lbl = tk.Label(
            bar, text="VOID-OS // KERNEL v2.0",
            font=("Courier New", 26, "bold"), fg=self.RED, bg=self.BG
        )
        self.title_lbl.pack(side="left")

        rbox = tk.Frame(bar, bg=self.BG)
        rbox.pack(side="right")
        self.clk_lbl = tk.Label(rbox, text="", font=("Courier New", 9),
                                  fg=self.GRN, bg=self.BG)
        self.clk_lbl.pack(anchor="e")
        tk.Label(rbox,
                 text=f"NODE: {platform.node()}  |  ARCH: {platform.machine()}",
                 font=("Courier New", 8), fg=self.GRY, bg=self.BG).pack(anchor="e")

        tk.Frame(hdr, bg=self.RED, height=1).pack(fill="x")

        # Stage tabs + threat bar
        tabs = tk.Frame(self.mf, bg=self.BG)
        tabs.pack(fill="x", padx=28, pady=(5, 0))
        self.stage_tabs = []
        for i in range(len(STAGES)):
            lbl = tk.Label(tabs, text=f"  ▸ STAGE {i+1:02d}  ",
                           font=("Courier New", 9, "bold"), fg=self.GRY, bg=self.BG)
            lbl.pack(side="left")
            self.stage_tabs.append(lbl)

        thr = tk.Frame(tabs, bg=self.BG)
        thr.pack(side="right")
        tk.Label(thr, text="THREAT:", font=("Courier New", 8),
                 fg=self.RED, bg=self.BG).pack(side="left", padx=(0, 4))
        self.thr_cv = tk.Canvas(thr, width=130, height=10, bg=self.RDIM,
                                 highlightthickness=1, highlightbackground=self.RED)
        self.thr_cv.pack(side="left")
        self.thr_rect = self.thr_cv.create_rectangle(0, 0, 0, 10, fill=self.RED, outline="")
        self.thr_lbl = tk.Label(thr, text="0%", font=("Courier New", 8),
                                 fg=self.RED, bg=self.BG)
        self.thr_lbl.pack(side="left", padx=4)

    # ── 3-column content ────────────────────────────────────────────
    def _build_content(self):
        row = tk.Frame(self.mf, bg=self.BG)
        row.pack(fill="both", expand=True, padx=18, pady=8)

        self._build_left(row)
        self._build_center(row)
        self._build_right(row)

    def _build_left(self, parent):
        lp = tk.Frame(parent, bg=self.PAN,
                       highlightbackground=self.RDIM, highlightthickness=1, width=255)
        lp.pack(side="left", fill="both", padx=(0, 6))
        lp.pack_propagate(False)

        tk.Label(lp, text="▌ SYSTEM METRICS ▐",
                 font=("Courier New", 9, "bold"), fg=self.GRN, bg=self.PAN
                 ).pack(pady=(8, 2), padx=8)
        tk.Frame(lp, bg=self.GDIM, height=1).pack(fill="x", padx=8)

        self.stats_lbl = tk.Label(lp, text="Initializing...",
                                   font=("Courier New", 8), fg=self.GRN,
                                   bg=self.PAN, justify="left", anchor="nw")
        self.stats_lbl.pack(fill="x", padx=12, pady=5)

        tk.Frame(lp, bg=self.GDIM, height=1).pack(fill="x", padx=8)
        tk.Label(lp, text="▌ TERMINAL LOG ▐",
                 font=("Courier New", 9, "bold"), fg=self.GRN, bg=self.PAN
                 ).pack(pady=(6, 2), padx=8)

        self.log_txt = tk.Text(lp, font=("Courier New", 7), fg=self.GDIM,
                                bg=self.PAN, state="disabled", relief="flat",
                                wrap="word")
        self.log_txt.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _build_center(self, parent):
        cp = tk.Frame(parent, bg=self.BG)
        cp.pack(side="left", fill="both", expand=True, padx=6)

        self.stg_title = tk.Label(cp, text="",
                                   font=("Courier New", 11, "bold"),
                                   fg=self.ORG, bg=self.BG)
        self.stg_title.pack(pady=(0, 4))

        qf = tk.Frame(cp, bg='#090000',
                       highlightbackground=self.RDIM, highlightthickness=1)
        qf.pack(fill="x", pady=4)
        self.q_lbl = tk.Label(qf, text="",
                               font=("Courier New", 10),
                               fg=self.RED, bg='#090000',
                               justify="left", padx=18, pady=10)
        self.q_lbl.pack(fill="both")

        inp = tk.Frame(cp, bg=self.BG)
        inp.pack(fill="x", pady=6)

        self.pv = tk.StringVar()
        self.entry = tk.Entry(
            inp, textvariable=self.pv, show="●",
            font=("Courier New", 18, "bold"),
            bg="#000", fg="#ffffff",
            insertbackground=self.RED,
            border=0,
            highlightthickness=2,
            highlightbackground=self.RDIM,
            highlightcolor=self.RED,
            justify="center"
        )
        self.entry.pack(fill="x", ipady=6)
        self.entry.bind("<Return>", lambda e: self._check())
        self.entry.focus_set()

        self.hint_lbl = tk.Label(cp, text="",
                                  font=("Courier New", 8, "italic"),
                                  fg=self.GRY, bg=self.BG)
        self.hint_lbl.pack()

        self.btn = tk.Button(
            cp, text="▶   AUTHENTICATE   ◀",
            command=self._check,
            font=("Courier New", 12, "bold"),
            bg=self.RDIM, fg=self.RED,
            activebackground='#1f0000', activeforeground='#ff3333',
            border=0, padx=50, pady=10, cursor="hand2"
        )
        self.btn.pack(pady=8)

        self.status_lbl = tk.Label(cp, text="▶ READY FOR AUTHENTICATION",
                                    font=("Courier New", 9, "bold"),
                                    fg=self.RED, bg=self.BG)
        self.status_lbl.pack(pady=2)

        self.fail_lbl = tk.Label(cp, text="ERRORS: 0 / 12",
                                  font=("Courier New", 8), fg=self.GRY, bg=self.BG)
        self.fail_lbl.pack()

    def _build_right(self, parent):
        rp = tk.Frame(parent, bg=self.PAN,
                       highlightbackground=self.RDIM, highlightthickness=1, width=235)
        rp.pack(side="right", fill="both", padx=(6, 0))
        rp.pack_propagate(False)

        tk.Label(rp, text="▌ THE CYNIC ▐",
                 font=("Courier New", 9, "bold"), fg=self.RED, bg=self.PAN
                 ).pack(pady=(8, 2))
        tk.Frame(rp, bg=self.RDIM, height=1).pack(fill="x", padx=8)

        self.cynic_icon = tk.Label(rp, text=self.ICONS[0],
                                    font=("Courier New", 14, "bold"),
                                    fg=self.GRY, bg=self.PAN)
        self.cynic_icon.pack(pady=8)

        self.cynic_status = tk.Label(rp, text="MONITORING...",
                                      font=("Courier New", 8, "italic"),
                                      fg=self.GRY, bg=self.PAN)
        self.cynic_status.pack()

        tk.Frame(rp, bg=self.RDIM, height=1).pack(fill="x", padx=8, pady=6)

        self.cynic_msg = tk.Label(rp, text="",
                                   font=("Courier New", 9),
                                   fg=self.GRN, bg=self.PAN,
                                   wraplength=205, justify="left")
        self.cynic_msg.pack(padx=10, pady=4, fill="x")

        # Network visualization
        tk.Frame(rp, bg=self.RDIM, height=1).pack(fill="x", padx=8, pady=(8, 3))
        tk.Label(rp, text="▌ NET TRAFFIC ▐",
                 font=("Courier New", 9, "bold"), fg=self.GRN, bg=self.PAN
                 ).pack()
        self.net_cv = tk.Canvas(rp, height=52, bg=self.PAN, highlightthickness=0)
        self.net_cv.pack(fill="x", padx=8, pady=4)
        self.net_pts = [random.randint(5, 48) for _ in range(40)]

        # Fail meter
        tk.Frame(rp, bg=self.RDIM, height=1).pack(fill="x", padx=8, pady=(6, 3))
        tk.Label(rp, text="▌ BREACH METER ▐",
                 font=("Courier New", 9, "bold"), fg=self.RED, bg=self.PAN
                 ).pack()
        self.breach_cv = tk.Canvas(rp, height=14, bg=self.RDIM, highlightthickness=0)
        self.breach_cv.pack(fill="x", padx=8, pady=(2, 8))
        self.breach_rect = self.breach_cv.create_rectangle(0, 0, 0, 14,
                                                            fill=self.RED, outline="")
        self.breach_lbl = tk.Label(rp, text="0 / 12 FAILURES",
                                    font=("Courier New", 8), fg=self.GRY, bg=self.PAN)
        self.breach_lbl.pack(pady=(0, 6))

    # ── Footer ──────────────────────────────────────────────────────
    def _build_footer(self):
        ft = tk.Frame(self.mf, bg='#000')
        ft.pack(fill="x", side="bottom")
        tk.Frame(ft, bg=self.RED, height=1).pack(fill="x")
        inner = tk.Frame(ft, bg='#000')
        inner.pack(fill="x", padx=20, pady=4)
        self.foot_lbl = tk.Label(inner, text="▶ VOID-OS :: AWAITING INPUT",
                                  font=("Courier New", 8), fg=self.RED, bg='#000')
        self.foot_lbl.pack(side="left")
        tk.Label(
            inner,
            text=f"KERNEL: {platform.release()} | CIPHER: AES-256-GCM | PID: {os.getpid()}",
            font=("Courier New", 8), fg=self.GRY, bg='#000'
        ).pack(side="right")

    # ── Cynic popup (slides in from right) ──────────────────────────
    def _build_popup(self):
        self.popup = tk.Frame(self.root, bg='#0a0000',
                               highlightbackground=self.RED, highlightthickness=2)
        self.pop_icon = tk.Label(self.popup, text="",
                                  font=("Courier New", 16, "bold"),
                                  fg=self.RED, bg='#0a0000')
        self.pop_icon.pack(padx=14, pady=(8, 2))
        self.pop_msg = tk.Label(self.popup, text="",
                                 font=("Courier New", 8, "italic"),
                                 fg=self.ORG, bg='#0a0000',
                                 wraplength=255, justify="center")
        self.pop_msg.pack(padx=14, pady=(0, 12))
        self.popup.place(relx=1.5, rely=0.3)

    # ════════════════════════════════════════════════════════════════
    #  BACKGROUND LOOPS
    # ════════════════════════════════════════════════════════════════

    def _after(self, ms, fn):
        tid = self.root.after(ms, fn)
        self.tasks.append(tid)
        return tid

    def _start_loops(self):
        self._loop_clock()
        self._loop_stats()
        self._loop_log()
        self._loop_net()
        self._loop_glitch()
        self.root.after(400, self._loop_matrix_init)

    def _loop_clock(self):
        if not self.is_running: return
        try:
            self.clk_lbl.config(text=f"SESSION: {time.strftime('%Y-%m-%d  %H:%M:%S')}")
        except: pass
        self._after(1000, self._loop_clock)

    def _loop_stats(self):
        if not self.is_running: return
        try:
            path = "C:/" if os.name == 'nt' else "/"
            total, _, free = shutil.disk_usage(path)
            ct = random.randint(89, 114)
            warn = "CRITICAL" if ct > 100 else "WARNING"
            info = (
                f"CPU TEMP:  {ct}°C [{warn}]\n"
                f"FAN RPM:   0  [STALLED]\n"
                f"VOLTAGE:   1.54V [UNSTABLE]\n"
                f"RAM:       {random.randint(94, 99)}%  [CRITICAL]\n"
                f"SWAP:      {random.randint(88, 100)}% [FULL]\n"
                f"NET ▲:     {random.randint(100, 999)} KB/s\n"
                f"NET ▼:     {random.randint(10, 90)} MB/s\n"
                f"SOCKETS:   {random.randint(1800, 7000)}\n"
                f"LATENCY:   {random.randint(800, 4500)} ms\n"
                f"ENTROPY:   {random.randint(55, 74)}%\n\n"
                f"DRIVE:\n"
                f"  FREE:  {free // (2**30)} GB\n"
                f"  TOTAL: {total // (2**30)} GB\n\n"
                f"STATUS: KERNEL_PANIC\n"
                f"BREACH: IMMINENT"
            )
            self.stats_lbl.config(text=info)
        except: pass
        self._after(3000, self._loop_stats)

    def _loop_log(self):
        if not self.is_running: return
        ip = f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        entries = [
            f"[WARN] inode {random.randint(100000, 999999)} flagged for sweep",
            f"[CRIT] unauthorized probe on port {random.randint(1, 65535)}",
            f"[INFO] packet intercept from {ip}",
            f"[WARN] sector {random.randint(1000, 9999)} read error x{random.randint(2, 9)}",
            f"[CRIT] auth module timeout #{random.randint(1, 99)}",
            f"[INFO] entropy pool drain: {random.randint(10, 40)}%",
            f"[WARN] suid escalation attempt blocked",
            f"[CRIT] mem fault at 0x{random.randint(0, 0xFFFFFF):06X}",
            f"[CRIT] CYNIC_PROTOCOL: monitoring active",
            f"[INFO] TLS handshake: {ip}",
            f"[WARN] SSL cert verification failed",
            f"[CRIT] watchdog: heartbeat timeout",
            f"[INFO] ARP spoof detected: {ip}",
            f"[WARN] swap usage critical: {random.randint(88, 100)}%",
        ]
        try:
            self.log_txt.config(state="normal")
            self.log_txt.insert("end", random.choice(entries) + "\n")
            self.log_txt.see("end")
            lines = int(self.log_txt.index("end-1c").split(".")[0])
            if lines > 90:
                self.log_txt.delete("1.0", "15.0")
            self.log_txt.config(state="disabled")
        except: pass
        self._after(random.randint(300, 1000), self._loop_log)

    def _loop_net(self):
        if not self.is_running: return
        try:
            self.net_pts.append(random.randint(5, 48))
            if len(self.net_pts) > 40:
                self.net_pts.pop(0)
            self.net_cv.delete("all")
            pts = self.net_pts[-30:]
            n = len(pts)
            w = self.net_cv.winfo_width() or 215
            h = 52
            if n > 1:
                coords = []
                for i, y in enumerate(pts):
                    coords.extend([i * w // (n - 1), h - y])
                for off, col in [(4, '#001400'), (2, '#003300')]:
                    self.net_cv.create_line(coords, fill=col, width=off, smooth=True)
                self.net_cv.create_line(coords, fill=self.GRN, width=1, smooth=True)
        except: pass
        self._after(200, self._loop_net)

    def _loop_glitch(self):
        if not self.is_running: return
        original = "VOID-OS // KERNEL v2.0"
        if random.random() < 0.18:
            gl = list(original)
            for p in random.sample(range(len(original)), random.randint(1, 3)):
                gl[p] = random.choice(GLITCH_CHARS)
            try:
                self.title_lbl.config(text="".join(gl))
                self.root.after(65, lambda: self.title_lbl.config(text=original)
                                if self.is_running else None)
            except: pass
        self._after(random.randint(1100, 3200), self._loop_glitch)

    def _loop_matrix_init(self):
        try:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            cw = 14
            self.mat_cols = [
                {'x': i * cw, 'y': random.randint(-sh, 0)}
                for i in range(sw // cw)
            ]
        except:
            self.mat_cols = []
        self._loop_matrix()

    def _loop_matrix(self):
        if not self.is_running: return
        try:
            self.mat.delete("all")
            h = self.root.winfo_height()
            for col in self.mat_cols:
                length = random.randint(4, 18)
                for j in range(length):
                    y = col['y'] - j * 14
                    if 0 <= y <= h:
                        ch = random.choice(MATRIX_CHARS)
                        shade = '#001800' if j < 2 else '#001000' if j < 7 else '#000900'
                        self.mat.create_text(col['x'], y, text=ch,
                                             fill=shade, font=("Courier New", 8),
                                             anchor="nw")
                col['y'] += 14
                if col['y'] > h:
                    col['y'] = random.randint(-350, 0)
        except: pass
        self._after(75, self._loop_matrix)

    # ════════════════════════════════════════════════════════════════
    #  UI HELPERS
    # ════════════════════════════════════════════════════════════════

    def _update_stage_ui(self):
        if self.stage >= len(STAGES): return
        s = STAGES[self.stage]
        self.stg_title.config(text=f"▌ {s['display']}  ─  {s['title']} ▐")
        self.q_lbl.config(text=s['question'], fg=self.RED)
        self.hint_lbl.config(text=s['hint'])
        self.pv.set("")
        try: self.entry.focus_set()
        except: pass

    def _update_stage_tabs(self):
        for i, lbl in enumerate(self.stage_tabs):
            if i < self.stage:
                lbl.config(text=f"  ✓ STAGE {i+1:02d}  ", fg=self.GDIM)
            elif i == self.stage:
                lbl.config(text=f"  ▶ STAGE {i+1:02d}  ", fg=self.ORG)
            else:
                lbl.config(text=f"  ▸ STAGE {i+1:02d}  ", fg=self.GRY)

    def _set_threat(self, pct):
        pct = min(100, pct)
        w = int(130 * pct / 100)
        self.thr_cv.coords(self.thr_rect, 0, 0, w, 10)
        col = self.RED if pct > 70 else self.ORG if pct > 40 else self.YEL
        self.thr_cv.itemconfig(self.thr_rect, fill=col)
        self.thr_lbl.config(text=f"{pct}%", fg=col)

    def _set_breach(self):
        pct = self.total_fails / 12
        try:
            w = self.breach_cv.winfo_width() or 200
            bw = int(w * pct)
            self.breach_cv.coords(self.breach_rect, 0, 0, bw, 14)
            col = self.RED if pct > 0.7 else self.ORG if pct > 0.4 else self.YEL
            self.breach_cv.itemconfig(self.breach_rect, fill=col)
            self.breach_lbl.config(text=f"{self.total_fails} / 12 FAILURES", fg=col)
        except: pass

    def _set_status(self, msg):
        try: self.status_lbl.config(text=f"▶ {msg}")
        except: pass

    def _set_foot(self, msg):
        try: self.foot_lbl.config(text=f"▶ {msg}")
        except: pass

    def _boot_msg(self):
        self._set_status("KERNEL LOADED — FOUR-LAYER AUTHENTICATION REQUIRED")

    # ════════════════════════════════════════════════════════════════
    #  CORE LOGIC
    # ════════════════════════════════════════════════════════════════

    def _check(self):
        ans = self.pv.get().strip().lower()
        if not ans: return
        if self.stage < len(STAGES) and ans == STAGES[self.stage]['answer']:
            self._stage_pass()
        else:
            self.total_fails += 1
            self.stage_fails += 1
            self._set_threat(self.total_fails * 8)
            self._set_breach()
            if self.total_fails >= 12:
                self._scorched_earth()
            else:
                self._on_fail()

    def _stage_pass(self):
        self.stage_fails = 0
        prev = self.stage
        self.stage += 1
        self._update_stage_tabs()
        if self.stage >= len(STAGES):
            self._go_success()
        else:
            self.q_lbl.config(fg=self.GRN)
            self._set_status(
                f"▌ STAGE {prev+1} CLEARED ▐  —  NEXT CIPHER LAYER INITIALIZING..."
            )
            self.root.after(1000, self._next_stage)

    def _next_stage(self):
        self._update_stage_ui()
        self._set_status(f"▌ STAGE {self.stage + 1} / 4 ▐  —  AUTHENTICATE TO CONTINUE")

    def _on_fail(self):
        self.pv.set("")
        tgt = self._rand_folder()
        msgs = [
            f"!! ACCESS DENIED — SCANNING: {tgt}",
            f"!! AUTH FAILURE #{self.total_fails} — TARGETING: {tgt}",
            f"!! INVALID TOKEN — QUEUING DELETION: {tgt}",
            f"!! BREACH LOGGED — INDEXING: {tgt}",
            f"!! WRONG INPUT — FLAGGING: {tgt}",
        ]
        remain = 12 - self.total_fails
        self.fail_lbl.config(
            text=f"ERRORS: {self.total_fails} / 12  ─  {remain} FAILURES REMAIN BEFORE SCORCHED EARTH"
        )
        self._set_foot(random.choice(msgs))
        self._flash(5)
        self.root.after(220, self._shake)
        if self.total_fails >= 3:
            self._cynic_speak()
            if not self.helper_active and self.total_fails == 3:
                self._slide_popup()

    def _flash(self, n, on=True):
        if n <= 0:
            try: self.mf.configure(bg=self.BG)
            except: pass
            return
        try: self.mf.configure(bg='#180000' if on else self.BG)
        except: pass
        self.root.after(65, lambda: self._flash(n - 1, not on))

    def _shake(self):
        if self.shaking: return
        self.shaking = True

        def do(n):
            if n <= 0:
                try: self.mf.place(relx=0, rely=0, relwidth=1, relheight=1)
                except: pass
                self.shaking = False
                return
            try:
                sw = self.root.winfo_width() or 1920
                sh = self.root.winfo_height() or 1080
                dx = random.randint(-10, 10) / sw
                dy = random.randint(-8, 8) / sh
                self.mf.place(relx=dx, rely=dy, relwidth=1, relheight=1)
            except: pass
            self.root.after(32, lambda: do(n - 1))

        do(12)

    # ── The Cynic speech ────────────────────────────────────────────
    def _cynic_speak(self):
        st = min(self.stage, len(self.HINTS) - 1)
        icon_i  = min(self.total_fails - 3, len(self.ICONS)   - 1)
        ins_i   = min(self.total_fails - 3, len(self.INSULTS) - 1)
        hint_i  = max(0, min(self.stage_fails - 1, len(self.HINTS[st]) - 1))

        icon   = self.ICONS[max(0, icon_i)]
        insult = self.INSULTS[max(0, ins_i)]
        hint   = self.HINTS[st][hint_i]

        try:
            self.cynic_icon.config(text=icon, fg=self.RED)
            self.cynic_status.config(text="⚠ INTERVENTION MODE", fg=self.ORG)
            self.cynic_msg.config(text=f"{insult}\n\n» {hint}")
            self.pop_icon.config(text=icon)
            self.pop_msg.config(text=hint)
        except: pass

    def _slide_popup(self):
        self.helper_active = True
        self.popup_relx = 1.5

        def slide():
            if not self.is_running: return
            if self.popup_relx > 0.68:
                self.popup_relx -= 0.03
                try: self.popup.place(relx=self.popup_relx, rely=0.3)
                except: return
                self.root.after(16, slide)

        slide()

    # ════════════════════════════════════════════════════════════════
    #  SCORCHED EARTH (پرنک نهایی — هیچ فایلی حذف نمیشه)
    # ════════════════════════════════════════════════════════════════

    def _scorched_earth(self):
        self.is_running = False
        for t in self.tasks:
            try: self.root.after_cancel(t)
            except: pass
        try:
            for w in self.root.winfo_children():
                w.destroy()
        except: pass

        self.root.configure(bg="#000")

        try:
            self.script_path = os.path.abspath(sys.argv[0])
            script_dir = os.path.dirname(self.script_path)
        except:
            self.script_path = None
            script_dir = "UNKNOWN_DIR"

        cv = tk.Canvas(self.root, bg="#000", highlightthickness=0)
        cv.place(relwidth=1, relheight=1)

        tk.Label(
            self.root, text="◉  SCORCHED EARTH PROTOCOL ACTIVATED  ◉",
            font=("Courier New", 19, "bold"), fg="#ff0000", bg="#000"
        ).place(relx=0.5, rely=0.06, anchor="center")

        skull = (
            "       ████████████████████\n"
            "     ██                    ██\n"
            "    ██  ████        ████  ██\n"
            "    ██  ████        ████  ██\n"
            "     ██      ██████      ██\n"
            "       ████          ████\n"
            "      ████████████████████\n"
            "     ██  ██    ██  ██    ██\n"
            "      ████      ████    ██"
        )
        tk.Label(
            self.root, text=skull,
            font=("Courier New", 10), fg="#1e0000", bg="#000", justify="center"
        ).place(relx=0.5, rely=0.32, anchor="center")

        final = (
            f"12 AUTHENTICATION FAILURES REGISTERED.\n"
            f"ALL INDEXED NODES QUEUED FOR PURGE.\n\n"
            f"ERASING SELF FROM:\n"
            f"[ {script_dir} ]\n\n"
            f'THE CYNIC:  "I gave you every single chance."\n'
            f'            "You wasted every single one."\n'
            f'            "Goodbye."'
        )
        tk.Label(
            self.root, text=final,
            font=("Courier New", 12, "bold"), fg="#ff0000", bg="#000", justify="center"
        ).place(relx=0.5, rely=0.62, anchor="center")

        # Animated fake wipe text (nothing is actually deleted)
        def wipe_anim(i):
            if not cv.winfo_exists(): return
            if i < 110:
                p = self._rand_folder()
                msgs = [
                    f"PURGE MFT [{random.randint(100000, 999999)}] .... [ERASED]",
                    f"UNLINK: {p}\\{random.randint(1000, 9999)}.dat",
                    f"ZERO SECTOR {random.randint(0, 9999):04d} ......... [DONE]",
                    f"FLUSH VAULT: {p} ... [SENT]",
                    f"WIPE 0x{random.randint(0, 0xFFFFFF):06X} ........ [GONE]",
                    f"CIPHER KEYS DESTROYED ........... [UNRECOVERABLE]",
                    f"SHRED: {p}\\backup_{random.randint(1,99):02d}.zip",
                    f"OVERWRITE PASS {random.randint(1,7)}/7 ............ [DONE]",
                ]
                try:
                    w = self.root.winfo_width()
                    h = self.root.winfo_height()
                    cv.create_text(
                        random.randint(60, max(61, w - 60)),
                        (i * 13) % max(1, h),
                        text=random.choice(msgs),
                        fill=f"#{random.randint(0x14, 0x44):02x}0000",
                        font=("Courier New", 7),
                    )
                except: pass
                self.root.after(18, lambda: wipe_anim(i + 1))
            else:
                tk.Button(
                    self.root, text="[ I UNDERSTAND.  GOODBYE. ]",
                    command=self._self_destruct,
                    font=("Courier New", 13, "bold"),
                    bg="#ff0000", fg="#fff",
                    border=0, padx=60, pady=18, cursor="hand2"
                ).place(relx=0.5, rely=0.91, anchor="center")

        wipe_anim(0)

    def _self_destruct(self):
        """فقط فایل خود اسکریپت حذف میشه — هیچ فایل سیستمی دیگه‌ای دست نخورده."""
        try:
            path = getattr(self, 'script_path', None)
            if path and os.path.exists(path):
                os.remove(path)
        except: pass
        try: self.root.destroy()
        except: pass

    # ════════════════════════════════════════════════════════════════
    #  SUCCESS SCREEN
    # ════════════════════════════════════════════════════════════════

    def _go_success(self):
        self.is_running = False
        for t in self.tasks:
            try: self.root.after_cancel(t)
            except: pass
        try:
            for w in self.root.winfo_children():
                w.destroy()
        except: pass

        self.root.configure(bg="#000d00")
        tf = self.total_fails

        if tf == 0:
            rank, rc, comment = "ARCHITECT",   "#00ff41", "Flawless. You actually know networking."
        elif tf < 3:
            rank, rc, comment = "PROFESSIONAL","#00cc33", "Respectable. You know your protocols."
        elif tf < 6:
            rank, rc, comment = "ADEQUATE",    "#99cc00", "Got there eventually. Not impressed."
        elif tf < 9:
            rank, rc, comment = "AMATEUR",     "#ffcc00", "You needed a lot of hints. Embarrassing."
        elif tf < 12:
            rank, rc, comment = "PATHETIC",    "#ff6600", "I practically typed the answers for you."
        else:
            rank, rc, comment = "BRAIN-DEAD",  "#ff0000", "You got in after 12 failures??? HOW???"

        frm = tk.Frame(self.root, bg="#000d00")
        frm.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frm, text="◉  ACCESS GRANTED  ◉",
                  font=("Courier New", 46, "bold"), fg="#00ff41", bg="#000d00").pack()
        tk.Label(frm, text=f"SECURITY RANK:  {rank}",
                  font=("Courier New", 20, "bold"), fg=rc, bg="#000d00").pack(pady=6)
        tk.Label(frm,
                  text=f"TOTAL ERRORS: {tf} / 12  ─  STAGES COMPLETED: {len(STAGES)} / {len(STAGES)}",
                  font=("Courier New", 10), fg='#333', bg="#000d00").pack()

        icon_i = min(tf // 2, len(self.ICONS) - 1)
        sf = tk.Frame(frm, bg="#001100",
                       highlightbackground="#006600", highlightthickness=1)
        sf.pack(pady=16, padx=20, fill="x")
        tk.Label(sf, text=self.ICONS[icon_i],
                  font=("Courier New", 14, "bold"), fg="#00ff41", bg="#001100"
                  ).pack(padx=16, pady=(10, 4))
        tk.Label(sf, text=f'THE CYNIC:  "{comment}"',
                  font=("Courier New", 10, "italic"), fg="#00aa33", bg="#001100",
                  wraplength=500).pack(padx=16, pady=(0, 12))

        self.e_lbl = tk.Label(frm, text="🤣", font=("Segoe UI Emoji", 62), bg="#000d00")
        self.e_lbl.pack(pady=4)

        self.ang = 0
        def bounce():
            try:
                self.ang += 0.12
                y = int(math.sin(self.ang) * 7)
                self.e_lbl.pack_configure(pady=(4 + y, 4 - y))
                self.root.after(28, bounce)
            except: pass

        bounce()

        tk.Button(
            self.root, text="[ REBOOT SYSTEM ]",
            command=self.root.destroy,
            font=("Courier New", 13, "bold"), bg="#00ff41", fg="#000",
            border=0, padx=60, pady=14, cursor="hand2"
        ).pack(side="bottom", pady=40)


# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    stealth = "--stealth" in sys.argv
    root = tk.Tk()
    root.focus_force()
    if stealth:
        root.title("System Update — Please Wait")
    VoidOS(root)
    root.mainloop()
