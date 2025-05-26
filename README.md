# VTrace - Virtual Machine Resource Monitoring & Management Platform

**VTrace** is a professional-grade system designed for monitoring, managing, scheduling, and auditing virtual machines (VMs). It combines a secure Flask backend with a responsive Bootstrap-based frontend to deliver powerful VM resource insights in real-time, along with operational control, logging, and encryption-based authentication.

---

## 🚀 Features

- 📊 Real-time VM resource monitoring (CPU, RAM, Disk, Network)
- 🖥️ VM discovery, start, stop, and reboot functionality
- ⏱️ Task scheduler for automated VM operations
- 🔐 Encrypted user authentication and secure configuration handling
- 📁 File-based VM indexer (finder module)
- 📝 Operational and resource usage logging with CSV and file output

---

## 🧠 System Architecture

(https://tree.nathanfriend.com/?s=(%27oJs!(%27fancy!true~fullPath!false~trailingSlash!true~rootDot!false)~7!(%277!%27VTrace-web-*templates-**base0dashboard06in06s0He_ILhostLmenuLFLI0Bing0snapshots0IsCapp3*G*Kauth38.enc-8.jsA-4_utils3G6gE_83main3password.hash-26gE32usage.csv-9findE3K539F39BE39status3requirements.txt%27)~vEsiA!%271%27)*%20%20-%5Cn*0C*2re7_3.py-4encryJ59HE6log7source8cAfig9I_AonBschedulC.html-*EerFmAitorG4.key-HmanagIvmJptiAK5.6-L02%01LKJIHGFECBA987654320-*)

---

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- pip
- VirtualBox, QEMU, or KVM installed (VM-based ops)

### Backend Setup

```bash
git clone https://github.com/ArdacanBodur/VTrace_Lite.git
cd vtrace-lite
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python .\web\app.py   
