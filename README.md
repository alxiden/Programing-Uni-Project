# Programing-Uni-Project
My project done for my Level 4 Principles of Programming assignment at the Univercity of Gloucestershire

Project brief:

Scenario: Secure Marketing Application with Graphical User Interface using SQLite and QR Code

 

Overview: As a programmer, you have been tasked with developing a secure marketing application with a graphical user interface (GUI) using SQLite database and QR code. The system should allow users to view marketing promotions, scan QR codes to access additional information, and track their interactions with promotions.



Software Requirements:

1.     Graphical User Interface: You will need to develop a GUI for the marketing application using Python programming language. The GUI should be user-friendly and visually appealing, with at least the following features to include search bar, promotion categories, and a QR code scanner.

2.     User Authentication: The system should have a secure user authentication process, requiring users to provide their login credentials to access their personal information and view promotions. Passwords must be hashed and stored securely in the SQLite database.

3.     QR Code Generator and Scanner: The system should be able to generate and scan QR codes and retrieve additional information about promotions, such as product details or discounts. You will need to implement a QR code generator and scanner in the application. QR codes generated should be saved in the local directory of your developed software (application).

4.     SQLite Database: You will need to create a SQLite database to store promotion and user information. The database should have at least three tables: one for promotions, one for user registration, and another for storing user interactions with promotions. The database should be linked with developed GUI.

5.     SQL Injection Prevention: The system should be protected against SQL injection attacks. You must ensure that all user inputs are sanitized and validated before being passed to the SQLite database. For this application, any user’s age under 18 is considered as an attack and details should be rejected and not saved in the database.
