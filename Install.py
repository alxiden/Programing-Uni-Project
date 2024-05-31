#Imports
import sqlite3
import random
import datetime
import hashlib
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import requests
import zipfile
import qrcode

# Class to create the database and insert data
class Install:
    def __init__(self):
        self.conn = ''
        self.Name_list =['Sainsburys','Tesco','Asda','Morrisons','Aldi','Lidl','Waitrose','Co-op','Iceland','M&S','Boots','Superdrug','Wilko','Home Bargains','B&M','Poundland','Poundstretcher']        
        self.use_default = False


    def create_db(self):
        # Create database and tables
        self.folder_creator()
        self.logos()
        self.conn = sqlite3.connect('Database/database.db')
        self.c = self.conn.cursor()
        self.create_tables()
        self.insert_data()
        self.ran_data()
        self.banner_maker()
        self.conn.close()
        
    def date_maker(self):
        # Generate random start and end dates
        start_day = random.randint(1,28)
        start_Month = random.randint(1,12)
        start_Year = random.randint(2023,2027)
        end_day = random.randint(1,28)
        end_Month = random.randint(1,12)
        end_Year = random.randint(start_Year,2028)
        start_date = f'{start_day}/{start_Month}/{start_Year}'
        end_date = f'{end_day}/{end_Month}/{end_Year}'
        created_day = random.randint(1,datetime.datetime.now().day)
        created_Month = random.randint(1,datetime.datetime.now().month)
        created_Year = random.randint(2020, datetime.datetime.now().year)
        created_date = f'{created_day}/{created_Month}/{created_Year}'
        return start_date,end_date, created_date
        

    def create_tables(self):
        #Account Types Table
        self.c.execute('''CREATE TABLE IF NOT EXISTS "AccountTypes" (
	                    "Type_ID" INTEGER NOT NULL UNIQUE,
	                    "Account_Type_Name"	TEXT NOT NULL,
	                    PRIMARY KEY("Type_ID" AUTOINCREMENT))''')
        #Login Details Table
        self.c.execute('''CREATE TABLE IF NOT EXISTS "LoginDetails" (
	                    "Username_ID"	INTEGER NOT NULL UNIQUE,
	                    "Username"	TEXT NOT NULL,
	                    "Password"	NUMERIC NOT NULL,
	                    "User_ID"	INTEGER NOT NULL,
	                    "Login_Attempts"	INTEGER,
	                    "Recovery_Attempts"	INTEGER,
	                    "Active"	TEXT NOT NULL,
	                    FOREIGN KEY("User_ID") REFERENCES "Users"("User_ID"),
	                    PRIMARY KEY("Username_ID" AUTOINCREMENT))''')
        #Promotion Catagorys Table
        self.c.execute('''CREATE TABLE IF NOT EXISTS "PromotionCatagorys" (
	                    "Catagory_ID"	INTEGER NOT NULL UNIQUE,
	                    "Catagory_Name"	TEXT NOT NULL,
	                    "Colour"	TEXT NOT NULL,
	                    PRIMARY KEY("Catagory_ID" AUTOINCREMENT))''')
        #Promotions Table
        self.c.execute('''CREATE TABLE IF NOT EXISTS "Promotions" (
	                    "Promo_ID"	INTEGER NOT NULL UNIQUE,
	                    "Name"	TEXT NOT NULL,
	                    "Description"	TEXT NOT NULL,
	                    "Start_Date"	TEXT NOT NULL,
	                    "End_Date"	TEXT NOT NULL,
                        "Created_Date" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	                    "Discount"	INTEGER NOT NULL,
	                    "QRCode"	TEXT NOT NULL,
	                    "Catagory"	INTEGER NOT NULL,
                        "logo" TEXT NOT NULL DEFAULT 'Images/Logo.png',
	                    FOREIGN KEY("Catagory") REFERENCES "PromotionCatagorys"("Catagory_ID"),
	                    PRIMARY KEY("Promo_ID" AUTOINCREMENT))''')
        #Purchase History Table
        self.c.execute('''CREATE TABLE IF NOT EXISTS "PurchaseHistory" (
	                    "History_ID"	INTEGER NOT NULL UNIQUE,
	                    "Promo_ID"	INTEGER NOT NULL,
	                    "Date_Brought"	TEXT NOT NULL,
	                    "Users_ID"	INTEGER NOT NULL,
	                    FOREIGN KEY("Users_ID") REFERENCES "Users"("User_ID"),
	                    FOREIGN KEY("Promo_ID") REFERENCES "Promotions"("Promo_ID"),
	                    PRIMARY KEY("History_ID" AUTOINCREMENT))''')
        #Users Table
        self.c.execute('''CREATE TABLE IF NOT EXISTS "Users" (
	                    "User_ID"	INTEGER NOT NULL UNIQUE,
	                    "First_Name"	TEXT NOT NULL,
	                    "Surname"	TEXT NOT NULL,
                        "Age" INTEGER NOT NULL DEFAULT 18,
	                    "Email"	TEXT NOT NULL UNIQUE,
	                    "Account_Type"	INTEGER NOT NULL,
	                    "Date_Created"	TEXT NOT NULL,
	                    "Recovery_Hash"	TEXT NOT NULL UNIQUE,
	                    FOREIGN KEY("Account_Type") REFERENCES "AccountTypes"("Type_ID"),
	                    PRIMARY KEY("User_ID" AUTOINCREMENT))''')
        self.conn.commit()
    
    def ran_data(self):

        Discount_list = range(1,99)
        Catagory_list = [1,2,3,4,5,6]
        for i in range(0,100):
            promo_name = random.choice(self.Name_list)
            promo_dates = self.date_maker()
            # Randomly select a discount for the promotion
            promo_discount = random.choice(Discount_list)
            # Randomly select a category for the promotion
            promo_catagory = random.choice(Catagory_list)
            # Map the category number to a category name
            if promo_catagory == 1:
                catagory = 'food'
            elif promo_catagory == 2:
                catagory = 'travel'
            elif promo_catagory == 3:
                catagory = 'home'
            elif promo_catagory == 4:
                catagory = 'clothes'
            elif promo_catagory == 5:
                catagory = 'electronics'
            elif promo_catagory == 6:
                catagory = 'other'
            # Define a list of possible descriptions for the promotion
            Description_list = [f'''Welcome to the wonderful world of {promo_name}. They've got everyday essentials, fabulous finds and the biggest brands in {catagory}, all at up to {promo_discount}% less than the RRP.''',
                                f'''Escape to the fantabulous world of {promo_name} - there's so much going on, the fun never stops! Get {promo_discount}% off {catagory}.''',
                                f'''Enjoy up to {promo_discount}% off selected products at {promo_name}.''',
                                f'''{promo_name} is the UK's leading retailer of {catagory} accessories. Get {promo_discount}% off selected {catagory}.''',
                                f'''Save money when you shop online with {promo_name} eGifts! Get everything you need all delivered directly to your door for {promo_discount}% off.  '''
								]
            # Randomly select a description for the promotion
            promo_description = random.choice(Description_list)
            # Create a QR code object and save it to the QR folder
            qrcode_name = f'Images/QR/{i}_{promo_name}.png'
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=2,
            )
            qr.add_data(f'Promotion {i}:,\n{promo_name},\n{promo_description}\n Promotion end date: {promo_dates[1]}')
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(qrcode_name)

            if self.use_default == True:
                logo_path = 'Images/Logos/Logo.png'
            else:
                logo_path = f'Images/Logos/{promo_name}.png'
            self.c.execute('''INSERT INTO "Promotions" ("Name","Description","Start_Date","End_Date","Created_Date","Discount","QRCode","Catagory","logo") VALUES (?,?,?,?,?,?,?,?,?)''',(promo_name,promo_description,promo_dates[0],promo_dates[1],promo_dates[2], promo_discount,qrcode_name,promo_catagory, logo_path))
            self.conn.commit()
        
    def insert_data(self):
        # Insert account types into the AccountTypes table
        self.c.execute('''INSERT INTO "AccountTypes" ("Type_ID","Account_Type_Name") VALUES (1,'Admin')''')
        self.c.execute('''INSERT INTO "AccountTypes" ("Type_ID","Account_Type_Name") VALUES (2,'User')''')
        self.c.execute('''INSERT INTO "AccountTypes" ("Type_ID","Account_Type_Name") VALUES (3,'Test')''')
        # Insert promotion categories into the PromotionCatagorys table
        self.c.execute('''INSERT INTO "PromotionCatagorys" ("Catagory_ID","Catagory_Name","Colour") VALUES (1,'Food','Turquoise')''')
        self.c.execute('''INSERT INTO "PromotionCatagorys" ("Catagory_ID","Catagory_Name","Colour") VALUES (2,'Travel','Light Blue')''')
        self.c.execute('''INSERT INTO "PromotionCatagorys" ("Catagory_ID","Catagory_Name","Colour") VALUES (3,'Home','Light Green')''')
        self.c.execute('''INSERT INTO "PromotionCatagorys" ("Catagory_ID","Catagory_Name","Colour") VALUES (4,'Clothes','Light Yellow')''')
        self.c.execute('''INSERT INTO "PromotionCatagorys" ("Catagory_ID","Catagory_Name","Colour") VALUES (5,'Electronics','Orange')''')
        self.c.execute('''INSERT INTO "PromotionCatagorys" ("Catagory_ID","Catagory_Name","Colour") VALUES (6,'Other','Pink')''')
        # Hash the password 'Admin'
        password_hash = hashlib.sha256('Admin'.encode()).hexdigest()
        # Insert users into the Users table
        self.c.execute(f'''INSERT INTO "Users" ("First_Name","Surname","Email","Account_Type","Date_Created","Recovery_Hash") VALUES (?,?,?,?,?,?)''',('Admin','Admin','','1','01/01/2020',''))
        self.c.execute(f'''INSERT INTO "Users" ("First_Name","Surname","Email","Account_Type","Date_Created","Recovery_Hash") VALUES (?,?,?,?,?,?)''',('Users','Users','defutl@defult.co.uk','2','01/01/2020','test'))
        self.c.execute(f'''INSERT INTO "LoginDetails" ("Username","Password","User_ID","Login_Attempts","Recovery_Attempts","Active") VALUES ('Admin','{password_hash}','1','0','0','True')''')
        password_hash = hashlib.sha256('User'.encode()).hexdigest()
        self.c.execute(f'''INSERT INTO "LoginDetails" ("Username","Password","User_ID","Login_Attempts","Recovery_Attempts","Active") VALUES ('User','{password_hash}','2','0','0','True')''')
        self.conn.commit()
    
    def banner_maker(self):
        # Light Banner creation
        create_banner = Image.new('RGB', (600, 200), color = 'white')
        create_banner.save('Images/create_banner.png')
        text = "D . E . L . I . B . I . R . D . S"
        img = Image.open("Images/create_banner.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40,)
        draw.text((70, 80),text,fill='Black',font=font)
        draw.text((70, 40),text,fill='Grey',font=font)
        draw.text((70, 120),text,fill='Grey',font=font)
        img.save('Images/create_banner_light.png')

        # Dark Banner creation
        create_banner = Image.new('RGB', (600, 200), color = 'black')
        create_banner.save('Images/create_banner.png')
        text = "D . E . L . I . B . I . R . D . S"
        img = Image.open("Images/create_banner.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40,)
        draw.text((70, 80),text,fill='White',font=font)
        draw.text((70, 40),text,fill='Grey',font=font)
        draw.text((70, 120),text,fill='Grey',font=font)
        img.save('Images/create_banner_dark.png')

    def folder_creator(self):
        try:
            # Attempt to create necessary directories
            os.mkdir('Database')
            os.mkdir('Images')
            os.mkdir('Images/Logos')
            os.mkdir('Images/QR')
        except:
            # If there's an error (like the directories already exist), show an error message
            messagebox.showerror('Error','Error creating folders, please check permissions and remove any existing folders named "Database" or "Images"')

    def logos(self):
        try:
            # Attempt to download a zip file of logos from Dropbox, Onedrive refused to work for no good reason
            download_link = 'https://www.dropbox.com/scl/fo/biohst1vp732n8scaqzg7/h?rlkey=3214ae1qzf3rwsl3b7gk5aeau&dl=1'
            files = requests.get(download_link)
            open('Images.zip', 'wb').write(files.content)
            with zipfile.ZipFile('Images.zip', 'r') as zip_ref:
                zip_ref.extractall('Images/Logos')
            # Remove the zip file after extraction
            os.remove('Images.zip')   
        except:
            # If there's an error (like the download link is broken), show an error message and use a default logo
            messagebox.showerror('Error','Error downloading logos, proceeding with default logo for all promotions.')
            # Create a default logo
            logo = Image.new('RGB', (200, 200), color='white')
            draw = ImageDraw.Draw(logo)
            draw.ellipse((50, 50, 150, 150), fill='Green')
            font = ImageFont.truetype('arial.ttf', 40)
            text = 'Defult Logo'
            draw.text((200, 200), text, fill='black', font=font)
            logo.save('Images/Logos/logo.png')
            # Set use_default to True to indicate that the default logo should be used
            self.use_default = True 

if __name__ == "__main__":
    # If this script is run directly (not imported), create an Install object and call its create_db method
    install = Install()
    install.create_db()