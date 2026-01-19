# 🎮 The Hacker Store - Insecure Deserialization Project
**Author:** Bar Lahat
**Vulnerability:** Python Pickle Insecure Deserialization
**Impact:** Logic Manipulation & Remote Code Execution (RCE) via Web Shell

## 📌 Project Overview
This project demonstrates how insecure deserialization can be exploited in two different ways:
1.  **Logic Exploit (The Cheat):** Modifying serialized objects to gain infinite money and admin privileges.
2.  **RCE Exploit (The Backdoor):** Injecting a malicious payload to plant a permanent **Web Shell** on the server.

## 📂 File Structure
* `vulnerable_game.py`: The vulnerable Flask application (The Store).
* `exploit_cheat.py`: Generates a payload to modify user stats (Coins/Admin).
* `exploit_backdoor.py`: Generates a payload that uses PowerShell to drop a `shell.html` backdoor.
* `secure_server.py`: A patched version of the server (using JSON).

## 🚀 How to Run the Demo

### Part 1: Logic Attack (The Cheat)
1.  Run the server: `python vulnerable_game.py`
2.  Visit `http://127.0.0.1:5000`. Notice you are a "Guest" with 10 coins.
3.  Run `python exploit_cheat.py` and copy the cookie.
4.  Inject the cookie and refresh.
5.  **Result:** You are now Admin, have 1,000,000 coins, and the Flag is unlocked.

### Part 2: RCE Attack (The Web Shell)
1.  Run `python exploit_backdoor.py` and copy the cookie.
2.  Inject the cookie and refresh the home page.
3.  Navigate to the secret backdoor: `http://127.0.0.1:5000/page/shell.html`
4.  **Result:** You have full command execution access on the server. Try running `dir` or `whoami`.

## 🛡️ Mitigation
To fix this vulnerability, avoid using `pickle` for untrusted data. Use safer formats like **JSON** (implemented in `secure_server.py`).

---
*For Educational Purposes Only.*