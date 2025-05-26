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

vtrace-lite/
├── web/
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── logs.html
│   │   ├── manage_vm.html
│   │   ├── resource_host.html
│   │   ├── resource_menu.html
│   │   ├── resource_monitor.html
│   │   ├── resource_vm.html
│   │   ├── scheduling.html
│   │   ├── snapshots.html
│   │   └── vms.html
│   ├── app.py
│   ├── encryption.key
│   └── vm_manager.log
├── auth.py
├── config.enc
├── config.json
├── encryption_utils.py
├── encryption.key
├── logger_config.py
├── main.py
├── password.hash
├── resource_logger.py
├── resource_usage.csv
├── vm_finder.py
├── vm_manager.log
├── vm_manager.py
├── vm_monitor.py
├── vm_scheduler.py
├── vm_status.py
└── requirements.txt

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
