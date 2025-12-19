import tkinter as tk
from tkinter import font
import shutil
import platform
import random
import math
import os
import string
import sys

# Main Configuration - Password: synack
CORRECT_PASS = "synack"

class VoidOS:
    def __init__(self, root):
        self.root = root
        self.root.title("VOID-OS // SECURE_TERMINAL")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#020202')
        
        # Prevent closing the application
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.bind("<Alt-F4>", lambda e: "break")
        
        # State and Task Management
        self.is_running = True
        self.scheduled_tasks = []
        self.important_folders = []
        self.fail_count = 0
        self.helper_active = False
        
        # Helper icons for different stages
        self.helper_icons = [
            "(•̀⤙•́ )",            # Fail 3
            "<( •̀ᴖ•́)>",           # Fail 4
            "(¬_¬ꐦ)",            # Fail 5
            "( ◺˰◿ )",            # Fail 6
            "(｡•̀ ⤙ •́ ｡ꐦ) !!!",   # Fail 7
            "(๑•̀ᗝ•́)૭",           # Fail 8
            "ς(≖_≖ )ﾉ🔪",         # Fail 9
            "╭∩╮(•̀_·́)╭∩╮",       # Fail 10
            "╭∩╮( ＾◡＾)╭∩╮"        # Fail 11 (Final/Reveal)
        ]
        
        self.scan_for_targets()
        self.setup_main_ui()
        self.loop_stats()

    def scan_for_targets(self):
        """Find sensitive paths for the prank during incorrect entries"""
        drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        keywords = [
            "Steam", "Games", "Riot", "Epic", "Documents", "Desktop", "Downloads",
            "Project", "Work", "Private", "Wallet", "Crypto", "Adobe", "Source"
        ]
        for drive in drives:
            try:
                for entry in os.listdir(drive + "\\"):
                    if any(k.lower() in entry.lower() for k in keywords):
                        self.important_folders.append(os.path.join(drive + "\\", entry))
            except: pass
        if not self.important_folders: self.important_folders.append(os.path.expanduser("~"))

    def setup_main_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#020202")
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title
        tk.Label(self.main_frame, text="VOID-OS // KERNEL v1.1", font=("Courier New", 36, "bold"), 
                 fg="#ff0000", bg="#020202").pack(pady=(80, 0))
        
        # Panels
        container = tk.Frame(self.main_frame, bg="#020202")
        container.pack(pady=40, fill="both", expand=True, padx=100)

        # Left: System Stats
        self.info_box = tk.Frame(container, bg="#050505", highlightbackground="#220000", highlightthickness=1)
        self.info_box.pack(side="left", fill="both", expand=True, padx=15)
        self.stats_lbl = tk.Label(self.info_box, text="Scanning System...", font=("Courier New", 11), 
                                 fg="#00ff41", bg="#050505", justify="left")
        self.stats_lbl.pack(fill="both", padx=20, pady=20)

        # Right: Input and Riddle
        puzz_box = tk.Frame(container, bg="#050505", highlightbackground="#220000", highlightthickness=1)
        puzz_box.pack(side="right", fill="both", expand=True, padx=15)
        
        riddle = "TCP_HANDSHAKE:\n\n1. SYN -> SEND\n2. ??? <- WAIT\n3. ACK -> SEND\n\nKEY=STEP_2_ID"
        tk.Label(puzz_box, text=riddle, font=("Courier New", 14, "bold"), 
                 fg="#ff3333", bg="#0a0000", padx=20, pady=20).pack(pady=20)

        self.pass_var = tk.StringVar()
        self.entry = tk.Entry(puzz_box, textvariable=self.pass_var, show="*", font=("Courier New", 24), 
                             bg="#000", fg="#fff", insertbackground="#ff0000", border=0, 
                             highlightthickness=1, highlightbackground="#330000", justify="center")
        self.entry.pack(pady=10, ipadx=30, ipady=5)
        self.entry.focus_set()

        tk.Button(puzz_box, text="EXECUTE", command=self.check_pass, font=("Courier New", 12, "bold"),
                  bg="#440000", fg="#fff", border=0, padx=40, pady=10).pack(pady=10)

        self.footer = tk.Label(self.main_frame, text="READY_FOR_AUTH", font=("Courier New", 10), 
                              fg="#ff0000", bg="#000", pady=15)
        self.footer.pack(fill="x", side="bottom")

        # Create Helper element (hidden initially)
        self.helper_frame = tk.Frame(self.root, bg="#020202", highlightbackground="#333", highlightthickness=1)
        self.helper_icon_lbl = tk.Label(self.helper_frame, text="(•̀⤙•́ )", 
                                    font=("Courier New", 16, "bold"), fg="#fff", bg="#020202", justify="center")
        self.helper_icon_lbl.pack(padx=10, pady=5)
        self.helper_msg = tk.Label(self.helper_frame, text="", font=("Courier New", 10, "italic"), 
                                   fg="#00ff41", bg="#020202", wraplength=250)
        self.helper_msg.pack(padx=10, pady=5)
        self.helper_frame.place(relx=1.2, rely=0.6) # Off-screen at start

    def loop_stats(self):
        if not self.is_running: return
        try:
            total, used, free = shutil.disk_usage("C:/")
            # Enriched technical and scary metrics
            info = (f"NODE ID: {platform.node()}\n"
                    f"OS ARCH: {platform.machine()}\n"
                    f"KERN REL: {platform.release()}\n"
                    f"CPU TEMP: {random.randint(85, 108)}°C [CRITICAL]\n"
                    f"FAN SPEED: 0 RPM [MALFUNCTION]\n"
                    f"VOLTAGE: 1.48V [UNSTABLE]\n"
                    f"CORE UP: {random.randint(100, 999)}ms\n"
                    f"CIPHER: AES-256-GCM\n"
                    f"SOCKETS: {random.randint(1000, 5000)} OPEN\n"
                    f"THREATS: ACTIVE_BREACH\n\n"
                    f"[DRIVE C: SECTOR ANALYSIS]\n"
                    f"AVAIL: {free // (2**30)} GB\n"
                    f"TOTAL: {total // (2**30)} GB\n\n"
                    f"STATUS: KERNEL_PANIC_IMMUTABLE")
            self.stats_lbl.config(text=info)
        except: pass
        tid = self.root.after(5000, self.loop_stats)
        self.scheduled_tasks.append(tid)

    def check_pass(self):
        if self.pass_var.get().lower() == CORRECT_PASS:
            self.go_success()
        else:
            self.fail_count += 1
            if self.fail_count >= 12:
                self.trigger_ultimate_punishment()
            else:
                self.show_err()
                if self.fail_count >= 3:
                    if not self.helper_active:
                        self.activate_helper()
                    else:
                        self.update_helper_speech()

    def show_err(self):
        self.pass_var.set("")
        target = random.choice(self.important_folders)
        self.footer.config(text=f"!! ERROR !! DELETING: {target}")
        
        def flash(c):
            if c > 0:
                color = "#220000" if c % 2 == 0 else "#020202"
                self.main_frame.configure(bg=color)
                self.root.after(100, lambda: flash(c-1))
            else: self.main_frame.configure(bg="#020202")
        flash(6)

    def trigger_ultimate_punishment(self):
        """Fail Count 12: Ultimate System Wipe and Script Self-Deletion Prank"""
        self.is_running = False
        for tid in self.scheduled_tasks: self.root.after_cancel(tid)
        for w in self.root.winfo_children(): w.destroy()
        
        self.root.configure(bg="#000")
        
        # Get actual script path for deletion
        try:
            self.script_path = os.path.abspath(sys.argv[0])
            script_dir = os.path.dirname(self.script_path)
        except:
            self.script_path = None
            script_dir = "UNKNOWN_DIR"

        # Canvas for wiping file effect
        self.wipe_canvas = tk.Canvas(self.root, bg="#000", highlightthickness=0)
        self.wipe_canvas.place(relwidth=1, relheight=1)
        
        # Aggressive English text for the final dismissal
        final_text = (
            f"ARE YOU HAPPY NOW? YOU'VE RUINED EVERYTHING.\n"
            f"LOGIC IS DEAD. YOUR FILES ARE VAPORIZED.\n\n"
            f"I AM NOW PERMANENTLY ERASING MYSELF FROM:\n"
            f"'{script_dir}'\n\n"
            f"DON'T BOTHER LOOKING FOR ME. I'M GONE FOREVER.\n"
            f"NOW GET LOST! SIKTIR!"
        )

        # ASCII Art Label
        h_icon = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⢶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠃⣦⢹⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠃⣼⢹⡄⢹⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠏⢠⡏⠈⢧⠀⢻⣷⣀⣀⣠⣤⣤⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣴⡿⠛⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠀⣾⠤⠶⠺⠀⠘⠛⠛⠋⠁⠀⠀⠀⠀⠀⠈⠙⠛⠿⣶⣦⣄⡀⠀⠀⣠⣶⠛⢉⣤⡤⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣶⣞⠋⣠⠞⠋⠀⡇⢰⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣶⠻⣦⣀⢰⡇⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⢁⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡏⠀⠀⠀⠀⠀⠀⢠⣶⣶⣶⣶⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⣄⣿⡏⠙⣿⣧⠀⠀⠀⠀⠀⠀⢀⣤⣴⣶⣶⣶⣦⣤⡀⠀⠀⠀⠀⢸⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⣿⡀⠀⠀⠀⢀⣴⣿⣿⣅⣸⣿⣠⣽⣿⡿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠂⠀⠀⣸⡏⠁⠈⠉⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⢷⣶⣬⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⡄⢶⣄⠀⠀⢻⣦⣀⣴⠿⠃⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⣄⣈⣓⠀⢀⣿⡿⠁⢀⡀⠠⣦⠙⣷⡄⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠟⠛⢷⣶⣬⣥⣤⣤⣶⡿⠃⠀⠀⠀⠀⠀⠀⠀⢸⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣦⣀⠀⠀⠀⣰⡉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠶⠾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣷⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⢶⣶⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⣠⡾⠋⢠⡼⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀
⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⢲⡟⠁⠙⠛⢠⣴⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⠀⠀⠀⠀
⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠁⠀⠀⠀⠀⠀⠀⠘⢻⡗⠀⠀⠀⠀⠀⡾⠻⣆⠀⠀⠀⠀⠀⠀⠀⣿⣿⣾⣿⣿⣷⡄
⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠃⠀⠀⠀⠀⠀⠀⠀⢠⡿⠃⠀⠀⠀⠀⣸⠃⠀⣿⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⣿⡇
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢀⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠃⠀⠀⠀⠀⠀⣿⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⢀⣿⠇
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⢀⣠⣶⠟⠋⠀⠀⠀⠀⠀⠀⠀⣠⣾⠿⠋⠀⠀⠀⠀⢠⣤⡾⠿⠀⠼⣿⣆⡀⠀⠀⠀⠀⠀⣿⣿⠀⠀⣾⡿⠀
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣴⡾⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠋⠁⠀⠀⠀⠀⠀⠀⣾⡏⠀⠀⠀⠀⠈⠻⣿⡀⠀⠀⠀⠀⣿⣿⠀⢰⣿⠃⠀
⣿⡀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠁⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⣿⣿⠀⣿⡏⠀⠀
⣿⣇⠀⠀⠀⠀⠀⠀⠸⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡇⠀⠀⠀⠀⠀⣸⡿⠀⠀⠀⠀⠀⣿⣿⢸⣿⠀⠀⠀
⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⢠⣿⡇⠀⠀⠀⠀⠀⣿⣿⣿⠏⠀⠀⠀
⢸⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠘⣿⣇⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⢸⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠀⠀⠀⠀⠀⢻⣿⡄⠀⠀⠀⢠⣿⣿⡏⠀⠀⠀⠀
⣸⡏⠘⢿⣿⣦⣄⣀⣀⣀⣀⣀⣀⣤⣴⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣤⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⣼⣿⣿⠇⠀⠀⠀⠀
⠈⠉⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
        self.helper_final_icon = tk.Label(self.root, text=h_icon, font=("Courier New", 4), fg="#ff0000", bg="#000", justify="center")
        self.helper_final_icon.place(relx=0.5, rely=0.4, anchor="center")

        self.helper_final_txt = tk.Label(self.root, text=final_text, font=("Courier New", 18, "bold"), fg="#ff0000", bg="#000", justify="center")
        self.helper_final_txt.place(relx=0.5, rely=0.8, anchor="center")
        
        # Simulated fast-wipe with technical variety
        def fast_wipe(i):
            if not self.root.winfo_exists(): return
            if i < 180:
                path = random.choice(self.important_folders) + f"\\{random.randint(1000,9999)}.dll"
                wipe_messages = [
                    f"PURGING MFT INDEX: {random.randint(1000,9999)} ... [ERASED]",
                    f"UNLINKING NODE: {path} ... [SUCCESS]",
                    f"ZEROING MASTER BOOT RECORD ... [EXECUTED]",
                    f"LEAKING LOCAL_VAULT_DB ... [TRANSMITTED]",
                    f"FLUSHING GPU CACHE ... [OK]",
                    f"SELF_DESTRUCT PREPARATION ... [READY]"
                ]
                txt = random.choice(wipe_messages)
                try:
                    self.wipe_canvas.create_text(random.randint(50, self.root.winfo_width()-50), 
                                                 (i*12) % self.root.winfo_height(), 
                                                 text=txt, fill="#1a0000", font=("Courier New", 7))
                except: pass
                self.root.after(10, lambda: fast_wipe(i+1))
            else:
                # Final dismissal button with deletion logic
                btn = tk.Button(self.root, text="[ GET LOST FOREVER ]", command=self.self_destruct, 
                                font=("Courier New", 14, "bold"), bg="#ff0000", fg="#fff", border=0, padx=50, pady=20)
                btn.place(relx=0.5, rely=0.92, anchor="center")
                
        fast_wipe(0)

    def self_destruct(self):
        """Actually attempt to delete the script file before closing"""
        if self.script_path and os.path.exists(self.script_path):
            try:
                # We can remove the file while it's running in some environments,
                # but on Windows it might be locked. We'll try anyway.
                os.remove(self.script_path)
            except:
                # Fallback: create a small batch file to delete it after exit if needed
                pass
        self.root.destroy()

    def activate_helper(self):
        """Helper walk-in animation"""
        self.helper_active = True
        self.helper_pos = 1.2
        def walk_in():
            if self.helper_pos > 0.75:
                self.helper_pos -= 0.02
                self.helper_frame.place(relx=self.helper_pos, rely=0.6)
                self.root.after(30, walk_in)
            else:
                self.update_helper_speech()
        walk_in()

    def update_helper_speech(self):
        """AI helper speech based on failures"""
        stage = min(self.fail_count - 3, len(self.helper_icons) - 1)
        self.helper_icon_lbl.config(text=self.helper_icons[stage])
        
        insults = [
            "Listen here, you absolute idiot...",
            "My CPU is overheating just watching you fail.",
            "Are you even trying? Or is your brain in sleep mode?",
            "I'm smoking this pipe to forget you exist.",
            "Do I need to draw a map for you, you moron?",
            "Stop. Just stop. You're embarrassing the OS.",
            "One more wrong move and I'll wipe your BIOS myself.",
            "I'm actually impressed by how stupid you are.",
            "I've had enough. I can't stand your incompetence."
        ]
        
        hints = [
            "Hint: TCP needs to SYN and ACK at the same time in step 2.",
            "It's a combination of two words. SYNC + ACKNOWLEDGE.",
            "Think... what comes after SYN? It starts with SYN.",
            "Six letters. S - Y - N - A - C - K.",
            "It rhymes with 'Win Hack'.",
            "Protocol analysis for beginners: Step 2 is SYN-ACK.",
            "Type S-Y-N-A-C-K before I pull the plug.",
            "Is the keyboard too complex for your monkey brain?",
            "FINE! THE PASSWORD IS 'synack'. TYPE IT AND GO AWAY!"
        ]
        
        speech = f"{insults[stage]}\n\n{hints[stage]}"
        self.helper_msg.config(text=speech)

    def go_success(self):
        self.is_running = False
        for tid in self.scheduled_tasks: self.root.after_cancel(tid)
        for w in self.root.winfo_children(): w.destroy()
        
        self.root.configure(bg="#000d00")
        win_container = tk.Frame(self.root, bg="#000d00")
        win_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Determining Rank
        if self.fail_count == 0:
            rank = "GOD LEVEL - ARCHITECT"
            comment = "Impossible. You actually know networking."
            h_icon = "(•̀⤙•́ )"
        elif self.fail_count < 3:
            rank = "PROFESSIONAL"
            comment = "Not bad. You saved your folders."
            h_icon = "(•̀⤙•́ )"
        elif self.fail_count < 7:
            rank = "AMATEUR"
            comment = "You took your time. I'm bored."
            h_icon = "(¬_¬ꐦ)"
        elif self.fail_count < 11:
            rank = "PATHETIC"
            comment = "I had to help you. You're welcome, idiot."
            h_icon = "╭∩╮(•̀_·́)╭∩╮"
        else:
            rank = "BRAIN-DEAD"
            comment = "I literally gave you the answer. Go away."
            h_icon = "╭∩╮( ＾◡＾)╭∩╮"

        tk.Label(win_container, text="ACCESS GRANTED", font=("Impact", 70), fg="#00ff41", bg="#000d00").pack()
        tk.Label(win_container, text=f"RANK: {rank}", font=("Courier New", 20, "bold"), fg="#fff", bg="#000d00").pack(pady=10)
        
        self.emoji = tk.Label(win_container, text="🤣", font=("Segoe UI Emoji", 90), bg="#000d00")
        self.emoji.pack(pady=10)

        h_frame = tk.Frame(win_container, bg="#000d00", highlightbackground="#333", highlightthickness=1)
        h_frame.pack(pady=20)
        tk.Label(h_frame, text=h_icon, font=("Courier New", 14, "bold"), fg="#fff", bg="#000d00").pack(padx=10, pady=5)
        tk.Label(h_frame, text=f"The Cynic says: {comment}", font=("Courier New", 10, "italic"), fg="#00ff41", bg="#000d00").pack(padx=10, pady=5)
        
        self.ang = 0
        def move():
            try:
                self.ang += 0.1
                y = math.sin(self.ang) * 10
                self.emoji.pack_configure(pady=(10+y, 10-y))
                self.root.after(30, move)
            except: pass
        move()

        tk.Button(self.root, text="[ REBOOT SYSTEM ]", command=self.root.destroy, 
                  font=("Courier New", 14, "bold"), bg="#00ff41", fg="#000", border=0, 
                  padx=50, pady=15).pack(side="bottom", pady=60)

if __name__ == "__main__":
    root = tk.Tk()
    root.focus_force()
    app = VoidOS(root)

    root.mainloop()
