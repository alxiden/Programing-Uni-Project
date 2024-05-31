# Standard library imports
import hashlib
import datetime
import shutil
from os.path import exists

# Third party imports
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import sqlite3

# Local imports
import DataFunctions
import Install

class Main(tk.Frame):

    def __init__(self):
        #Application name
        self.app_name = 'D.E.L.I.B.I.R.D.S'

        #Initialise the datafunctions
        self.df = DataFunctions.DataProcessor()

        #Database
        self.database_location = exists('Database/database.db')
        self.conn = ''        

        #promotion information
        self.promo_catagory = ''
        self.new_promotions = ''
        self.prev_promotions =''
        self.all_promotions = ''
                             
        #Windows - Used to check if the window is already open to prevent page duplication
        self.root = ''
        self.account_create = ''
        self.reset_password = ''
        self.admin_verify = ''
        self.admin = ''
        self.account_window = ''
        self.search_popup = ''
        self.scanner_window = ''

        #Images - asigns the images throughout the program
        self.Light_image = ''
        self.Dark_image = ''
        self.search_image = ''
        
        #Size variables - Used to set the size of the widgets
        self.banner_size = 500, 200
        self.button_width = 15
        self.button_padding = 2
        self.font_size = 10
        self.min_width = 600
        self.min_height = 400
        self.font_size_options = ['8', '10', '12', '14', '16', '18', '20',]

        #Colours - Used to set the colours of the widgets
        self.bg_col = 'black'
        self.txt_col = 'white'
        self.ent_txt_col = 'black'
        self.global_theame = 'Dark'

        #User information
        self.user_id = ''
    
    #-----------------Functions-------------------#
    def install_check(self,):
        # Check if the database location exists
        if self.database_location == False:
            messagebox.showinfo(f'{self.app_name} - Install', f'Application not found, now installing {self.app_name}?')
            self.install = Install.Install()
            # Call the create_db method of the Install instance to create the database
            self.install.create_db()
        else:
            # If the database location does exist, connect to the database
            self.conn = sqlite3.connect('Database/database.db')
            self.database = self.conn.cursor()
    # This function changes the theme of the application
    def change_theme(self, theme):
        # Store the theme globally
        self.global_theame = theme
        if theme == 'Dark':
            self.bg_col = 'black'
            self.txt_col = 'white'
            self.ent_txt_col = 'black'
        else:
            self.bg_col = 'white'
            self.txt_col = 'black'
            self.ent_txt_col = 'black'
        # Apply the background color to the root window and the login frame
        self.root.configure(bg = self.bg_col)
        self.login_frame.configure(bg = self.bg_col)
        # Set the banner image to the correct theme
        if self.global_theame == 'Dark':
            self.image = self.Dark_image.resize(self.banner_size, Image.LANCZOS)
        else:   
            self.image = self.Light_image.resize(self.banner_size, Image.LANCZOS)
        # Convert the image to a PhotoImage and apply it to the banner
        self.Banner_img = ImageTk.PhotoImage(self.image)
        self.banner.configure(bg = self.bg_col, image=self.Banner_img)
        # Apply the background and text colors to the username and password labels and entries, and the theme and font size labels and radio buttons
        self.username_label.configure(bg = self.bg_col, fg = self.txt_col)
        self.username_entry.configure(fg = self.ent_txt_col)
        self.password_label.configure(bg = self.bg_col, fg = self.txt_col)
        self.password_entry.configure(fg = self.ent_txt_col)
        self.theme_label.configure(bg = self.bg_col, fg = self.txt_col)
        self.theme_radio1.configure(bg = self.bg_col, fg = self.txt_col, selectcolor=self.bg_col)
        self.theme_radio2.configure(bg = self.bg_col, fg = self.txt_col, selectcolor=self.bg_col)
        self.font_size_label.configure(bg = self.bg_col, fg = self.txt_col)

    # Changes the font size of the application
    def change_font_size(self, size,):
        # Set the global font size to the provided size
        self.font_size = int(size)
        # Adjust the minimum window size based on the font size
        if self.font_size < 14:
            self.min_width = 600
            self.min_height = 400    
        elif self.font_size >= 14 and self.font_size <= 20 :
            self.min_width = 1000
            self.min_height = 500
        # Apply the minimum window size to the root window
        self.root.minsize(self.min_width, self.min_height)
        # Apply the font size to various elements in the UI
        self.username_label.configure(font = (None, self.font_size))
        self.username_entry.configure(font = (None, self.font_size))
        self.password_label.configure(font = (None, self.font_size))   
        self.password_entry.configure(font = (None, self.font_size)  )
        self.theme_label.configure(font = (None, self.font_size))
        self.font_size_label.configure(font = (None, self.font_size))
        self.login_button.configure(font = (None, self.font_size))
        self.register_button.configure(font = (None, self.font_size))   
        self.reset_password_button.configure(font = (None, self.font_size)) 
        self.quit_button.configure(font = (None, self.font_size))   
        self.theme_radio1.configure(font = (None, self.font_size))
        self.theme_radio2.configure(font = (None, self.font_size))
        
    # Sets the Frame defults for pages
    def frame_defults(self, frame, title):
        frame.title(f'{self.app_name} - {title}')
        frame.minsize(self.min_width, self.min_height)
        frame.configure(bg = self.bg_col)
        frame.option_add('*Font', f'Arial {self.font_size}')

    # Handles the login
    def login(self, username, password):
        try:
            # Attempt to login the user with the provided username and password
            account = self.df.login_user(username, password)
            if account == False:
                pass
            else:
                # If the login attempt was successful, store the user's ID and account type
                self.user_id = account[0]
                self.account_type = self.database.execute('SELECT Account_Type FROM Users WHERE User_ID = ?',(self.user_id,)).fetchone()[0]
                if self.account_type == 1:
                    # If the user is an admin, open the admin page
                    self.admin_page()
                else:
                    # If the user is not an admin, open the home page
                    self.home_page()
        except Exception as e:
            messagebox.showerror(f'{self.app_name} - Login', 'Error in login, please contact an admin.')
            #print(e)
            pass

    # Handles the registration and account updates
    def account_updates(self,id,username,password,name,last_name,email,account_type, frame, age, state):
        #print(id,username,password,name,last_name,email,account_type, frame, state)
        # If the user is not an admin, open the home page
        if username == '' or password == '' or name == '' or last_name == '' or email == '' or account_type == '':
            messagebox.showerror(f'{self.app_name} - Add Account', 'Please fill in all fields')
            return False
        # Check if the username is valid
        elif self.df.username_check(username, mode='update') == False:
            messagebox.showerror(f'{self.app_name} - Add Account', 'Username must be less than 20 characters and not contain any special characters')
            return False
        # Check if the email is valid
        elif self.df.email_check(email, mode='update') == False:
            messagebox.showerror(f'{self.app_name} - Add Account', 'Please enter a valid email address')
            return False
        # Check if the name is valid
        elif self.df.name_check(name) == False:
            messagebox.showerror(f'{self.app_name} - Add Account', 'Please enter a valid name')
            return False
        # Check if the last name is valid
        elif self.df.name_check(last_name) == False:
            messagebox.showerror(f'{self.app_name} - Add Account', 'Please enter a valid surname')
            return False
        elif self.df.age_check(age) == False:
            messagebox.showerror(f'{self.app_name} - Add Account', 'Please enter a valid age')
            return False
        if account_type == 'Admin':
            account_type = 1
        elif account_type == 'User':
            account_type = 2
        
         

        if state == 'Update':
            try:
                # If the password has not changed, use the existing password
                if password == self.database.execute('SELECT Password FROM LoginDetails WHERE User_ID = ?',(id,)).fetchone()[0]:
                    password_hash = password
                else:
                    # If the password has changed, hash the new password
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                account_type_clean = str(account_type).replace('(','').replace(')','').replace('\'','').replace(',','')
                # Update the user's details in the Users table
                self.database.execute('''UPDATE main.Users SET First_Name = ?, Surname = ?, Email = ?, Account_Type = ? WHERE User_ID = ?;''',(name,last_name,email,account_type_clean,id))
                self.conn.commit()
                # Update the user's login details in the LoginDetails table
                self.database.execute('''UPDATE 'main'.'LoginDetails' SET 'Username' = ?, 'Password' = ? WHERE 'User_ID' = ?;''',(username,password_hash,id))
                self.conn.commit()
                messagebox.showinfo(f'{self.app_name} - Add Account', 'Account Updated')
                try:
                    frame.grid_forget()
                except:
                    pass
            except Exception as e:
                messagebox.showerror(f'{self.app_name} - Add Account', 'Error in update, please contact an admin.')
                #print(e)
                return False
        elif state == 'Add':
            try:
                # Generate a recovery phrase and hash it
                recovery_phrase = self.df.recovery_phrase_gen()
                recovery_hash = hashlib.sha256(recovery_phrase.encode()).hexdigest()
                date_added = datetime.datetime.now().strftime('%d/%m/%Y')
                # Hash the password
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                account_type_clean = str(account_type).replace('(','').replace(')','').replace('\'','').replace(',','')
                account_type_id = self.database.execute('SELECT Type_ID FROM AccountTypes WHERE Account_Type_Name = ?',(account_type_clean,)).fetchone()
                # Insert the new user into the Users table
                self.database.execute('''INSERT INTO 'main'.'Users'('First_Name', 'Surname', 'Email', 'Account_Type', 'Date_Created', 'Recovery_Hash') VALUES (?, ?, ?, ?, ?, ?);''',(name,last_name,email,account_type_id[0],date_added, recovery_hash))
                self.conn.commit()
                # Insert the new user's login details into the LoginDetails table
                self.database.execute('''INSERT INTO 'main'.'LoginDetails'('Username', 'Password', 'User_ID', 'Active') VALUES (?, ?, (SELECT User_ID FROM Users WHERE Email = ?), 'True');''',(username,password_hash,email))
                messagebox.showinfo(f'{self.app_name} - Add Account', f'The account recovery phrase is {recovery_phrase}')
                self.conn.commit()
                messagebox.showinfo(f'{self.app_name} - Add Account', 'Account Added')
                self.account_ID_num_lable.configure(text = len(self.database.execute('SELECT User_ID FROM Users').fetchall()) + 1)
                frame.grid_forget()
            except Exception as e:
                messagebox.showerror(f'{self.app_name} - Add Account', 'Error in creation, please contact an admin.')
                #print(e)
        try:        
            self.acc_update_button.configure(state='disabled')
            self.acc_delete_button.configure(state='disabled') 
        except:
            pass  

    def search_function(self,search_type,text):
        self.search_page()
        frame = self.search_popup
        results = ''
        if search_type == 'Promotions':
            results = self.database.execute('SELECT * FROM Promotions WHERE Name LIKE ? OR Description LIKE ?',(text,text)).fetchall()
        elif search_type == 'Accounts':
            for i in text:
                if i == '':
                    pass
                else:
                    results = self.database.execute('SELECT * FROM Users WHERE First_Name LIKE ? OR Surname LIKE ? OR Email LIKE ?',(i,i,i)).fetchall()
                    if len(results) == 0:
                        results = self.database.execute('SELECT * FROM LoginDetails WHERE Username LIKE ?',(i,)).fetchall()
                        if len(results) != 0:
                            #print(results[0][3])
                            results = self.database.execute('SELECT * FROM Users WHERE User_ID = ?',(results[0][3],)).fetchall()
        else:
            messagebox.showerror(f'{self.app_name} - Search', 'Error in search, please contact an admin.')
        if len(results) == 0:
            messagebox.showinfo(f'{self.app_name} - Search', 'No results found')

        promo_col = 0
        promo_row = 1
        results_frame = tk.Frame(frame, bg = self.bg_col, border=3, relief='solid')
        results_frame.grid(row = 1, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding, rowspan=6, columnspan=5)
        self.promo_var = tk.StringVar(results_frame)
        for promo in results:
            text = f'{promo[1]}: {promo[2]}'
            radiobutton = tk.Radiobutton(results_frame, text = text, variable=self.promo_var, selectcolor=self.bg_col, bg=self.bg_col, fg= self.txt_col, tristatevalue=0, value = promo[0],)
            radiobutton.grid(row = promo_row, column = promo_col, sticky=tk.W, padx=5, pady=5)
            promo_row += 1
                
        
        confirm_button = tk.Button(results_frame, text='Confirm', width=self.button_width, relief='ridge', command=lambda: self.return_data(search_type,self.promo_var.get()))
        confirm_button.grid(row = promo_row, column = 0, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)
        
    def return_data(self, type, id):
        if type == 'Promotions':
            self.promo_data = self.database.execute('SELECT * FROM Promotions WHERE Promo_ID = ?',(id,)).fetchone()

            #empty/reset the fields
            promo_id = len(self.database.execute('SELECT Promo_ID FROM Promotions').fetchall())+ 1
            self.promo_ID_num_lable.configure(text = promo_id)
            self.promo_name_entry.delete(0, 'end')
            self.promo_description_entry.delete(1.0, 'end')
            self.promo_start_date_entry.delete(0, 'end')
            self.promo_end_date_entry.delete(0, 'end')
            self.promo_discount_entry.delete(0, 'end')
            self.promo_qr_code_entry.delete(0, 'end')
            self.promo_catagory_var.set('')
            self.logo_path_entry.delete(0, 'end')
            
            #insert the data
            self.promo_ID_num_lable.configure(text = self.promo_data[0])
            self.promo_name_entry.insert(0,self.promo_data[1])
            self.promo_description_entry.insert(1.0,self.promo_data[2])
            self.promo_start_date_entry.insert(0, self.promo_data[3])
            self.promo_end_date_entry.insert(0, self.promo_data[4])
            self.promo_discount_entry.insert(0, self.promo_data[6])
            self.promo_qr_code_entry.insert(0, self.promo_data[7])
            #print(self.promo_data[8])
            catagory = self.database.execute('SELECT Catagory_Name FROM PromotionCatagorys WHERE Catagory_ID = ?',(self.promo_data[8],)).fetchone()
            #print(catagory)
            self.promo_catagory_var.set(catagory[0])
            self.logo_path_entry.insert(0, self.promo_data[9])
            self.update_button.configure(state='normal')
            self.delete_button.configure(state='normal')
        elif type == 'Accounts':
            
            #empty/reset the fields
            account_id = len(self.database.execute('SELECT User_ID FROM Users').fetchall())+ 1
            self.account_ID_num_lable.configure(text = account_id)
            self.account_username_entry.delete(0, 'end')
            self.account_password_entry.delete(0, 'end')
            self.account_name_entry.delete(0, 'end')
            self.account_last_name_entry.delete(0, 'end')
            self.account_email_entry.delete(0, 'end')
            self.account_age_entry.delete(0, 'end')
            try:
                self.account_type_entry.set('')
            except:
                pass

            #insert the data
            self.account_data = self.database.execute('SELECT * FROM Users WHERE User_ID = ?',(id,)).fetchone()
            self.logindata = self.database.execute('SELECT * FROM LoginDetails WHERE User_ID = ?',(id,)).fetchone()
            self.account_ID_num_lable.configure(text = self.account_data[0])
            self.account_username_entry.insert(0,self.logindata[1])
            self.account_password_entry.insert(0,self.logindata[2])
            self.account_name_entry.insert(0,self.account_data[1])
            self.account_last_name_entry.insert(0,self.account_data[2])
            self.account_email_entry.insert(0,self.account_data[4])
            self.account_age_entry.insert(0,self.account_data[3])
            try:
                account_type = self.database.execute('SELECT Account_Type_Name FROM AccountTypes WHERE Type_ID = ?',(self.account_data[5],)).fetchone()

                self.account_type_entry.set(account_type[0])
                self.acc_update_button.configure(state='normal')
                self.acc_delete_button.configure(state='normal')   
                self.disable_button.configure(state='normal') 
            except Exception as e:
                #print(e)
                pass
            
                    
        else:
            messagebox.showerror(f'{self.app_name} - Search', 'Error in search, please contact an admin.')
        try:
            self.search_popup.destroy()
        except:
            pass
    
    #Deletes the promotion or account from the database
    def delete_data(self, type, id, frame):
        if type == 'Promotions':
            messagebox.choice = messagebox.askyesno(f'{self.app_name} - Search', 'Are you sure you want to delete this promotion?')
            if messagebox.choice == True:
                self.database.execute('DELETE FROM Promotions WHERE Promo_ID = ?',(id,))
                self.conn.commit()
                messagebox.showinfo(f'{self.app_name} - Search', 'Promotion Deleted')
                frame.grid_forget()
        elif type == 'Accounts':
            messagebox.choice = messagebox.askyesno(f'{self.app_name} - Search', 'Are you sure you want to delete this account?')
            if messagebox.choice == True:
                self.database.execute('DELETE FROM Users WHERE User_ID = ?',(id,))
                self.conn.commit()
                self.database.execute('DELETE FROM LoginDetails WHERE User_ID = ?',(id,))
                self.conn.commit()
                messagebox.showinfo(f'{self.app_name} - Search', 'Account Deleted')
                frame.grid_forget()
        else:
            messagebox.showerror(f'{self.app_name} - Search', 'Error in search, please contact an admin.')
    
    #disables the account
    def disable_account(self, id):
        try:
            self.database.execute('UPDATE LoginDetails SET Active = "False" WHERE User_ID = ?',(id,))
            self.conn.commit()
            messagebox.showinfo(f'{self.app_name} - Search', 'Account Disabled')
        except Exception as e:
            messagebox.showerror(f'{self.app_name} - Search', 'Error in search, please contact an admin.')
            #print(e)
        self.disable_button.configure(state='disabled')
        self.acc_delete_button.configure(state='disabled')
        self.acc_update_button.configure(state='disabled')

    #file browser for the logo
    def file_browser(self,):
        try:
            file_path = filedialog.askopenfilename(initialdir = '/Images',title = 'Select file',filetypes = (('jpeg files','*.jpg'),('PNG files','*.png'),))
            filename = file_path.split('/')[-1] 
            shutil.copy(file_path, f'Images/{filename}')
            new_file_path = f'Images/{filename}'
            return new_file_path
        except Exception as e:
            #print(e)
            return False
    #-----------------Widget Generation-------#
    
    #creates the account fields for the admin page   
    def account_fields(self, frame, update = False):

        account_ID_lable = tk.Label(frame, text = 'Account ID:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5,)
        account_ID_lable.grid(row = 4, column = 0,sticky='E')

        if update == True:
            self.account_ID_num_lable = tk.Label(frame, text = len(self.database.execute('SELECT User_ID FROM Users').fetchall()) + 1, bg = self.bg_col, fg = self.txt_col, padx=5, pady=5, )
            self.account_ID_num_lable.grid(row = 4, column = 1,sticky='E') 

            self.account_type_entry = tk.StringVar(frame)
            account_type_list = self.database.execute('SELECT Account_Type_Name FROM AccountTypes').fetchall()
            self.account_type_optionbox = tk.OptionMenu(frame, self.account_type_entry, *account_type_list,)
            self.account_type_optionbox.configure(width= 23)
            self.account_type_optionbox.grid(row = 12, column = 1, sticky='W', columnspan=2)

        else:
            self.account_ID_num_lable = tk.Label(frame, text = self.user_id, bg = self.bg_col, fg = self.txt_col, padx=5, pady=5, )
            self.account_ID_num_lable.grid(row = 4, column = 1,sticky='E')

            account_type = self.database.execute('SELECT Account_Type FROM Users WHERE User_ID = ?',(self.user_id,)).fetchone()
            self.account_type_entry = self.database.execute('SELECT Account_Type_Name FROM AccountTypes WHERE Type_ID = ?',(account_type)).fetchone()[0]
            self.account_type_lable_1 = tk.Label(frame, text = self.account_type_entry, bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
            self.account_type_lable_1.grid(row = 11, column = 1,sticky='W')

        account_username_lable = tk.Label(frame, text = 'Username:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        self.account_username_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        account_password_lable = tk.Label(frame, text = 'Password:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5,)
        self.account_password_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30, show='*')
        account_name_lable = tk.Label(frame, text = 'Name:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        self.account_name_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        account_last_name_lable = tk.Label(frame, text = 'Surname:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        self.account_last_name_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        account_age_lable = tk.Label(frame, text = 'Age:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        self.account_age_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        account_email_lable = tk.Label(frame, text = 'Email:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        self.account_email_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        account_type_lable = tk.Label(frame, text = 'Account Type:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        
        row = 5
        column = 0
        lable_widgets = [account_ID_lable, account_username_lable, account_password_lable, account_name_lable, account_last_name_lable,account_age_lable, account_email_lable, account_type_lable]
        for widget in lable_widgets:
            widget.grid(row = row, column = column, sticky='E', padx = self.button_padding, pady = self.button_padding)
            row += 1

        entry_widgets = [self.account_ID_num_lable, self.account_username_entry, self.account_password_entry, self.account_name_entry, self.account_last_name_entry, self.account_age_entry, self.account_email_entry]
        row = 5
        column = 1
        for widget in entry_widgets:
            widget.grid(row = row, column = column, sticky='W', padx = self.button_padding, pady = self.button_padding)
            row += 1

        

        if update == True:
            try:
                self.promo_search_frame.grid_forget()
            except:
                pass
            self.account_search_frame.grid(row = 4, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding, rowspan=6, columnspan=5)

            frame_buttons = tk.Frame(self.account_search_frame, bg = self.bg_col, border=3, relief='solid')
            frame_buttons.grid(row = 5, column = 3, sticky=tk.N, padx = self.button_padding, pady = self.button_padding,rowspan=6, columnspan=5)

            self.disable_button = tk.Button(frame_buttons, text='Disable', width=self.button_width, relief='ridge', state='disabled', command= lambda: self.df.close_account(self.account_ID_num_lable.cget('text'), frame))
            self.disable_button.grid(row = 3, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

            search_button = tk.Button(frame_buttons, text='Search', width=self.button_width, relief='ridge', command=lambda: self.search_function('Accounts',[self.account_name_entry.get(),
                                                                                                                                                              self.account_username_entry.get(),
                                                                                                                                                              self.account_last_name_entry.get(),
                                                                                                                                                              self.account_email_entry.get() ],))  
            search_button.grid(row = 4, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

            account_add_button = tk.Button(frame_buttons, text='Add', width=self.button_width, relief='ridge', command=lambda: self.account_updates(self.account_ID_num_lable.cget('text'),
                                                                                                                                                    self.account_username_entry.get(),
                                                                                                                                                    self.account_password_entry.get(),
                                                                                                                                                    self.account_name_entry.get(),
                                                                                                                                                    self.account_last_name_entry.get(),
                                                                                                                                                    self.account_email_entry.get(),
                                                                                                                                                    self.account_type_entry.get(),
                                                                                                                                                    frame,
                                                                                                                                                    self.account_age_entry.get(),
                                                                                                                                                    'Add'))
            account_add_button.grid(row = 6, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

            self.acc_update_button = tk.Button(frame_buttons, text='Update', width=self.button_width, relief='ridge',state='disabled', command=lambda: self.account_updates(self.account_ID_num_lable.cget('text'),
                                                                                                                                                                            self.account_username_entry.get(),
                                                                                                                                                                            self.account_password_entry.get(),
                                                                                                                                                                            self.account_name_entry.get(),
                                                                                                                                                                            self.account_last_name_entry.get(),
                                                                                                                                                                            self.account_email_entry.get(),
                                                                                                                                                                            self.account_type_entry.get(),
                                                                                                                                                                            frame,
                                                                                                                                                                            self.account_age_entry.get(),
                                                                                                                                                                            'Update'))
            self.acc_update_button.grid(row = 12, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

            self.acc_delete_button = tk.Button(frame_buttons, text='Delete', width=self.button_width, relief='ridge',state='disabled', command=lambda: self.delete_data('Accounts',self.account_ID_num_lable.cget('text'),frame))
            self.acc_delete_button.grid(row = 7, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)
         
    #creates the promotion fields for the admin page
    def promo_fields(self, frame, update = False):
        id_num = len(self.database.execute('SELECT Promo_ID FROM Promotions').fetchall()) + 1

        self.promo_ID_lable = tk.Label(frame, text = 'Promotion ID:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5,)
        promo_name_lable = tk.Label(frame, text = 'Promotion Name:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_description_lable = tk.Label(frame, text = 'Promotion Description:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_start_date_lable = tk.Label(frame, text = 'Promotion Start Date:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_end_date_lable = tk.Label(frame, text = 'Promotion End Date:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_discount_lable = tk.Label(frame, text = 'Promotion Discount:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_catagory_lable = tk.Label(frame, text = 'Promotion Catagory:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_qr_code_lable = tk.Label(frame, text = 'Promotion QR Code:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        logo_path_label = tk.Label(frame, text = 'Logo Path:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)

        widget_list = [self.promo_ID_lable, promo_name_lable,promo_description_lable, promo_start_date_lable, promo_end_date_lable, promo_discount_lable, promo_catagory_lable, promo_qr_code_lable, logo_path_label]
        row = 4
        column = 0
        for widget in widget_list:
            widget.grid(row = row, column = column, sticky='E', padx = self.button_padding, pady = self.button_padding)
            row += 1

        self.promo_ID_num_lable = tk.Label(frame, text = id_num, bg = self.bg_col, fg = self.txt_col, padx=5, pady=5,)
        self.promo_name_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        self.promo_description_entry = tk.Text(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30,height=5)
        self.promo_start_date_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        self.promo_end_date_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        self.promo_discount_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        self.promo_catagory_list = self.database.execute('SELECT Catagory_Name FROM PromotionCatagorys').fetchall()

        self.promo_catagory_var = tk.StringVar(frame)
        promo_catagory_dropdown = tk.OptionMenu(frame, self.promo_catagory_var, *self.promo_catagory_list,)
        promo_catagory_dropdown.configure(width= 23)

        self.logo_path_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        self.promo_qr_code_entry = tk.Entry(frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30)
        
        widget_list = [self.promo_ID_num_lable, self.promo_name_entry, self.promo_description_entry, self.promo_start_date_entry, self.promo_end_date_entry, self.promo_discount_entry, promo_catagory_dropdown,self.promo_qr_code_entry, self.logo_path_entry,]
        row = 4
        column = 1
        for widget in widget_list:
            widget.grid(row = row, column = column, sticky='W', padx = self.button_padding, pady = self.button_padding)
            row += 1

        if update == True:
            self.account_search_frame.grid_forget()
            self.promo_search_frame.grid(row = 7, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding, rowspan=6, columnspan=5)
            
            frame_buttons = tk.Frame(self.promo_search_frame, bg = self.bg_col, border=3, relief='solid')
            frame_buttons.grid(row = 6, column = 3, sticky=tk.N, padx = self.button_padding, pady = self.button_padding, rowspan=20, columnspan=2)

            #qr_code_button = tk.Button(frame_buttons, text='QR Code Search', width=self.button_width, relief='ridge', command=lambda: self.camera_window()) Not being included on release
            search_button = tk.Button(frame_buttons, text='Search', width=self.button_width, relief='ridge', command=lambda: self.search_function('Promotions',self.promo_name_entry.get(),))
            self.update_button = tk.Button(frame_buttons, text='Update', state='disabled', width=self.button_width, relief='ridge', command=lambda: self.df.promotion_updates(self.promo_ID_num_lable.cget('text'),
                                                                                                                                                    self.promo_name_entry.get(),
                                                                                                                                                    self.promo_description_entry.get(1.0, 'end'),
                                                                                                                                                    self.promo_start_date_entry.get(),
                                                                                                                                                    self.promo_end_date_entry.get(),
                                                                                                                                                    self.promo_discount_entry.get(),
                                                                                                                                                    self.promo_qr_code_entry.get(),
                                                                                                                                                    self.promo_catagory_var.get(),
                                                                                                                                                    self.logo_path_entry.get(),
                                                                                                                                                    frame,
                                                                                                                                                    'update' ))
            self.delete_button = tk.Button(frame_buttons, text='Delete', state='disabled', width=self.button_width, relief='ridge', command=lambda: self.delete_data('Promotions',self.promo_ID_num_lable.cget('text'),frame))
            promo_add_button = tk.Button(frame_buttons, text='Add', width=self.button_width, relief='ridge', command=lambda: self.df.promotion_updates(self.promo_ID_num_lable.cget('text'),
                                                                                                                                                    self.promo_name_entry.get(),
                                                                                                                                                    self.promo_description_entry.get(1.0, 'end'),
                                                                                                                                                    self.promo_start_date_entry.get(),
                                                                                                                                                    self.promo_end_date_entry.get(),
                                                                                                                                                    self.promo_discount_entry.get(),
                                                                                                                                                    self.promo_qr_code_entry.get(),
                                                                                                                                                    self.promo_catagory_var.get(),
                                                                                                                                                    self.logo_path_entry.get(),
                                                                                                                                                    frame,
                                                                                                                                                    'add'))
            spacer_label1 = tk.Label(frame_buttons, text = '', bg = self.bg_col, fg = self.txt_col, pady= 10)
            spacer_label2 = tk.Label(frame_buttons, text = '', bg = self.bg_col, fg = self.txt_col, pady= 10)
            generate_QR_code_button = tk.Button(frame_buttons, text='Generate QR Code', width=self.button_width, relief='ridge', command= lambda: self.promo_qr_code_entry.insert(0,self.df.generate_qr(self.promo_ID_num_lable.cget('text'),
                                                                                                                                                                                                        self.promo_name_entry.get(),
                                                                                                                                                                                                        self.promo_description_entry.get(1.0, 'end'),
                                                                                                                                                                                                        self.promo_end_date_entry.get(),)))
            File_browser_button = tk.Button(frame_buttons, text='Browse', width=self.button_width, relief='ridge', command=lambda: self.logo_path_entry.insert(0,self.file_browser()))

            widget_list = [search_button, self.update_button, self.delete_button, promo_add_button, spacer_label1,spacer_label2, generate_QR_code_button, File_browser_button]
            row = 1
            column = 1
            for widget in widget_list:
                widget.grid(row = row, column = column, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)
                row += 1           
    
    #Catagory button design for the homepage
    def catagory_button(self, frame, row, column, text,colour, command ):
        button = tk.Button(frame, text=text, width=self.button_width, relief='ridge', command=command, bg=colour)
        button.grid(row = row, column = column, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

    #promotion display design for the homepage 
    def promo_frames(self, frame, row, column, text, colour, logo, command):
        promo_frame = tk.Frame(frame, bg = colour, border=3, relief='solid')
        promo_frame.grid(row = row, column = column, sticky=tk.N, padx = self.button_padding, pady = self.button_padding,)

        tk.Label(promo_frame, text = text,fg = self.bg_col, padx=5, pady=5, bg=colour).grid(row = 0, column = 0,sticky='W')
        logo_import = Image.open(logo)
        logo = ImageTk.PhotoImage(logo_import.resize((60, 60), Image.LANCZOS))
        img = tk.Label(promo_frame, image = logo, fg = self.txt_col, padx=5, pady=5,)
        img.photo = logo
        img.grid(row = 0, column = 1,sticky='E')

        tk.Button(promo_frame, text='View', width=15, relief='ridge', command=lambda: self.promo_details_page(command)).grid(row = 2, column = 0, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)
        tk.Button(promo_frame, text='Buy', width=15, relief='ridge', command=lambda : self.df.brought_promotion(command, self.user_id)).grid(row = 2, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

    #Powers the search section of the homepage
    def home_page_search(self,catagory,brought,text):
        try:
            #Checks the searched text and filters
            if text == '' and catagory == 'All Categories' and brought == 'All Promotions':
                messagebox.showerror(f'{self.app_name} - Search', 'Please enter a search term or filter.')
                return False
            
            catagory = str(catagory).replace('(','').replace(')','').replace('\'','').replace(',','')
            
            #Gets the catagory ID
            if catagory == 'All Categories':
                catagory_id = None
            else:
                catagory_id = self.database.execute('SELECT Catagory_ID FROM PromotionCatagorys WHERE Catagory_Name = ?',(catagory,)).fetchone()[0]

            #Generates the search results
                #Searches for catagory only
            if text == '' and catagory_id != None and brought == 'All Promotions':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Catagory = ?',(catagory_id,)).fetchall()
                #Searches for never brought only
            elif text == '' and catagory_id == None and brought == 'Never Brought':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Promo_ID NOT IN (SELECT Promo_ID FROM PurchaseHistory WHERE Users_ID = ?)',(self.user_id,)).fetchall()
                #Searches for brought only
            elif text == '' and catagory_id == None and brought == 'Previously Brought':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Promo_ID IN (SELECT Promo_ID FROM PurchaseHistory WHERE Users_ID = ?)',(self.user_id,)).fetchall()
                #Searches for catagory and search term
            elif text != '' and catagory_id != None and brought == 'All Promotions':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Catagory = ? AND Name LIKE ? OR Description LIKE ?',(catagory_id,f'{text}',f'{text}')).fetchall()
                #Searches for catagory, search term and never brought
            elif text != '' and catagory_id != None and brought == 'Never Brought':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Catagory = ? AND Name LIKE ? AND Promo_ID NOT IN (SELECT Promo_ID FROM PurchaseHistory WHERE Users_ID = ?) OR Description LIKE ?',(catagory_id,f'{text}',self.user_id,f'{text}')).fetchall()
                #Searches for catagory, search term and brought
            elif text != '' and catagory_id != None and brought == 'Previously Brought':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Catagory = ? AND Name LIKE ? AND Promo_ID IN (SELECT Promo_ID FROM PurchaseHistory WHERE Users_ID = ?) OR Description LIKE ?',(catagory_id,f'{text}',self.user_id,f'{text}')).fetchall()
                #Searches for catagory and never brought
            elif text == '' and catagory_id != None and brought == 'Never Brought':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Catagory = ? AND Promo_ID NOT IN (SELECT Promo_ID FROM PurchaseHistory WHERE Users_ID = ?)',(catagory_id,self.user_id)).fetchall()
                #Searches for catagory and brought
            elif text == '' and catagory_id != None and brought == 'Previously Brought':
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Catagory = ? AND Promo_ID IN (SELECT Promo_ID FROM PurchaseHistory WHERE Users_ID = ?)',(catagory_id,self.user_id)).fetchall()
            else:
                searchresults = self.database.execute('SELECT * FROM Promotions WHERE Name LIKE ? OR Description LIKE ?',(f'%{text}%',f'%{text}%')).fetchall()                  
                    
            #Displays the results
            if len(searchresults) == 0:
                messagebox.showinfo(f'{self.app_name} - Search', 'No results found')
            else:
                self.promo_area_frame.forget()
                self.promo_area_frame = tk.Frame(self.home_frame, bg = self.bg_col, border=3, relief='solid')
                self.promo_area_frame.pack()
                row = 0
                column = 0
                for promo in searchresults:
                    bg_colour = self.database.execute('SELECT * FROM PromotionCatagorys WHERE Catagory_ID = ?', (promo[8],)).fetchone()[2]
                    catagory_name = self.database.execute('SELECT Catagory_Name FROM PromotionCatagorys WHERE Catagory_ID = ?',(promo[8],)).fetchone()
                    catagory_name = catagory_name[0]
                    text = f'''{promo[1]}: \n{promo[6]}% off {catagory_name}'''
                    self.promo_frames(self.promo_area_frame, row, column, text, bg_colour, promo[9], promo[0])
                    column += 1
                    if column == 4:
                        row += 1
                        column = 0
        except Exception as e:
            messagebox.showerror(f'{self.app_name} - Search', 'Error in search, please contact an admin.')

    #-----------------Pages-------------------#

    #main application
    def Main(self):
        try:
            if self.root == '':
                self.root = tk.Tk()
            else:
                if self.root.winfo_exists():
                    pass
                else:
                    self.root = tk.Tk()
        except NameError as e:
            self.root = tk.Tk()
            #print(e)

        self.frame_defults(self.root, 'Login')
        self.login_frame = tk.Frame(self.root, bg= self.bg_col, )
        self.login_frame.grid(row=0,column=0)

        try:
            self.install_check()
            self.database_location = 'Database/database.db'

            self.conn = sqlite3.connect(self.database_location)
            self.database = self.conn.cursor()

            self.Light_image = Image.open('Images/create_banner_light.png')
            self.Dark_image = Image.open('Images/create_banner_dark.png')
            self.df.database_setup()
        except Exception as e:
            messagebox.showerror(f'{self.app_name} - Error', 'Error in Install, Please ensure that the install file is in the same location or contact an admin for further help.')
            self.root.quit()
            #print(e)

        #Banner
        if self.global_theame == 'Dark':
            self.image = self.Dark_image.resize(self.banner_size, Image.LANCZOS)
        else:   
            self.image = self.Light_image.resize(self.banner_size, Image.LANCZOS)

        self.banner_img = ImageTk.PhotoImage(self.image)
        self.banner = tk.Label(self.login_frame, image = self.banner_img, bg = self.bg_col)
        self.banner.grid(row = 0, column = 0, columnspan=5)
        

        #Username
        self.username_label = tk.Label(self.login_frame, text = 'Username:', bg = self.bg_col, fg = self.txt_col, font = (None, self.font_size))
        self.username_label.grid(row = 1, column = 0, sticky='E')

        self.username_entry = tk.Entry(self.login_frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        self.username_entry.grid(row = 1, column = 1, sticky='W', columnspan=2)

        #Password
        self.password_label = tk.Label(self.login_frame, text = 'Password:', bg = self.bg_col, fg = self.txt_col, font = (None, self.font_size))
        self.password_label.grid(row = 2, column = 0, sticky='E')

        self.password_entry = tk.Entry(self.login_frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 40, show='*')
        self.password_entry.grid(row = 2, column = 1, sticky='W', columnspan=2)

        #settings
        self.theme_label = tk.Label(self.login_frame, text = 'Theme: ', bg = self.bg_col, fg = self.txt_col, font = (None, self.font_size))
        self.theme_label.grid(row = 1, column = 4, sticky=tk.E)

        
        theame_selection = tk.StringVar(self.root, str(self.global_theame))

        self.theme_radio1 = tk.Radiobutton(self.login_frame, text = 'Dark', variable=theame_selection, selectcolor=self.bg_col, bg=self.bg_col, fg= self.txt_col, tristatevalue=0, value = 'Dark', command=lambda: self.change_theme('Dark'))
        self.theme_radio1.grid(row = 1, column = 5, sticky=tk.W)

        self.theme_radio2 = tk.Radiobutton(self.login_frame, text='Light',variable=theame_selection, selectcolor=self.bg_col, bg=self.bg_col, fg= self.txt_col, tristatevalue=0, value = 'Light', command=lambda: self.change_theme('Light'))
        self.theme_radio2.grid(row = 2, column = 5, sticky=tk.W)

        self.font_size_label = tk.Label(self.login_frame, text = 'Font Size: ', bg = self.bg_col, fg = self.txt_col, font = (None, self.font_size))
        self.font_size_label.grid(row = 3, column = 4, sticky=tk.W)

        self.font_size_list = tk.StringVar(self.root,)
        self.font_size_list.set(self.font_size_options[0])
        self.font_size_var = tk.StringVar(self.root, str(self.font_size))
        self.font_size_menu = tk.OptionMenu(self.login_frame, self.font_size_var, *self.font_size_options, command= self.change_font_size)
        self.font_size_menu.grid(row = 3, column = 5, sticky=tk.W)


        #Login Button
        self.login_button = tk.Button(self.login_frame, text='Login', width=self.button_width, relief='ridge', command=lambda: self.login(self.username_entry.get(),self.password_entry.get()) )
        self.login_button.grid(row = 3, column = 1, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        #Register Button
        self.register_button = tk.Button(self.login_frame, text='Create Account', width=self.button_width, relief='ridge', command=self.account_create_page)
        self.register_button.grid(row = 3, column = 2, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

        #Reset Password Button
        self.reset_password_button = tk.Button(self.login_frame, text='Reset Password', width=self.button_width, relief='ridge', command=self.reset_password_page)
        self.reset_password_button.grid(row = 4, column = 1, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        #Quit Button
        self.quit_button = tk.Button(self.login_frame, text='Quit', width=self.button_width, relief='ridge', command=self.root.quit)
        self.quit_button.grid(row = 4, column = 2, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)



        self.root.mainloop()

    #account creation page
    def account_create_page(self):
        try:
            if self.account_create == '':
                self.account_create = tk.Toplevel()
            else:
                if self.account_create.winfo_exists():
                    pass
                else:
                    self.account_create = tk.Toplevel()
        except NameError as e:
            self.account_create = tk.Toplevel()
            
        self.frame_defults(self.account_create, 'Create Account')

        username_label = tk.Label(self.account_create, text = 'Username:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        password_label = tk.Label(self.account_create, text = 'Password:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        password_confirm_label = tk.Label(self.account_create, text = 'Confirm Password:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        email_label = tk.Label(self.account_create, text = 'Email:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        name_label = tk.Label(self.account_create, text = 'First Name:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        last_name_label = tk.Label(self.account_create, text = 'Surname:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        age_label = tk.Label(self.account_create, text = 'Age:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)

        label_list = [username_label,password_label,password_confirm_label,name_label,last_name_label,age_label,email_label]
        row = 1
        for i in label_list:
            i.grid(row = row, column = 0, sticky='E')
            row += 1

        username_entry = tk.Entry(self.account_create, fg = self.ent_txt_col, font = (None, self.font_size), width= 40,)
        password_entry = tk.Entry(self.account_create, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        password_confirm_entry = tk.Entry(self.account_create, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        name_entry = tk.Entry(self.account_create, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        last_name_entry = tk.Entry(self.account_create, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        age_entry = tk.Entry(self.account_create, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        email_entry = tk.Entry(self.account_create,fg = self.ent_txt_col, font = (None, self.font_size), width= 40)

        entry_list = [username_entry,password_entry,password_confirm_entry,name_entry,last_name_entry,age_entry,email_entry]
        row = 1
        for i in entry_list:
            i.grid(row = row, column = 1, sticky='W', columnspan=2)
            row += 1

        create_button = tk.Button(self.account_create, text='Create Account', width=self.button_width, relief='ridge',command= lambda: self.df.register_user(username_entry.get(),
                                                                                                                                                                password_entry.get(),
                                                                                                                                                                password_confirm_entry.get(),
                                                                                                                                                                email_entry.get(),
                                                                                                                                                                name_entry.get(),
                                                                                                                                                                last_name_entry.get(),
                                                                                                                                                                age_entry.get(),
                                                                                                                                                                2))
        create_button.grid(row = 8, column = 1, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        exit_button = tk.Button(self.account_create, text='Exit', width=self.button_width, relief='ridge', command=self.account_create.destroy)
        exit_button.grid(row = 8, column = 2, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

    #password reset page
    def reset_password_page(self):
        try:
            if self.reset_password == '':
                self.reset_password = tk.Toplevel()
            else:
                if self.reset_password.winfo_exists():
                    pass
                else:
                    self.reset_password = tk.Toplevel()
        except NameError as e:
            self.reset_password = tk.Toplevel()
            #print(e)
        
        self.frame_defults(self.reset_password, 'Reset Password')

        username_label = tk.Label(self.reset_password, text = 'Username:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        new_password_label = tk.Label(self.reset_password, text = 'New Password:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        confirm_password_label = tk.Label(self.reset_password, text = 'Confirm Password:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        username_entry = tk.Entry(self.reset_password, fg = self.ent_txt_col, font = (None, self.font_size), width= 40,)

        new_password_entry = tk.Entry(self.reset_password, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        confirm_password_entry = tk.Entry(self.reset_password, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)
        recovery_phrase_label = tk.Label(self.reset_password, text = 'Recovery Phrase:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        recovery_phrase_entry = tk.Entry(self.reset_password, fg = self.ent_txt_col, font = (None, self.font_size), width= 40)

        widget_list = [username_label,new_password_label,confirm_password_label,recovery_phrase_label,username_entry,new_password_entry,confirm_password_entry,recovery_phrase_entry]
        row = 1
        for i in range(len(widget_list)):
            if i < 4:
                widget_list[i].grid(row = row, column = 0, sticky='E')
            else:
                if i == 4:
                    row = 1
                widget_list[i].grid(row = row, column = 1, sticky='W', columnspan=2)
            row += 1

        reset_button = tk.Button(self.reset_password, text='Reset Password', width=self.button_width, relief='ridge', command=lambda: self.df.reset_password(username_entry.get(),
                                                                                                                                                        new_password_entry.get(),
                                                                                                                                                        confirm_password_entry.get(),
                                                                                                                                                        recovery_phrase_entry.get()))
        reset_button.grid(row = 5, column = 1, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        exit_button = tk.Button(self.reset_password, text='Exit', width=self.button_width, relief='ridge', command=self.reset_password.destroy)
        exit_button.grid(row = 5, column = 2, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

    #admin page - used to make changes to promotions and accounts
    def admin_page(self):
        try:
            if self.admin == '':
                self.admin = tk.Toplevel()
            else:
                if self.admin.winfo_exists():
                    pass
                else:
                    self.admin = tk.Toplevel()
        except NameError as e:
            self.admin = tk.Toplevel()
            #print(e)
        
        self.frame_defults(self.admin, 'Admin')

        self.search_frame = tk.Frame(self.admin, bg = self.bg_col, border=0, relief='ridge',)
        self.search_frame.grid(row = 0, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding,)

        #self.banner_img = ImageTk.PhotoImage(self.image)
        banner = tk.Label(self.search_frame, image = self.banner_img, bg = self.bg_col)
        banner.grid(row = 0, column = 0, columnspan = 6, padx = 10, pady = 10) 

        self.search_type_var = tk.StringVar(self.search_frame)
        search_raidio1 = tk.Radiobutton(self.search_frame, variable=self.search_type_var, text = 'Promotions',selectcolor=self.bg_col, bg=self.bg_col, fg= self.txt_col, tristatevalue=0, value = 'Promotions', command= lambda : self.promo_fields(self.promo_search_frame,True))
        search_raidio1.grid(row = 2, column = 2, sticky=tk.E )

        search_raidio2 = tk.Radiobutton(self.search_frame, variable=self.search_type_var, text='Accounts', selectcolor=self.bg_col, bg=self.bg_col, fg= self.txt_col, tristatevalue=0, value = 'Accounts', command= lambda : self.account_fields(self.account_search_frame, True))
        search_raidio2.grid(row = 2, column = 3,sticky=tk.W)

        self.account_search_frame = tk.Frame(self.search_frame, bg = self.bg_col, border=0, relief='ridge',)
        self.account_search_frame.grid(row = 4, column = 0, sticky = tk.E, padx = self.button_padding, pady = self.button_padding,)

        self.promo_search_frame = tk.Frame(self.search_frame, bg = self.bg_col, border=0, relief='ridge',)
        self.promo_search_frame.grid(row = 4, column = 0, sticky = tk.W, padx = self.button_padding, pady = self.button_padding, )

    #Homepage after login
    def home_page(self):
        self.login_frame.grid_forget()

        self.home_frame = tk.Frame(self.root, bg= self.bg_col, )
        self.home_frame.grid(row=0,column=0)
        self.home_frame.option_add('*Font', f'Arial {self.font_size}')
        self.home_frame.configure(bg = self.bg_col)
        self.root.title(f'{self.app_name} - Home')
        
        #Catagories
        Nav_bar_frame = tk.Frame(self.home_frame, bg = self.txt_col, border=2, relief='ridge',)
        Nav_bar_frame.pack(anchor=tk.W, fill=tk.X, expand=False)

        self.search_entry = tk.Entry(Nav_bar_frame, fg = self.ent_txt_col, font = (None, self.font_size), width= 30, relief='solid')
        self.search_entry.grid(row = 0, column = 0, sticky='W', columnspan=2, padx = self.button_padding, pady = self.button_padding)

        search_button = tk.Button(Nav_bar_frame, text='Search', width=self.button_width, relief='ridge', command=lambda: self.home_page_search(self.catagory_var.get(),self.prev_option.get(),self.search_entry.get()))
        search_button.grid(row = 0, column = 3, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        self.catagory_var = tk.StringVar(self.root,'All Categories')
        all_catagories = self.database.execute('SELECT Catagory_Name FROM PromotionCatagorys').fetchall()
        all_catagories.insert(0,'All Categories')
        catagory_dropdown = tk.OptionMenu(Nav_bar_frame, self.catagory_var, *all_catagories, )
        catagory_dropdown.configure(width= 10)
        catagory_dropdown.grid(row = 0, column = 4, sticky='W', padx = self.button_padding, pady = self.button_padding)

        options = ['All Promotions', 'Previously Brought', 'Never Brought']
        self.prev_option = tk.StringVar(self.root,'All Promotions')
        prev_brought_dropdown = tk.OptionMenu(Nav_bar_frame, self.prev_option, *options,)
        prev_brought_dropdown.configure(width= 15)
        prev_brought_dropdown.grid(row = 0, column = 5, sticky='W', padx = self.button_padding, pady = self.button_padding)

        spacer = tk.Label(Nav_bar_frame, text = '', bg = self.txt_col, fg = self.txt_col, padx=100, pady=5)
        spacer.grid(row = 0, column = 6, sticky='W')

        settings_frame = tk.Frame(Nav_bar_frame, bg = self.txt_col, border=0, relief='ridge',)
        settings_frame.grid(row = 0, column = 7, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        QR_code_button = tk.Button(settings_frame, text='QR Code', width=self.button_width, relief='ridge', command=lambda: self.camera_window())
        QR_code_button.grid(row = 0, column = 0, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        account_button = tk.Button(settings_frame, text='Account Settings', width=self.button_width, relief='ridge', command=lambda: self.account_page())
        account_button.grid(row = 0, column = 1, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        #Promotion Area
        self.promo_area_frame = tk.Frame(self.home_frame, bg = self.bg_col, border=2, relief='ridge',)
        self.promo_area_frame.pack()

        promo_label = tk.Label(self.promo_area_frame, text = 'Top Promotions', bg = self.bg_col, fg = self.txt_col, padx=5, pady=10)
        promo_label.grid(row = 0, column = 0, columnspan=4)

        promo_row = 1
        promo_col = 0
        self.all_promotions = self.database.execute('SELECT * FROM Promotions').fetchall()
        for promo in self.all_promotions[:20]:
            bg_colour = self.database.execute('SELECT * FROM PromotionCatagorys WHERE Catagory_ID = ?', (promo[8],)).fetchone()[2]
            catagory_name = self.database.execute('SELECT * FROM PromotionCatagorys WHERE Catagory_ID = ?', (promo[8],)).fetchone()[1]
            text = f'''{promo[1]}: \n{promo[6]}% off {catagory_name}'''
            self.promo_frames(self.promo_area_frame,promo_row, promo_col, text,bg_colour, promo[9], promo[0],)
            promo_col += 1
            if promo_col == 4:
                promo_col = 0
                promo_row += 1

    #promotion details page - displays the information about selected promotions
    def promo_details_page(self, promo_id):
        self.promo_details = tk.Toplevel()
        self.promo = self.database.execute('SELECT * FROM Promotions WHERE Promo_ID = ?', (promo_id,)).fetchone()

        self.frame_defults(self.promo_details, 'Promotion Details')

        #Promotion Details
        promo_details_frame = tk.Frame(self.promo_details, bg = self.bg_col, border=0, relief='ridge',)
        promo_details_frame.grid(row = 0, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding, rowspan=2)

        promo_name_label = tk.Label(promo_details_frame, text = f'Promotion Name: {self.promo[1]}', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_description_label = tk.Label(promo_details_frame, text = f'Promotion Description: {self.promo[2]}', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5, wraplength=600, justify='left')
        promo_start_date_label = tk.Label(promo_details_frame, text = f'Promotion Start Date: {self.promo[3]}', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_end_date_label = tk.Label(promo_details_frame, text = f'Promotion End Date: {self.promo[4]}', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_catagory_label = tk.Label(promo_details_frame, text = f'Promotion Catagory: {self.promo[8]}', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_discount_label = tk.Label(promo_details_frame, text = f'Promotion Discount: {self.promo[6]}%', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        promo_qr_code_label = tk.Label(promo_details_frame, text = f'Promotion QR Code:', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        
        

        widget_list = [promo_name_label,promo_description_label,promo_start_date_label,promo_end_date_label,promo_catagory_label,promo_discount_label,promo_qr_code_label]
        row = 0
        column = 0
        for widget in widget_list:
            widget.grid(row = row, column = column, sticky='W')
            row += 1
        qr_image = self.promo[7]

        qr_import = Image.open(qr_image)
        qr_image = ImageTk.PhotoImage(qr_import.resize((200, 200), Image.LANCZOS))
        qr_img = tk.Label(promo_details_frame, image = qr_image, fg = self.txt_col, padx=5, pady=5,)
        qr_img.photo = qr_image
        qr_img.grid(row = 7, column = 0, columnspan=2)

        #Promotion Buttons
        promo_button_frame = tk.Frame(self.promo_details, bg = self.bg_col, border=0, relief='ridge',)
        promo_button_frame.grid(row = 2, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding,)

        promo_buy_button = tk.Button(promo_button_frame, text='Buy', width=self.button_width, relief='ridge', command=lambda : self.df.brought_promotion(self.promo[0], self.user_id))
        promo_buy_button.grid(row = 0, column = 0, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)

        promo_close_button = tk.Button(promo_button_frame, text='Close', width=self.button_width, relief='ridge', command=self.promo_details.destroy)
        promo_close_button.grid(row = 0, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

    #search page - used to display the search results for promotions and accounts
    def search_page(self,):
        try:
            if self.search_popup == '':
                self.search_popup = tk.Toplevel()
            else:
                if self.search_popup.winfo_exists():
                    pass
                else:
                    self.search_popup = tk.Toplevel()
        except NameError as e:
            self.search_popup = tk.Toplevel()
            #print(e)

        self.frame_defults(self.search_popup, 'Search')

        self.search_frame = tk.Frame(self.search_popup, bg = self.bg_col, border=0, relief='ridge',)
        self.search_frame.grid(row = 0, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding,)

        self.results_frame = tk.Frame(self.search_popup, bg = self.bg_col, border=0, relief='ridge',)
        self.results_frame.grid(row = 1, column = 0, sticky = tk.N, padx = self.button_padding, pady = self.button_padding,)

    #account page - used to display the account details and make changes to them
    def account_page(self):
        try:
            if self.account_window == '':
                self.account_window = tk.Toplevel()
            else:
                if self.account_window.winfo_exists():
                    pass
                else:
                    self.account_window = tk.Toplevel()
        except NameError as e:
            self.account_window = tk.Toplevel()
            #print(e)
        
        self.frame_defults(self.account_window, 'Account Settings')

        account_info = self.database.execute('SELECT * FROM Users WHERE User_ID = ?', (self.user_id,)).fetchone()
        login_info = self.database.execute('SELECT * FROM LoginDetails WHERE User_ID = ?', (self.user_id,)).fetchone()

        #Account Details frame
        account_details_frame = tk.Frame(self.account_window, bg = self.bg_col, relief='ridge',)
        account_details_frame.grid(row = 0, column = 0, sticky = tk.N,)

        account_details_label = tk.Label(account_details_frame, text = 'Account Details', bg = self.bg_col, fg = self.txt_col, padx=5, pady=5)
        account_details_label.grid(row = 0, column = 0, sticky='W')

        self.account_fields(account_details_frame, False)
        self.return_data('Accounts',self.user_id,)
        
        frame = ''

        update_button = tk.Button(account_details_frame, text='Update', width=self.button_width, relief='ridge', command=lambda: self.account_updates(self.account_ID_num_lable.cget('text'),
                                                                                                                                                    self.account_username_entry.get(),
                                                                                                                                                    self.account_password_entry.get(),
                                                                                                                                                    self.account_name_entry.get(),
                                                                                                                                                    self.account_last_name_entry.get(),
                                                                                                                                                    self.account_email_entry.get(),
                                                                                                                                                    self.account_type_lable_1.cget('text'),
                                                                                                                                                    frame,
                                                                                                                                                    self.account_age_entry.get(),
                                                                                                                                                    'Update'))
        close_account_button = tk.Button(account_details_frame, text='Close Account', width=self.button_width, relief='ridge', command= lambda: self.df.close_account(self.user_id,self.root,state='Close Account'))
        update_button.grid(row = 14, column = 0, sticky=tk.E, padx = self.button_padding, pady = self.button_padding)
        close_account_button.grid(row = 14, column = 1, sticky=tk.W, padx = self.button_padding, pady = self.button_padding)

    #QR code scanning window - used to scan QR codes
    def camera_window(self):
        
        #cv2.namedWindow("QR Code Scanner")
        vc = cv2.VideoCapture(0)
        qrDecoder = cv2.QRCodeDetector()
        #data = ''

        while True:
            _, frame = vc.read()
            data,bbox, _ = qrDecoder.detectAndDecode(frame)

            if data :
                #print(data)
                qr_data = data
            cv2.imshow("QR Code Scanner - press Q to close", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if data != '':
                break
            
        vc.release()
        cv2.destroyAllWindows()

        try:
            promo_id = qr_data.split(':')[0]
            promo_id = promo_id.replace('Promotion ','')
            #print(promo_id)
            promo_id = int(promo_id)
            self.promo_details_page(promo_id)
        except Exception as e:
            #print(e)
            #messagebox.showerror(f'{self.app_name} - QR Code', 'Error in QR Code, please try again.')
            return False



#--------------Main Program-----------------#

if __name__ == '__main__':
    Main().Main()
