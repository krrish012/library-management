Library Management App


Overview:
This Library Management System is a user-friendly Python-based application with a MySQL backend, designed to streamline library operations. It empowers admins to manage books and users efficiently, including adding, issuing, returning, and viewing book records. Users can seamlessly borrow and return books, while the app ensures accurate transaction tracking and detailed user-book reports. The system employs robust data abstraction and integrity measures to eliminate redundancy and maintain a well-organized database structure. With features like admin authentication and dynamic reports, this application serves as a reliable tool for modern library management.


Features:

Admin Features:
•	Add new books to the library.
•	Remove books from the library.
•	Issue books to users and mark returns.
•	Create and manage admin accounts.
•	View detailed user-borrowing reports.
User Features:
•	Borrow books from the library.
•	Return books they have borrowed.
•	View available books with author details.
General Features:
•	Sign up as a new user.
•	Log in as an admin or user.
•	Generate reports for borrowed books and transaction history.
•	Clear all data while retaining the database structure for reuse.





Database Structure:

The database consists of the following tables:
1.	admins
Stores admin information.
o	admin_id (INT, PRIMARY KEY, AUTO_INCREMENT)
o	name (VARCHAR(100))
o	email (VARCHAR(100), UNIQUE)
o	password (VARCHAR(255))
2.	users
Stores regular user information.
o	user_id (INT, PRIMARY KEY, AUTO_INCREMENT)
o	name (VARCHAR(100))
o	email (VARCHAR(100), UNIQUE)
o	password (VARCHAR(255))
3.	books
Stores the details of the books in the library.
o	book_id (INT, PRIMARY KEY, AUTO_INCREMENT)
o	title (VARCHAR(255))
o	author (VARCHAR(100))
o	available (TINYINT(1), DEFAULT 1)
o	added_by (VARCHAR(20)) - Name of the admin who added the book.
4.	transactions
Stores the borrowing and returning transactions.
o	transaction_id (INT, PRIMARY KEY, AUTO_INCREMENT)
o	user_id (INT, FOREIGN KEY to users.user_id)
o	book_id (INT, FOREIGN KEY to books.book_id)
o	issue_date (DATE)
o	return_date (DATE, NULLABLE)
o	status (ENUM: 'borrowed', 'returned', DEFAULT 'borrowed')


Usage:
1.	Sign Up:
New users can sign up by providing their name, email, and password.
2.	Login:
Both admins and users can log in using their email and password. Once logged in, they are redirected to a menu tailored to their role.
3.	Admin Menu:
o	Add Book: Admins can add new books to the library, specifying details such as title, author, and availability.
o	Issue Book: Admins can issue books to users, recording borrowing transactions.
o	Return Book: Admins can process the return of books that have been borrowed.
o	Remove Book: Admins can delete books from the library database.
o	View User List: Admins can view a detailed report of users and their borrowed books.
o	Create Admin Account: Admins can create new admin accounts for managing the system.
4.	User Menu:
o	Borrow Book: Users can borrow available books from the library.
o	Return Book: Users can return the books they have borrowed.
o	View Available Books: Users can browse through the list of books that are currently available for borrowing.
5.	Exit:
Users and admins can choose to log out or exit the application when their tasks are completed.


How to use:

1.	Prerequisites:
Ensure the following are installed on your system:
o	MySQL Command Line Client
o	IDLE or any other Python development environment (download from python.org)
o	MySQL Connector for Python by running the command in the terminal (as admin): 
o	pip install mysql-connector-python
2.	Set Up MySQL:
o	Start the MySQL command line client and create a new database.
o	Create the 4 tables (admins, users, books, and transactions) using the structure provided in the "Database Structure" section.
o	Note down the connection data of the database (username, password, database name).
3.	Set Up Python:
o	Copy the provided Python application code into your Python file.
o	Insert the database connection details (username, password, database name) into the code where prompted.
4.	Run the App:
o	After everything is set up, simply run the Python file, and the application will start. Follow the prompts on the screen to use the Library Management System!


License:

This project is licensed under the MIT License.


Contributing:

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.


Contact:

If you have any questions or issues with the system, feel free to reach out to our developers at: 
- Email: katirakrrish@gmail.com, tamannabhunia14@gmail.com, rishichoraria1@gmail.com





Project by:
Krrish K., Rishi C. and Tamanna B