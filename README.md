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
````

Ensure you are using **Python 3.6+**.

---

## ▶️ How to Use

1. **Run the Script**:

```bash
python upi_qr_logger.py
```

2. **Choose UPI ID**:

   * Select default UPI ID or enter a new one.

3. **Enter Transaction Amount**:

   * Positive → Credit
   * Negative → Debit (checks for sufficient balance)

4. **Scan & Confirm**:

   * QR code opens automatically.
   * Press `Enter` to confirm or `F` to cancel the transaction.

5. **View Transactions**:
   * Filter transactions by date, type (credit/debit), or view all.
     
6. **Packages Used**:
   * The project uses a few essential Python packages to handle its core functionalities. The `qrcode` package is used to generate UPI QR codes   that can be scanned for payments. To manage the transaction data, the project utilizes `sqlite3`, which is a built-in Python module for interacting with SQLite databases. The `datetime` module, also built-in, is used to fetch and format timestamps for logging transactions. For displaying transaction history in a readable table format, the `prettytable` package is used. Together, these packages enable the creation, tracking, and display of UPI transactions in a simple command-line interface.


---

## 🗃️ Database Tables

1. **`transactions`**
   Stores every transaction with:

   * `upi_id`, `app_name`, `url`, `amount`, `transaction_type`, `timestamp`, `balance`

2. **`balance`**
   Tracks the latest balance after each transaction.

---

## 📦 Project Structure

```
.
├── upi_qr_logger.py     # Main script
├── transactions.db      # SQLite DB (auto-created)
└── README.md            # This file
```

---

## 📌 Sample Default UPI ID

```text
Your Default UPI ID.
Eg: abc@okaxisbank
```

Feel free to add your own UPI IDs or modify for different apps.

---

## 📸 Preview

Upon confirming, the QR code looks like this (for payment apps like GPay):

> ✅ Supports UPI URL format:
> `upi://pay?pa=UPI_ID&pn=Recipient%20Name&am=Amount&mc=1234`

---

## 🧰 Future Improvements

* GUI for easier interaction
* Support for multiple apps (PhonePe, Paytm)
* Export to CSV/PDF
* Graphs for expense/income tracking

---

## 📄 License

This project is open-source and free to use.

---

## 🤝 Contributions

Feel free to fork this repo and open a pull request if you have something to improve or add. Suggestions and bug reports are welcome via [Issues](https://github.com/Suryabhat/UPI-Transaction-Logger/issues)!

---

## 🙋‍♂️ Author

**Surya Narayana Bhat**

