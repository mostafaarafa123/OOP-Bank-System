import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("bank.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            balance REAL,
            type TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            type TEXT,
            amount REAL,
            date TEXT
        )
        """)
        self.conn.commit()
class Account:
    def __init__(self, db,id, username, balance):
        self.db=db
        self.id=id
        self.username=username
        self.balance=balance
    def update_balance(self):
        self.db.cursor.execute("UPDATE account set balance=? WHERE id=?",(self.balance,self.id)  )
        self.db.conn.commt()

    def add_transaction(self, t_type, amount):
        self.db.cursor.execute(
            "INSERT INTO transactions (account_id, type, amount, date) VALUES (?, ?, ?, ?)",
            (self.id, t_type, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.db.conn.commit()
    def deposit(self,amount):
        if amount>0:
            self.balance+=amount
            self.update_balance()
            self.add_transaction("Deposit",amount)
            print("Deposit successful.")
        else:
            print("Invalid amount.")
    def withDraw(self,amount):
        if amount>self.balance:
            print("Insufficient  balance.")
        elif amount<=0:
            print("Invalid amount")
        else:
            self.balance-=amount
            self.update_balance()
            self.add_transaction("WithDraw",amount)
            print("Withdrawal successful.")
    def show_transactions(self):
        self.db.cursor.execute("SELECT * FROM transactions WHERE id=?",(self.id))
        transactions = self.db.cursor.fetchall()
        print("Transaction History:")
        for i in transactions:
            print(i)
class SavingsAccount(Account):
    def withDraw(self,amount):
        if amount>self.balance:
            print("Insufficient balance.")
        else:
            super().withDraw(amount)
class CurrentAccount(Account):
    overdraft_limit = 500
    def withDraw(self, amount):
        if amount>self.balance+self.overdraft_limit:
            print("Overdraft limit exceeded.")
        else:
            self.balance-=amount
            self.update_balance()
            self.add_transaction("withdraw",amount)
            print("Withdrawal successful for Current Account.")
class Bank:
    def __init__(self):
        self.db=Database()
    def create_account(self):
        username=input("Please enter your username: ")
        password=input("Please enter your password: ")
        acc_type=input("enter the type from pres(1 for savings 2 for current): ").lower()
        if acc_type=="1":
            acc_type="savings"
        else:
            acc_type="current"
        try:
            self.db.cursor.execute("INSERT INTO accounts (username, password, balance, type) VALUES (?,?,?,?) ",(username,password,0,acc_type))
            self.db.conn.commit()
            print("account created successfully. ")
        except:
            print("Username already exists.")
    def login(self):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        self.db.cursor.execute("SELECT id,type  FROM accounts WHERE username=? and password=?",(username,password))
        result=self.db.cursor.fetchone()
        if result :
            acc_id,balance,acc_type=result
            if acc_type == "savings":
                return SavingsAccount(self.db, acc_id, username, balance)
            else:
                return CurrentAccount(self.db, acc_id, username, balance)
        else:
            print("Invalid login.")
            return None
class Admin:
    def __init__(self):
        self.db=Database()
    def view_all_accounts(self):
        self.db.cursor.execute("SELECT id, username, balance, type FROM accounts")
        accounts = self.db.cursor.fetchall()
        print("All Accounts:")
        for acc in accounts:
            print(acc)
    def view_all_transactions(self):
        self.db.cursor.execute("SELECT * FROM transactions")
        transactions = self.db.cursor.fetchall()
        print("All Transactions:")
        for t in transactions:
            print(t)
bank=Bank()
admin=Admin()
while True:
    print("1. Create Account")
    print("2. Login")
    print("3. Admin View")
    print("4. Exit")
    choice=input("Enter your choice: ")
    if choice=="1":
        bank.create_account()
    elif choice=="2":
        account=bank.login()
        if account:
            while True:
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Show Transactions")
                print("4. Logout")
                acc_choice=input("Enter your choice: ")
                if acc_choice=="1":
                    amount=float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                elif acc_choice=="2":
                    amount=float(input("Enter amount to withdraw: "))
                    account.withDraw(amount)
                elif acc_choice=="3":
                    account.show_transactions()
                elif acc_choice=="4":
                    break
                else:
                    print("Invalid choice.")
    elif choice=="3":
        while True:
            print("1. View All Accounts")
            print("2. View All Transactions")
            print("3. Back to Main Menu")
            admin_choice=input("Enter your choice: ")
            if admin_choice=="1":
                admin.view_all_accounts()
            elif admin_choice=="2":
                admin.view_all_transactions()
            elif admin_choice=="3":
                break
            else:
                print("Invalid choice.")
    elif choice=="4":
        break
    else:
        print("Invalid choice.")



