import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import date


class LibraryManagementSystem:
    def __init__(self):
        print("Initializing Library Management System")  
        # Database details for connection
        self.conn = mysql.connector.connect(  
            # Replace these with your own MySQL database's details
            host="localhost",
            user="root",
            password="1234",
            database="library_management"
        )
        self.cursor = self.conn.cursor(dictionary=True)
        
        # Main application window
        self.root = tk.Tk()
        self.root.title("Library Management System - Home")
        self.root.geometry("400x300")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Current logged-in user/admin details
        self.current_user = None
        self.is_admin = False
        
        # Call to create main menu
        self.create_main_menu()

        # Start the Tkinter event loop
        self.root.mainloop()  # Ensuring this is called to run the Tkinter app

    def on_closing(self):
        """Handle application closure, ensuring database connection is closed."""
        if messagebox.askokcancel("Quit", "You are about to close the Lib_Man_App, do you want to proceed?"):
            self.cursor.close()
            self.conn.close()
            self.root.destroy()


    def create_main_menu(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main menu labels and buttons
        tk.Label(self.root, text="Library Management System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Sign Up", command=self.open_signup_window).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.open_login_window).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.on_closing).pack(pady=10)

    def open_signup_window(self):
        #Debug statement
        print("Signup window opened")
        self.root.withdraw()  # Hide the main window
        signup_window = tk.Toplevel(self.root)  # Create a new window
        signup_window.title("Sign Up")
        signup_window.geometry("400x300")
        tk.Label(signup_window, text="Sign Up", font=("Arial", 16)).pack(pady=20)

        tk.Label(signup_window, text="Name:").pack()
        name_entry = tk.Entry(signup_window, width=30)
        name_entry.pack(pady=5)

        tk.Label(signup_window, text="Email:").pack()
        email_entry = tk.Entry(signup_window, width=30)
        email_entry.pack(pady=5)

        tk.Label(signup_window, text="Password:").pack()
        password_entry = tk.Entry(signup_window, show="*", width=30)
        password_entry.pack(pady=5)

        def signup():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            if not name or not email or not password:
                messagebox.showerror("Error", "All fields are required!")
                return
            self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already exists.")
                return
            try:
                self.cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
                self.conn.commit()
                messagebox.showinfo("Success", "Sign up successful!")
                signup_window.destroy()
                self.root.deiconify()  # Show the main window again
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(signup_window, text="Sign Up", command=signup).pack(pady=10)
        tk.Button(signup_window, text="Back to Main Menu", command=lambda: [signup_window.destroy(), self.root.deiconify()]).pack(pady=5)

    def open_login_window(self):
        print("Login window opened")  # Debug statement
        self.root.withdraw()  # Hide the main window
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("400x250")

        # Form Elements
        tk.Label(login_window, text="Login", font=("Arial", 16)).pack(pady=20)
        tk.Label(login_window, text="Email:").pack()
        email_entry = tk.Entry(login_window, width=30)
        email_entry.pack(pady=5)

        tk.Label(login_window, text="Password:").pack()
        password_entry = tk.Entry(login_window, show="*", width=30)
        password_entry.pack(pady=5)

        # Login logic
        def login():
            email = email_entry.get().strip()
            password = password_entry.get().strip()

            if not email or not password:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                # Check if login is as Admin
                self.cursor.execute("SELECT * FROM admins WHERE email = %s AND password = %s", (email, password))
                admin = self.cursor.fetchone()
                if admin:
                    self.current_user = admin
                    self.is_admin = True
                    login_window.destroy()
                    self.open_admin_menu()
                    return

                # Check if login is as User
                self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                user = self.cursor.fetchone()
                if user:
                    self.current_user = user
                    self.is_admin = False
                    login_window.destroy()
                    self.open_user_menu()
                    return

                # If neither Admin nor User
                messagebox.showerror("Login Failed", "Invalid email or password.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        # Buttons
        tk.Button(login_window, text="Login", command=login).pack(pady=10)
        tk.Button(login_window, text="Back to Main Menu", command=lambda: [login_window.destroy(), self.root.deiconify()]).pack(pady=5)


    def open_admin_menu(self):
        print("Admin Menu opened")
        admin_window = tk.Toplevel(self.root)
        admin_window.title(f"Admin Menu - {self.current_user['name']}")
        admin_window.geometry("500x500")
        tk.Label(admin_window, text=f"Welcome, {self.current_user['name']}!", font=("Arial", 16)).pack(pady=20)
        menu_options = [
            ("View Available Books", self.open_view_books_window),
            ("View User List", self.view_user_list),
            ("Add Book", self.open_add_book_window),
            ("Remove Book", self.open_remove_book_window),
            ("Issue Book", self.open_issue_book_window),
            ("Return Book", self.open_return_book_window),
            ("Create Admin Account", self.open_create_admin_window),
            ("Remove Admin Account", self.open_remove_admin_window),
            ("Logout", self.logout)
        ]
        for text, command in menu_options:
            tk.Button(admin_window, text=text, command=command, width=30).pack(pady=5)

    def open_user_menu(self):
        user_window = tk.Toplevel(self.root)
        user_window.title(f"User Menu - {self.current_user['name']}")
        user_window.geometry("500x400")
        tk.Label(user_window, text=f"Welcome, {self.current_user['name']}!", font=("Arial", 16)).pack(pady=20)
        menu_options = [
            ("View Available Books", self.open_view_books_window),
            ("Borrow Book", self.open_issue_book_window),
            ("Return Book", self.open_return_book_window),
            ("Logout", self.logout)
        ]
        for text, command in menu_options:
            tk.Button(user_window, text=text, command=command, width=30).pack(pady=5)


    def open_create_admin_window(self):
        create_admin_window = tk.Toplevel(self.root)
        create_admin_window.title("Create Admin Account")
        create_admin_window.geometry("400x300")
        tk.Label(create_admin_window, text="Create Admin Account", font=("Arial", 16)).pack(pady=20)

        tk.Label(create_admin_window, text="Name:").pack()
        name_entry = tk.Entry(create_admin_window, width=30)
        name_entry.pack(pady=5)

        tk.Label(create_admin_window, text="Email:").pack()
        email_entry = tk.Entry(create_admin_window, width=30)
        email_entry.pack(pady=5)

        tk.Label(create_admin_window, text="Password:").pack()
        password_entry = tk.Entry(create_admin_window, show="*", width=30)
        password_entry.pack(pady=5)

        def create_admin():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            if not name or not email or not password:
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                # Check if the admin already exists in the database
                self.cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
                if self.cursor.fetchone():
                    messagebox.showerror("Error", "Admin with this email already exists.")
                    return
                
                # Insert the new admin into the database
                self.cursor.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", 
                                    (name, email, password))
                self.conn.commit()
                messagebox.showinfo("Success", "Admin account created successfully!")
                create_admin_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(create_admin_window, text="Create Admin", command=create_admin).pack(pady=10)
        tk.Button(create_admin_window, text="Back to Admin Menu", command=create_admin_window.destroy).pack(pady=5)

    def open_remove_admin_window(self):
        remove_admin_window = tk.Toplevel(self.root)
        remove_admin_window.title("Remove Admin Account")
        remove_admin_window.geometry("400x300")
        tk.Label(remove_admin_window, text="Remove Admin Account", font=("Arial", 16)).pack(pady=20)

        tk.Label(remove_admin_window, text="Enter Admin Email to Remove:").pack()
        email_entry = tk.Entry(remove_admin_window, width=30)
        email_entry.pack(pady=5)

        def remove_admin():
            email = email_entry.get()
            if not email:
                messagebox.showerror("Error", "Email is required!")
                return
            try:
                # Check if the admin exists in the database
                self.cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
                admin = self.cursor.fetchone()
                if not admin:
                    messagebox.showerror("Error", "No admin found with this email.")
                    return

                # Remove the admin from the database
                self.cursor.execute("DELETE FROM admins WHERE email = %s", (email,))
                self.conn.commit()
                messagebox.showinfo("Success", "Admin account removed successfully!")
                remove_admin_window.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(remove_admin_window, text="Remove Admin", command=remove_admin).pack(pady=10)
        tk.Button(remove_admin_window, text="Back to Admin Menu", command=remove_admin_window.destroy).pack(pady=5)

    def open_view_books_window(self):
        view_books_window = tk.Toplevel(self.root)
        view_books_window.title("View Available Books")
        view_books_window.geometry("500x400")
        tk.Label(view_books_window, text="Available Books", font=("Arial", 16)).pack(pady=20)

        try:
            self.cursor.execute("SELECT book_id, title, author FROM books WHERE available = 1")
            books = self.cursor.fetchall()

            if not books:
                tk.Label(view_books_window, text="No available books found.").pack(pady=20)
            else:
                for row in books:
                    tk.Label(view_books_window, text=f"Book ID: {row['book_id']} - Title: {row['title']} - Author: {row['author']}").pack(pady=5)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

        tk.Button(view_books_window, text="Back", command=view_books_window.destroy).pack(pady=30)

    def open_add_book_window(self):
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add New Book")
        add_book_window.geometry("400x300")
        tk.Label(add_book_window, text="Add New Book", font=("Arial", 16)).pack(pady=20)

        tk.Label(add_book_window, text="Title:").pack()
        title_entry = tk.Entry(add_book_window, width=30)
        title_entry.pack(pady=5)

        tk.Label(add_book_window, text="Author:").pack()
        author_entry = tk.Entry(add_book_window, width=30)
        author_entry.pack(pady=5)

        def add_book():
            title = title_entry.get()
            author = author_entry.get()
            if not title or not author:
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                self.cursor.execute("INSERT INTO books (title, author, available, added_by) VALUES (%s, %s, %s, %s)",(title, author, 1, self.current_user['name']))
                self.conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                add_book_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(add_book_window, text="Add Book", command=add_book).pack(pady=10)
        tk.Button(add_book_window, text="Back to Admin Menu", command=add_book_window.destroy).pack(pady=5)

    def open_remove_book_window(self):
        remove_book_window = tk.Toplevel(self.root)
        remove_book_window.title("Remove Book")
        remove_book_window.geometry("400x300")
        tk.Label(remove_book_window, text="Remove Book", font=("Arial", 16)).pack(pady=20)

        tk.Label(remove_book_window, text="Book ID:").pack()
        book_id_entry = tk.Entry(remove_book_window, width=30)
        book_id_entry.pack(pady=5)

        def remove_book():
            book_id = book_id_entry.get()
            if not book_id:
                messagebox.showerror("Error", "Book ID is required!")
                return
            try:
                # Check if the book exists
                self.cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
                book = self.cursor.fetchone()
                if not book:
                    messagebox.showerror("Error", "No book found with the provided Book ID.")
                    return

                # Delete the book
                self.cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Book removed successfully!")
                remove_book_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(remove_book_window, text="Remove Book", command=remove_book).pack(pady=10)
        tk.Button(remove_book_window, text="Back to Admin Menu", command=remove_book_window.destroy).pack(pady=5)

    def open_issue_book_window(self):
        issue_book_window = tk.Toplevel(self.root)
        issue_book_window.title("Issue Book")
        issue_book_window.geometry("400x350")
        tk.Label(issue_book_window, text="Issue Book", font=("Arial", 16)).pack(pady=20)

        # Book ID entry
        tk.Label(issue_book_window, text="Book ID:").pack()
        book_id_entry = tk.Entry(issue_book_window, width=30)
        book_id_entry.pack(pady=5)

        if self.is_admin:
            # User ID entry for admins
            tk.Label(issue_book_window, text="User ID:").pack()
            user_id_entry = tk.Entry(issue_book_window, width=30)
            user_id_entry.pack(pady=5)
        else:
            user_id_entry = None  # No user_id entry for regular users

        def issue_book():
            book_id = book_id_entry.get()
            user_id = user_id_entry.get() if self.is_admin else self.current_user["user_id"]  # Use logged-in user ID
            if not book_id or (self.is_admin and not user_id):
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                self.cursor.execute("SELECT * FROM books WHERE book_id = %s AND available = 1", (book_id,))
                book = self.cursor.fetchone()
                if not book:
                    messagebox.showerror("Error", "Book not available or doesn't exist.")
                    return

                self.cursor.execute("INSERT INTO transactions (user_id, book_id, issue_date, status) VALUES (%s, %s, %s, %s)",
                                    (user_id, book_id, date.today(), "borrowed"))
                self.cursor.execute("UPDATE books SET available = 0 WHERE book_id = %s", (book_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
                issue_book_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(issue_book_window, text="Issue Book", command=issue_book).pack(pady=10)
        tk.Button(issue_book_window, text="Back to Menu", command=issue_book_window.destroy).pack(pady=5)

    def open_return_book_window(self):
        return_book_window = tk.Toplevel(self.root)
        return_book_window.title("Return Book")
        return_book_window.geometry("400x350")
        tk.Label(return_book_window, text="Return Book", font=("Arial", 16)).pack(pady=20)

        # Book ID entry
        tk.Label(return_book_window, text="Book ID:").pack()
        book_id_entry = tk.Entry(return_book_window, width=30)
        book_id_entry.pack(pady=5)

        # User ID entry for admins
        user_id_entry = None
        if self.is_admin:
            tk.Label(return_book_window, text="User ID:").pack()
            user_id_entry = tk.Entry(return_book_window, width=30)
            user_id_entry.pack(pady=5)
        else:
            # No user_id entry for regular users, use current_user's user_id
            user_id_entry = None

        def return_book():
            book_id = book_id_entry.get()
            user_id = user_id_entry.get() if self.is_admin else self.current_user["user_id"]  # Use logged-in user ID
            if not book_id or (self.is_admin and not user_id):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                # If admin mode, the book return check is done for the entered user_id
                if self.is_admin:
                    self.cursor.execute("SELECT * FROM transactions WHERE book_id = %s AND user_id = %s AND status = 'borrowed'",
                                        (book_id, user_id))
                else:
                    self.cursor.execute("SELECT * FROM transactions WHERE book_id = %s AND user_id = %s AND status = 'borrowed'",
                                        (book_id, self.current_user["user_id"]))

                transaction = self.cursor.fetchone()

                if not transaction:
                    messagebox.showerror("Error", "This book hasn't been borrowed by the user.")
                    return

                # Update the book's availability and transaction status
                self.cursor.execute("UPDATE books SET available = 1 WHERE book_id = %s", (book_id,))
                self.cursor.execute("UPDATE transactions SET return_date = %s, status = 'returned' WHERE book_id = %s AND user_id = %s", 
                                    (date.today(), book_id, user_id))
                self.conn.commit()
                messagebox.showinfo("Success", "Book returned successfully!")
                return_book_window.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(return_book_window, text="Return Book", command=return_book).pack(pady=10)
        tk.Button(return_book_window, text="Back to Menu", command=return_book_window.destroy).pack(pady=5)

    def view_user_list(self):
        user_list_window = tk.Toplevel(self.root)
        user_list_window.title("View User List")
        user_list_window.geometry("600x400")
        tk.Label(user_list_window, text="User List and Borrowed Books", font=("Arial", 16)).pack(pady=20)

        try:
            # Query to fetch all users and their borrowed book details
            self.cursor.execute("""
                SELECT u.user_id, u.name, b.book_id, b.title, t.issue_date 
                FROM users u
                LEFT JOIN transactions t ON u.user_id = t.user_id AND t.status = 'borrowed'
                LEFT JOIN books b ON t.book_id = b.book_id
            """)
            user_data = self.cursor.fetchall()

            if not user_data:
                tk.Label(user_list_window, text="No data found.").pack(pady=20)
            else:
                for row in user_data:
                    # Format the display for users and borrowed books
                    user_info = f"User ID: {row['user_id']} - Name: {row['name']}"
                    book_info = (
                        f"Book ID: {row['book_id']} - Title: {row['title']} - Issue Date: {row['issue_date']}"
                        if row['book_id']
                        else "No books borrowed"
                    )
                    tk.Label(user_list_window, text=f"{user_info} | {book_info}").pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        except Exception as e:
            messagebox.showerror("Error", str(e))

        tk.Button(user_list_window, text="Back", command=user_list_window.destroy).pack(pady=30)



    def logout(self):
        self.current_user = None
        self.is_admin = False
        # Destroys all open windows
        self.create_main_menu()
        # Unhides main menu
        self.root.deiconify()


if __name__ == "__main__":
    LibraryManagementSystem()




# All rights reserved - Krrish K, Rishi C, and Tamanna B.