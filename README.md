💀 VoidOS: The Nuclear Lock-Screen Prank

"In the void, no one hears your handshake fail."

VoidOS is a high-fidelity, cinematic terminal lock screen designed for network engineers, sysadmins, and security enthusiasts. It’s not just a screen locker; it’s a psychological thriller delivered via a CLI.

The system presents a "locked" state that demands a successful TCP 3-Way Handshake logic sequence to exit. Failure leads to escalation, insults from a reactive AI, and ultimately, a simulated (yet terrifying) system liquidation sequence.

🛠 Technical Architecture

VoidOS is built as a state-driven terminal application. It utilizes ANSI escape sequences for high-performance rendering without heavy dependencies.

1. The 'Cynic' AI State Machine

The Cynic is a reactive ASCII entity that tracks user failures. It operates on a linear entropy scale:

0-3 Failures: "Passive Aggressive" - Snarky comments, static ASCII.

4-8 Failures: "Aggravated" - Increased screen jitter, corrupted text streams.

9-11 Failures: "Hostile" - The AI starts "scanning" local paths (Steam, Crypto Wallets, Project folders) and listing them on-screen.

12 Failures: Nuclear Protocol initiated.

2. The TCP Handshake Puzzle

To "unlock" the system, the user must provide the correct sequence of packets. The logic requires:

SYN: Initializing the request.

SYN-ACK: Acknowledging the server response (provided by VoidOS).

ACK: Finalizing the connection.
Mathematical constraints: Sequence numbers must be manually incremented ($Seq + 1$) during the simulated exchange to pass validation.

3. System Liquidation Simulation

Upon the 12th failure, the application executes a "Scorched Earth" routine:

Visuals: Real-time logging of file deletion (simulated via stdout).

The Nuclear Option: The application utilizes self-deletion logic (e.g., os.Remove(os.Args[0]) in Go or os.remove(__file__) in Python) to erase its own existence, leaving the victim with a blank terminal.

🚀 Installation & Usage

Prerequisites

A terminal with ANSI Color support (xterm-256color recommended).

System-level permissions to read directory structures (for the "threat" scanning feature).

Quick Start

# Clone the repository
git clone [https://github.com/username/VoidOS.git](https://github.com/username/VoidOS.git)

# Enter the directory
cd VoidOS

# Run the kernel (Assuming Python implementation)
python3 void_os.py --stealth-mode


🕹 Key Features

Dynamic Directory Targeting: Uses a weighted list of "High-Value" directory names (e.g., .ssh, Desktop, Documents/Work) to create personalized fear.

High-Fidelity Terminal UI: Custom-built progress bars, matrix-style data streams, and kernel-level diagnostic logs.

Self-Destruct Sequence: A unique feature where the software "commits suicide" to prevent forensic analysis (and for the ultimate theatrical prank).

Zero-Escape Logic: Overrides common interrupts (SIGINT/Ctrl+C) to keep the victim trapped in the experience.

⚖️ Legal & Ethical Disclaimer

VOID-OS IS A PRANK TOOL. It does not actually delete user data (except for its own source code/executable during the self-destruct phase). The author is not responsible for any heart attacks, broken keyboards, or damaged friendships resulting from the use of this software. Use it responsibly on your peers, and never in a production environment where it could cause actual system downtime.

🤝 Contributing

If you want to add more insults to The Cynic or more complex network puzzles, feel free to open a Pull Request.

Maintained by the VoidOS Collective.
