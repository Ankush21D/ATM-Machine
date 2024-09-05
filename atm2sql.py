import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*********",
    port="3306"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS atm_db")
conn.commit()

conn.database = "atm_db"

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(100),
     phoneno VARCHAR(15),
     cardno BIGINT UNIQUE,
     pin INT,
     balance DECIMAL(10, 2) DEFAULT 0.00
)
""")
conn.commit()

cursor = conn.cursor()

print("Welcome to the ATM machine")

action = input("Register or login: ").lower()

if action == "register":
    print("New registration")
    name = input("Enter your name: ")
    phoneno = input("Enter your mobile no.: ")
    cardno = input("Enter Card details: ")  # Note: You may want to generate this dynamically
    print(f"Your new card NO. is: {cardno}")
    pin = int(input("Enter a valid pin: "))
    balance = 0.0

    cursor.execute("INSERT INTO users (name, phoneno, cardno, pin, balance) VALUES (%s, %s, %s, %s, %s)",
                   (name, phoneno, cardno, pin, balance))
    conn.commit()
    print("Registration successful!")

elif action == "login":
    print("Login")
    cardno = int(input("Enter your card details: "))
    pin = int(input("Enter your pin: "))

    # Verify login details
    cursor.execute("SELECT name, phoneno, cardno, pin, balance FROM users WHERE cardno = %s AND pin = %s", (cardno, pin))
    result = cursor.fetchone()

    if result:
        stored_name, stored_phoneno, stored_cardno, stored_pin, balance = result
        print("Login successful")
    else:
        print("Invalid card number or pin")
        cursor.close()
        conn.close()
        exit()

else:
    print("Invalid option. Please enter 'Register' or 'Login'.")
    cursor.close()
    conn.close()
    exit()

while True:
    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. Exit")

    account = int(input("Choose an option (1-3): "))

    if account == 1:
        print("Amount to be added")
        deposit = float(input("Enter amount to deposit: "))
        balance += deposit
        cursor.execute("UPDATE users SET balance = %s WHERE cardno = %s", (balance, cardno))
        conn.commit()
        print(f"New balance: ${balance:.2f}")

    elif account == 2:
        print("Amount to be withdrawn")
        withdrawal = float(input("Enter amount to withdraw: "))
        if withdrawal <= balance:
            balance -= withdrawal
            cursor.execute("UPDATE users SET balance = %s WHERE cardno = %s", (balance, cardno))
            conn.commit()
            print(f"New balance: ${balance:.2f}")
        else:
            print("Insufficient funds")

    elif account == 3:
        print("Exiting the program. Goodbye!")
        break

    else:
        print("Invalid option, please choose a number between 1 and 3.")

cursor.close()
conn.close()
