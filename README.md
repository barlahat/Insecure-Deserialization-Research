# Insecure Deserialization Research Project 🛡️
**Author:** Bar Lahat  
**Track:** A (Research & Implementation)

## 📌 Project Overview
This project demonstrates a critical web vulnerability: **Insecure Deserialization** (Python Pickle).
The goal is to simulate a real-world attack scenario where an attacker injects a malicious payload into a serialized object, leading to **Remote Code Execution (RCE)**.

## 📂 Files Structure
* `vulnerable_server.py`: The insecure Flask application (uses `pickle`).
* `exploit_generator.py`: The tool to generate malicious payloads (RCE PoC).
* `secure_server.py`: The fixed version of the application (uses `json`).
* `HACK_REPORT.txt`: Proof of Concept (PoC) output demonstrating the system takeover.

## 🚀 How to Run the Attack
1. **Start the Vulnerable Server:**
   ```bash
   python vulnerable_server.py