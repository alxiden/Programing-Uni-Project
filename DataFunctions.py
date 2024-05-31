# Importing libraries
import datetime
import random
import sqlite3
import re
import string
from tkinter import messagebox
import hashlib
import qrcode

# Defining the DataProcessor class
class DataProcessor:
    # Initializing the DataProcessor object
    def __init__(self):
        self.conn = None  # Used f0r the connection to the database
        self.cursor = None  # Used for the cursor for database operations

    # Method to set up the database
    def database_setup(self):
        self.conn = sqlite3.connect('Database/database.db')  # Connect to the database
        self.cursor = self.conn.cursor()  # Create a cursor object

    # Method to log in a user
    def login_user(self, username, password):
        # Check if the username is valid
        if self.username_check(username, 'login') == True:
            # Hash the password for security
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                # Try to fetch the user's account details from the database
                account = self.cursor.execute('SELECT "User_ID", "Active" FROM LoginDetails WHERE username = ? AND password = ?', (username, password_hash)).fetchone()
                # If the account is locked, show an error message
                if account[1] == 'False':
                    messagebox.showerror('Error', 'This account is locked, please contact an administrator')
                # If the account is active, return the account details
                elif account[1] == 'True' or account[1] == '1':
                    return account
                # If the username or password is incorrect, show an error message and log the login attempt
                else:
                    messagebox.showerror('Error', 'Incorrect username or password')
                    self.login_attempts(username)
                    return False
            # If fetching the account details fails, log the login attempt and return False
            except:
                messagebox.showerror('Error', 'Incorrect username or password')
                self.login_attempts(username)
                return False

    
        # Method to check if a username is valid
    def username_check(self, username, mode='new'):
        # Fetch all usernames from the database
        usernames = self.cursor.execute('SELECT username FROM LoginDetails').fetchall()
        # Check if the username length is between 4 and 20 characters
        if len(username) < 4 or len(username) > 20:
            messagebox.showerror('Error', 'Username must be between 4 and 20 characters')
            return False   
        # Check if the username only contains alphanumeric and numbers
        elif re.match(r'^[a-zA-Z0-9]+$', username):
            # Check if the username is already in use when creating a new account
            for i in usernames:
                if username == i[0] and mode == 'new':
                    messagebox.showerror('Error', 'Username already in use')
                    return False
            return True
        else:
            messagebox.showerror('Error', 'Username must only contain letters and numbers')
            return False
        
    # Method to check if a password is valid
    def password_check(self, password, password2):
        # Check if the password length is between 8 and 20 characters
        if len(password) < 8 or len(password) > 20:
            messagebox.showerror('Error', 'Password must be between 8 and 20 characters')
            return False
        # Check if the password contains at least one number
        elif not re.search('[0-9]', password):
            messagebox.showerror('Error', 'Password must contain at least one number')
            return False
        # Check if the password contains at least one uppercase letter
        elif not re.search('[A-Z]', password):
            messagebox.showerror('Error', 'Password must contain at least one uppercase letter')
            return False
        # Check if the password contains at least one lowercase letter
        elif not re.search('[a-z]', password):
            messagebox.showerror('Error', 'Password must contain at least one lowercase letter')
            return False
        # Check if the password contains at least one special character
        elif not re.search('[!£$%^&*()_+{:@~<>?|=-]', password):
            messagebox.showerror('Error', 'Password must contain at least one special character')
            return False
        # Check if the two entered passwords match
        elif password != password2:
            messagebox.showerror('Error', 'Passwords do not match')
            return False
        else:
            return True
        
      # Method to check if an email is valid
    def email_check(self, email, mode='new'):
        # Define the format for a valid email address
        email_format = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        
        # Fetch all emails from the database
        emails = self.conn.execute('SELECT Email FROM Users').fetchall()
        
        # Check if the email matches the defined format
        if not re.fullmatch(email_format, email):
            messagebox.showerror('Error', 'Invalid email address')
            return False
        # Check if the email is already in use
        elif email in emails:
            messagebox.showerror('Error', 'Email already in use')
            return False
        else:
            # Check if the email is already in use
            for i in emails:
                if email == i[0] and mode == 'new':
                    messagebox.showerror('Error', 'Email already in use')
                    return False
            return True
        
    # Method to check if a name is valid
    def name_check(self, name):
        # Check if the name length is between 2 and 20 characters
        if len(name) > 20:
            messagebox.showerror('Error', 'Name must be between 2 and 20 characters')
            return False
        # Check if the name only contains letters
        elif re.match(r'^[a-zA-Z]+$', name):
            return True
        else:
            messagebox.showerror('Error', 'Name must only contain letters')
            return False
    
    # Method to check if an age is valid
    def age_check(self, age):
        # Check if the age is a whole number
        if not re.match(r'^[0-9]+$', age):
            messagebox.showerror('Error', 'Age must be a whole number')
            return False
        # Check if the age is over 18
        elif int(age) < 18:
            messagebox.showerror('Error', 'You must be over 18 to register')
            return False
        else:
            return True

       # Method to check all user registration details
    def register_user_check(self, username, password, password2, email, first_name, last_name,age):
        # Check if the username, password, email, first name, last name, and age are valid
        if self.username_check(username) == False:
            return False
        elif self.password_check(password, password2) == False:
            return False
        elif self.email_check(email) == False:
            return False
        elif self.name_check(first_name) == False:
            return False
        elif self.name_check(last_name) == False:
            return False
        elif self.age_check(age) == False:
            return False
        else:
            return True
        
    # Method to generate a recovery phrase
    def recovery_phrase_gen(self):
        recovery_phrase = ''
        # Generate a 10-character recovery phrase
        for i in range(0, 10):
            recovery_phrase += random.choice(string.ascii_letters)
        return recovery_phrase
    
    # Method to register a new user
    def register_user(self, username, password, password2, email, first_name, last_name, age, account_type):
        # Check if the user registration details are valid
        if self.register_user_check(username, password, password2, email, first_name, last_name,age) == True:
            # Generate a user ID
            user_id = len(self.cursor.execute('SELECT User_ID FROM Users').fetchall()) + 1
            # Generate a recovery phrase
            recovery_phrase = self.recovery_phrase_gen()
            # Show the recovery phrase to the user
            messagebox.showinfo('Recovery Phrase', f'Your recovery phrase is: {recovery_phrase} \n Please keep this safe as there is no way to recover this if lost!')
            # Hash the password and recovery phrase for security
            password_hash = hashlib.sha256(str(password).encode()).hexdigest()
            recovery_phrase_hash = hashlib.sha256(recovery_phrase.encode()).hexdigest()
            # Insert the user's login details into the LoginDetails table
            self.cursor.execute('INSERT INTO LoginDetails (username, password, User_ID, Login_Attempts, Recovery_Attempts, Active) VALUES (?, ?, ?, ?, ?, ?)', (username, password_hash,user_id,0,0, True))
            # Insert the user's personal details into the Users table
            self.cursor.execute('INSERT INTO Users (User_ID, First_Name, Surname, Age, Email, Recovery_Hash, Account_type, Date_Created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, first_name, last_name, age, email, recovery_phrase_hash, account_type, datetime.datetime.now()))
            # Commit the changes to the database
            self.conn.commit()
            # Show a success message to the user
            messagebox.showinfo('Success', 'Account created successfully')
            return True
        
        # Method to handle login attempts
    def login_attempts(self, username):
        # Fetch the number of login attempts for the user
        login_attempts = self.cursor.execute('SELECT Login_Attempts FROM LoginDetails WHERE username = ?', (username,)).fetchall()[0][0]
        # If the number of login attempts is less than 3
        if login_attempts < 3:
            # Increment the number of login attempts
            login_attempts += 1
            # Update the number of login attempts in the database
            self.cursor.execute('UPDATE LoginDetails SET Login_Attempts = ? WHERE username = ?', (login_attempts, username))
            # Commit the changes to the database
            self.conn.commit()
        else:
            # If the number of login attempts is 3 or more, show an error message and lock the account
            messagebox.showerror('Error', 'Account locked')
            self.cursor.execute('UPDATE LoginDetails SET Active = ? WHERE username = ?', (False, username))
            self.conn.commit()

    # Method to handle recovery attempts
    def recovery_attempts(self, username):
        # Fetch the number of recovery attempts for the user
        recovery_attempts = self.cursor.execute('SELECT Recovery_Attempts FROM LoginDetails WHERE username = ?', (username,)).fetchall()[0][0]
        # If the number of recovery attempts is less than 3
        if recovery_attempts < 3:
            # Increment the number of recovery attempts
            recovery_attempts += 1
            # Update the number of recovery attempts in the database
            self.cursor.execute('UPDATE LoginDetails SET Recovery_Attempts = ? WHERE username = ?', (recovery_attempts, username))
            self.conn.commit()
        else:
            # If the number of recovery attempts is 3 or more, show an error message and lock the account
            messagebox.showerror('Error', 'This account is locked, please contact an administrator')
            self.cursor.execute('UPDATE LoginDetails SET Active = ? WHERE username = ?', (False, username))
            self.conn.commit()

    # Method to check the recovery phrase
    def recovery_phrase_check(self, username, recovery_phrase):
        # Fetch the recovery phrase from the database
        recovery_phrase_db = self.cursor.execute('SELECT Recovery_Hash FROM Users WHERE User_ID = (SELECT User_ID FROM LoginDetails WHERE username = ?)', (username,)).fetchall()[0][0]
        # Hash the entered recovery phrase
        recovery_phrase = hashlib.sha256(recovery_phrase.encode()).hexdigest()
        # If the entered recovery phrase matches the one in the database, return True
        if recovery_phrase == recovery_phrase_db:
            return True
        else:
            # If the entered recovery phrase does not match, increment the number of recovery attempts and return False
            self.recovery_attempts(username)
            return False

    # Method to reset the password
    def reset_password(self, username, password, password2, recovery_phrase):
        # Check if the username is valid
        if self.username_check(username, 'reset') == False:
                    return False
        # Check if the password is valid
        elif self.password_check(password, password2) == False:
            return False
        # Check if the recovery phrase is valid
        elif self.recovery_phrase_check(username, recovery_phrase) == False:
            # Show an error message if the password reset failed
            messagebox.showerror('Error', 'Password reset failed')
            return False
        else:
            # Hash the new password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            # Update the password in the database
            self.cursor.execute('UPDATE LoginDetails SET password = ? WHERE username = ?', (password_hash, username))
            # Commit the changes to the database
            self.conn.commit()
            self.cursor.execute('UPDATE LoginDetails SET Recovery_Attempts = ? WHERE username = ?', (0, username))
            self.conn.commit()
            self.cursor.execute('UPDATE LoginDetails SET Login_Attempts = ? WHERE username = ?', (0, username))
            self.conn.commit()
            self.cursor.execute('UPDATE LoginDetails SET Active = ? WHERE username = ?', (True, username))
            self.conn.commit()
            # Show a success message
            messagebox.showinfo('Success', 'Password reset successfully')
            return True
        
    # Method to handle promotion updates
    def promotion_updates(self, id, name, description, start_date, end_date, discount, qr_code, catagory, logo, frame, action):
        # Check if the start date, end date, and discount are valid
        if self.date_check(start_date) == False:
            return False
        elif self.date_check(end_date) == False:
            return False
        elif self.discount_check(discount) == False:
            return False
        
        # If the action is to add a promotion
        if action == 'add':
            # Insert the promotion details into the Promotions table
            catagory = str(catagory).replace('(','').replace(')','').replace('\'','').replace(',','')
            #print(catagory)
            catagory = self.cursor.execute('SELECT Catagory_ID FROM PromotionCatagorys WHERE Catagory_Name = ?', (catagory,)).fetchone()
            catagory = str(catagory).replace('(','').replace(')','').replace('\'','').replace(',','')
            #print(catagory)
            self.cursor.execute('INSERT INTO Promotions (Promo_ID, Name, Description, Start_Date, End_Date, Discount, QRCode, Catagory, Logo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, name, description, start_date, end_date, discount, qr_code, catagory, logo))
            # Commit the changes to the database
            self.conn.commit()
            # Show a success message
            messagebox.showinfo('Success', 'Promotion added successfully')
            frame.grid_forget()
        # If the action is to update a promotion
        elif action == 'update':
            catagory = self.cursor.execute('SELECT Catagory_ID FROM PromotionCatagorys WHERE Catagory_Name = ?', (catagory,)).fetchone()
            catagory = str(catagory).replace('(','').replace(')','').replace('\'','').replace(',','')
            # Update the promotion details in the Promotions table
            self.cursor.execute('UPDATE Promotions SET Name = ?, Description = ?, Start_Date = ?, End_Date = ?, Discount = ?, QRCode = ?, Catagory = ?, Logo = ? WHERE Promo_ID = ?', (name, description, start_date, end_date, discount, qr_code, catagory, logo, id))
            # Commit the changes to the database
            self.conn.commit()
            # Show a success message
            messagebox.showinfo('Success', 'Promotion updated successfully')
            frame.grid_forget()
        else:
            pass


    # Method to generate a QR code for a promotion
    def generate_qr(self, id, name,description, promo_date):
        # Define the name of the QR code image file
        qr_code_name = f'Images/QR/{id}_{name}.png'
        # Create a QR code object
        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=2,
            )
        # Add data to the QR code
        qr.add_data(f'Promotion {id}:,\n{name},\n{description}\n Promotion end date: {promo_date}')
        # Generate the QR code
        qr.make(fit=True)
        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        # Save the image to a file
        img.save(qr_code_name)
        # Return the name of the image file
        return str(qr_code_name)
    
    # Method to check if a date is in the correct format
    def date_check(self, date):
        try:
            # Try to parse the date
            datetime.datetime.strptime(date, '%d/%m/%Y')
            return True
        except:
            # If the date is not in the correct format, show an error message
            messagebox.showerror('Error', 'Invalid date format')
            return False

    # Method to check if a discount is valid
    def discount_check(self, discount):
        # Check if the discount is a whole number
        if not re.match(r'^[0-9]+$', discount):
            messagebox.showerror('Error', 'Discount must be a whole number')
            return False
        # Check if the discount is between 1 and 100
        elif int(discount) <= 0 or int(discount) >= 100:
            messagebox.showerror('Error', r'Discount must be between 1% and 99%')
            return False
        else:
            return True 
        
    # Method to record a promotion purchase
    def brought_promotion(self, promo_id, user_id,):
        # Generate a history ID
        historyid = len(self.cursor.execute('SELECT History_ID FROM PurchaseHistory').fetchall()) + 1
        date = datetime.datetime.now()
        # Insert the purchase into the PurchaseHistory table
        self.cursor.execute('INSERT INTO PurchaseHistory (History_ID, Promo_ID, Users_ID, Date_Brought) VALUES (?, ?, ?, ?)', (historyid, promo_id, user_id, date))
        self.conn.commit()
        messagebox.showinfo('Success', 'Promotion brought successfully')

    def close_account(self, id, root, state = 'Admin'):
        # Update the Active column in the LoginDetails table
        self.cursor.execute('UPDATE LoginDetails SET Active = ? WHERE User_ID = ?', (False, id))
        # Commit the changes to the database
        self.conn.commit()
        # Show a success message
        messagebox.showinfo('Success', 'Account closed successfully')
        # Close the window
        if state == 'Admin':
            root.grid_forget()
        else:
            root.destroy()

        







