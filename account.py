print("it is printing....")
import random
import json
import re
import datetime


class Accounts:
    def __init__(self):
        print('welcome')
        self.new_account_number = int(random.random() * 10 ** 12)
        self.users = []

    def ReadUsers(self):
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
                self.users = data['users']
        except Exception as e:
            print(e)

    def WriteUsers(self):
        newUsers = {'users': self.users}
        with open('users.json', 'w') as file:
            json.dump(newUsers, file, indent=2)

    def signup(self):
        list1 = [int(i) for i in str(self.new_account_number)]
        print("SIGN UP...")
        self.ReadUsers()
        email_pattern = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        while True:
            name = input("name :")
            email = input("email : ")
            password = input("password :")
            re_password = input("re-enter password :")
            phone = input("enter phone :")
            account_number = None
            balance = 0

            if email == '' or name == '' or password == '' or re_password == '' or phone == '':
                print("fields cannot be empty>>")
                continue
            elif not re.match(email_pattern, email):
                print("email is not valid!")
                continue
            elif password != re_password:
                print("passwords not matched!")
                continue
            else:
                try:
                    phone = int(phone)
                    if self.users:
                        for i in self.users:
                            if email == i['email']:
                                print(f"email {email} already exists")
                                print("please ,try again..")
                                continue
                except:
                    print('phone should be integer')
                    continue
                break

        NewAccount = {
            'name': name,
            'email': email,
            'password': password,
            'phone': int(phone),
            'account_number': self.new_account_number,
            'balance': 0,
            'last_deposited_at': '',
            'last_withdrawn_at': ''

        }

        IsCreate = input("create account y/n :")
        if IsCreate.upper() == 'Y':
            self.users.append(NewAccount)
            try:
                self.WriteUsers()
                print("account created successfully!")
            except Exception as e:
                print(f"something went wrong,try again...{e}")
        else:
            return


class Account(Accounts):
    def __init__(self):
        super().__init__()
        self.signedIn = False
        self.current_user = None

    def SignIn(self):
        print("sign in to your account")
        user_email = input("enter email :")
        user_password = input("enter password: ")
        super().ReadUsers()
        # print(f"self.users -signin - {self.users}")
        if self.users:
            # print(f"self users {self.users}")
            for i in self.users:
                if i['email'] == user_email and i['password'] == user_password:
                    self.current_user = i
                    self.signedIn = True
                    print("signed in successfully!")
        else:
            print("no account found,create one!")
            super().signup()

    def check_balance(self):
        print('---------------------------')
        print(f"available balance: {self.current_user['balance']}")
        print('---------------------------')

    def deposit(self):
        print("deposit to your account>")
        try:
            user_deposit = float(input("amount:"))
            print(user_deposit)
            # print(f"self.users {self.users}")
            for i in self.users:
                # print(i['email'])
                if i['email'] == self.current_user['email']:
                    print(f"{i['email']} {self.current_user['email']}")
                    i['balance'] += user_deposit
                    i['last_deposited_at'] = str(datetime.datetime.now())
                    self.current_user = i
            super().WriteUsers()
            print(f"amount {user_deposit} deposited!")
            print('------------------------------')
        except Exception as e:
            print(f"error depositing {e}")
            print("try again!")

    def withdraw(self):
        print("withdraw..")
        try:
            withdraw_amount = float(input("amount to withdraw: "))
            if withdraw_amount > self.current_user['balance']:
                print("insufficient balance")
                print('---------------------')
            else:
                for i in self.users:
                    if i['email'] == self.current_user['email']:
                        i['balance'] = float(i['balance']) - withdraw_amount
                        i['last_withdrawn_at'] = str(datetime.datetime.now())
                        self.current_user = i
                super().WriteUsers()
                print(f"amount {withdraw_amount} debited!")
                print('---------------------------------')
        except Exception as e:
            print(f"error {e}")
            print("try again..")

    def statement(self):
        print(f"your account statement")
        print('-------------------------------------')
        print(f"Name : {self.current_user['name']}")
        print(f"Email : {self.current_user['email']}")
        print(f"Phone : {self.current_user['phone']}")
        print(f"Account Number  : {self.current_user['account_number']}")
        print(f"Current Balance : {self.current_user['balance']}")
        print(f"Last Deposited At : {self.current_user['last_deposited_at']}")
        print(f"Last Withdrawn At : {self.current_user['last_withdrawn_at']}")
        print('-------------------------------------')


def MyAccount():
    try:
        while True:
            print("1:check balance")
            print("2:deposit")
            print("3:withdraw")
            print("4:statement")
            print("5:logout")
            user_option = int(input("select from above :"))
            if user_option == 1:
                A.check_balance()
                continue
            elif user_option == 2:
                A.deposit()
                continue
            elif user_option == 3:
                A.withdraw()
                continue
            elif user_option == 4:
                A.statement()
                continue
            elif user_option == 5:
                print("logged out successfully!")
                break
            else:
                print("invalid input!")
                continue
    except Exception as e:
        print(f"error - {e}")
        print('try again...')


A = Account()
print("options - ")
print("1 - create an account")
print("2 - log in to your account")
try:
    select = int(input("select an option: "))
    if select == 1:
        A.signup()
        while not A.signedIn:
            user_in = input("log in (y/n): ")
            if user_in.upper() == 'Y':
                A.SignIn()
            else:
                break
        if A.signedIn:
            MyAccount()
    elif select == 2:
        while not A.signedIn:
            user_in = input("log in (y/n): ")
            if user_in.upper() == 'Y':
                A.SignIn()
                if not A.signedIn:
                    print("check email and password, Try again..")
            else:
                break
        if A.signedIn:
            MyAccount()
    else:
        print("invalid input!")
except Exception as e:
    print(e)
