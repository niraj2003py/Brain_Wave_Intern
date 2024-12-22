class Account:
    def __init__(self, user_id, pin, balance=0):  # Fixed the constructor name
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def check_pin(self, pin):
        return self.pin == pin

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(('Deposit', amount))
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient balance'
        else:
            self.balance -= amount
            self.transactions.append(('Withdraw', amount))
            return self.balance

    def get_transaction_history(self):
        return self.transactions if self.transactions else 'No transactions available'

    def transfer(self, target_account, amount):
        if amount > self.balance:
            return 'Insufficient balance'
        else:
            self.withdraw(amount)
            target_account.deposit(amount)
            self.transactions.append(('Transfer', amount))
            return self.balance

    def check_balance(self):  # New method to check available balance
        return self.balance


class ATM:
    def __init__(self):  # Fixed the constructor name
        self.accounts = {}
        self.language = "English"

    def choose_language(self):  # Renamed to avoid conflict
        print("Choose Language:")
        print("1. English")
        print("2. हिंदी")
        choice = input("Enter your choice: ")
        if choice == '1':
            self.language = "English"
        elif choice == '2':
            self.language = "Hindi"
        else:
            print("Invalid choice, defaulting to English.")
            self.language = "English"

    def create_account(self, user_id, pin, balance=0):
        self.accounts[user_id] = Account(user_id, pin, balance)

    def verify_pin(self, account):
        pin_prompt = "Please re-enter your PIN to confirm: " if self.language == "English" else "कृपया लेन-देन की पुष्टि के लिए अपना पिन दोबारा दर्ज करें: "
        pin = input(pin_prompt)
        return account.check_pin(pin)

    def run(self):
        self.choose_language()  # Updated to match the new method name
        welcome_msg = "Welcome to the ATM!" if self.language == "English" else "एटीएम में आपका स्वागत है!"
        insert_card_msg = "Please insert your card to proceed..." if self.language == "English" else "कृपया आगे बढ़ने के लिए अपना कार्ड डालें..."
        press_enter_msg = "Press Enter after inserting your card." if self.language == "English" else "कार्ड डालने के बाद एंटर दबाएं।"

        while True:
            print(welcome_msg)
            print(insert_card_msg)
            input(press_enter_msg)

            atm_interface_msg = "ATM Interface" if self.language == "English" else "एटीएम इंटरफ़ेस"
            access_account_msg = "1. Access Account" if self.language == "English" else "1. खाता एक्सेस करें"
            quit_msg = "2. Quit" if self.language == "English" else "2. बाहर निकलें"
            choice_msg = "Choose an option: " if self.language == "English" else "एक विकल्प चुनें: "
            print(f"\n{atm_interface_msg}")
            print(access_account_msg)
            print(quit_msg)
            choice = input(choice_msg)
            if choice == '1':
                user_id_msg = "Enter your user ID: " if self.language == "English" else "अपना यूजर आईडी दर्ज करें: "
                pin_invalid_msg = "Invalid PIN. Transaction cancelled." if self.language == "English" else "अमान्य पिन। लेन-देन रद्द कर दिया गया।"
                operation_invalid_msg = "Invalid operation." if self.language == "English" else "अमान्य ऑपरेशन।"

                user_id = input(user_id_msg)
                if user_id in self.accounts:
                    account = self.accounts[user_id]
                    while True:
                        operation_msg = "\n1. Transaction History\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Check Balance\n6. Quit" if self.language == "English" else "\n1. लेन-देन का इतिहास\n2. निकासी\n3. जमा\n4. स्थानांतरण\n5. शेष राशि जांचें\n6. बाहर निकलें"
                        operation_prompt = "Choose an operation: " if self.language == "English" else "एक ऑपरेशन चुनें: "
                        print(operation_msg)
                        operation = input(operation_prompt)
                        if operation == '1':
                            history_msg = account.get_transaction_history()
                            print(history_msg if isinstance(history_msg, str) else str(history_msg))
                        elif operation == '2':
                            withdraw_msg = "Enter amount to withdraw: " if self.language == "English" else "निकासी के लिए राशि दर्ज करें: "
                            amount = float(input(withdraw_msg))
                            if self.verify_pin(account):
                                print(account.withdraw(amount))
                            else:
                                print(pin_invalid_msg)
                        elif operation == '3':
                            deposit_msg = "Enter amount to deposit: " if self.language == "English" else "जमा करने के लिए राशि दर्ज करें: "
                            amount = float(input(deposit_msg))
                            if self.verify_pin(account):
                                print(account.deposit(amount))
                            else:
                                print(pin_invalid_msg)
                        elif operation == '4':
                            target_id_msg = "Enter target user ID: " if self.language == "English" else "लक्ष्य उपयोगकर्ता आईडी दर्ज करें: "
                            target_id = input(target_id_msg)
                            transfer_msg = "Enter amount to transfer: " if self.language == "English" else "स्थानांतरण के लिए राशि दर्ज करें: "
                            amount = float(input(transfer_msg))
                            if target_id in self.accounts:
                                if self.verify_pin(account):
                                    print(account.transfer(self.accounts[target_id], amount))
                                else:
                                    print(pin_invalid_msg)
                            else:
                                target_not_found_msg = "Target account not found." if self.language == "English" else "लक्ष्य खाता नहीं मिला।"
                                print(target_not_found_msg)
                        elif operation == '5':  # Option to check balance
                            if self.verify_pin(account):
                                print(f"Available balance: {account.check_balance()}")  # Display the available balance
                            else:
                                print(pin_invalid_msg)
                        elif operation == '6':
                            break
                        else:
                            print(operation_invalid_msg)
                else:
                    user_id_invalid_msg = "Invalid user ID." if self.language == "English" else "अमान्य उपयोगकर्ता आईडी।"
                    print(user_id_invalid_msg)
            elif choice == '2':
                exit_msg = "Thank you for using the ATM. Goodbye!" if self.language == "English" else "एटीएम का उपयोग करने के लिए धन्यवाद। अलविदा!"
                print(exit_msg)
                break
            else:
                invalid_choice_msg = "Invalid choice. Please try again." if self.language == "English" else "अमान्य विकल्प। कृपया पुनः प्रयास करें।"
                print(invalid_choice_msg)


# Create an ATM instance
atm = ATM()
atm.create_account('user1', '1234', 1000)
atm.create_account('user2', '5678', 5000)

# Run the ATM system
atm.run()
