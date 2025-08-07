# 🏦 UPI QR Code Transaction Logger with SQLite

This Python project is a **command-line UPI transaction logger** that:
- Generates a UPI QR code for a selected UPI ID
- Logs credit or debit transactions
- Maintains and updates balance in an SQLite database
- Displays filtered transaction history in a clean tabular format

---

## 📌 Features

- 🔐 **UPI ID Selection** (default or user-input)
- 💸 **Credit & Debit Support** with balance check
- 📉 **Real-Time Balance Management**
- 🧾 **QR Code Generation** for UPI payment (Google Pay)
- 🗃️ **SQLite Database Storage**
- 📊 **Transaction Filtering** by date or type
- 📋 **Pretty Table Display** for better readability

---

## 🧑‍💻 Getting Started

### 🔧 Prerequisites

Install required Python packages:

```bash
pip install qrcode[pil] prettytable
