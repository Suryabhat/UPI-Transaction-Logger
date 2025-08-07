import qrcode
import sqlite3
from datetime import datetime
from prettytable import PrettyTable  # Install using `pip install prettytabl1e`

# Initialize the database
conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()

# Create table for transactions if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upi_id TEXT NOT NULL,
    app_name TEXT NOT NULL,
    url TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    balance REAL NOT NULL
)''')
conn.commit()

# Add the 'balance' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE transactions ADD COLUMN balance REAL DEFAULT 0.0")
    conn.commit()
except sqlite3.OperationalError:
    # Ignore if the column already exists
    pass

# Create a table for balance if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS balance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    current_balance REAL NOT NULL
)''')

# Check and initialize dummy balance
cursor.execute("SELECT current_balance FROM balance ORDER BY id DESC LIMIT 1")
balance_row = cursor.fetchone()
if balance_row is None:
    cursor.execute("INSERT INTO balance (current_balance) VALUES (1000.00)")  # Initial balance: 1000
    conn.commit()
    current_balance = 1000.00
else:
    current_balance = balance_row[0]

print(f"\nCurrent Balance: ₹{current_balance:.2f}")

# Define default UPI IDs
UPI_1 = "suryanarayanabhat1508@okhdfcbank"
#UPI_2 = "exampleuser@okicici"

# UPI selection by the user
print("\nSelect a UPI ID:")
print(f"1. {UPI_1}")
#print(f"2. {UPI_2}")
print("2. Enter a new UPI ID")

upi_choice = int(input("Enter your choice (1-2): "))
if upi_choice == 1:
    upi_id = UPI_1
elif upi_choice == 2:
    upi_id = input("Enter your UPI ID: ")
else:
    print("Invalid choice!")
    conn.close()
    exit()

# Taking transaction details as input
amount = float(input("Enter the amount: "))

# Determine transaction type based on balance update
if amount > 0:
    new_balance = current_balance + amount
    transaction_type = "credit"
else:
    # Check for insufficient balance in case of debit
    if abs(amount) > current_balance:
        print(f"\nInsufficient balance! Your current balance is ₹{current_balance:.2f}. Cannot debit ₹{abs(amount):.2f}.")
        conn.close()
        exit()  # Exit the program if the transaction cannot proceed
    else:
        new_balance = current_balance + amount  # Subtracting for debit
        transaction_type = "debit"

# UPI URL for Google Pay
google_pay_url = f'upi://pay?pa={upi_id}&pn=Recipient%20Name&am={abs(amount)}&mc=1234'

# Generate QR code and handle transaction logging
def generate_qr(app_name, url, file_name):
    qr = qrcode.make(url)
    qr.show()  # Display the QR code
    
    # Ask user for confirmation
    print("\nPress Enter to confirm the transaction or F to cancel...")
    user_input = input().strip().lower()
    
    if user_input == "f":
        print(f"\nTransaction canceled. Your balance remains unchanged at ₹{current_balance:.2f}.")
        return False  # Transaction not successful
    else:
        # Log transaction in the database
        cursor.execute('INSERT INTO transactions (upi_id, app_name, url, amount, transaction_type, timestamp, balance) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (upi_id, app_name, url, abs(amount), transaction_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), new_balance))
        conn.commit()
        return True  # Transaction successful

# Generate QR code for Google Pay and handle the result
transaction_status = generate_qr("Google Pay", google_pay_url, 'google_pay_qr.png')

if transaction_status:
    # Update balance in the database only if the transaction is successful
    cursor.execute("INSERT INTO balance (current_balance) VALUES (?)", (new_balance,))
    conn.commit()
    print(f"\nTransaction successful! Updated Balance: ₹{new_balance:.2f}")
else:
    print("\nNo transaction was recorded.")

# Display filter options
print("\nChoose a filter to view transactions:")
print("1. By Date")
print("2. By Transaction Type")
print("3. View All Transactions")

# Get user choice
choice = int(input("Enter your choice (1-3): "))

if choice == 1:
    date_input = input("Enter the date (DD-MM-YYYY): ")
    
    # Convert DD-MM-YYYY to YYYY-MM-DD
    try:
        date = datetime.strptime(date_input, "%d-%m-%Y").strftime("%Y-%m-%d")
        cursor.execute("SELECT * FROM transactions WHERE DATE(timestamp) = ?", (date,))
    except ValueError:
        print("Invalid date format! Please use DD-MM-YYYY.")
        conn.close()
        exit()


# Fetch data based on the chosen filter
# if choice == 1:
#     date = input("Enter the date (YYYY-MM-DD): ")
#     cursor.execute("SELECT * FROM transactions WHERE DATE(timestamp) = ?", (date,))
elif choice == 2:
    transaction_type = input("Enter transaction type (credit/debit): ").lower()
    cursor.execute("SELECT * FROM transactions WHERE transaction_type = ?", (transaction_type,))
elif choice == 3:
    cursor.execute("SELECT * FROM transactions")
else:
    print("Invalid choice!")
    conn.close()
    exit()

# Fetch and display results
rows = cursor.fetchall()

if rows:
    # Define table headers (matching database columns)
    table = PrettyTable(["ID", "UPI ID", "App Name", "URL", "Amount", "Transaction Type", "Timestamp", "Balance"])
    for row in rows:
        table.add_row(row)
    print("\nFiltered Transactions:")
    print(table)
else:
    print("\nNo transactions found for the selected filter.")

# Close the database connection
conn.close()
