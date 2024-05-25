import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Set up the SQLite database
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    # Create default admin user
    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin')
    ''')
    conn.commit()
    conn.close()

# Function to handle user sign-up
def signup():
    def submit_signup():
        username = signup_username_entry.get()
        password = signup_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User signed up successfully!")
            main_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    clear_frame()
    tk.Label(app, text="Sign Up", font=("Arial", 14)).pack(pady=10)
    tk.Label(app, text="Username").pack()
    signup_username_entry = tk.Entry(app, bg="black", bd=2, fg="white")
    signup_username_entry.pack(pady=5)
    tk.Label(app, text="Password").pack()
    signup_password_entry = tk.Entry(app, show="*", bg="black", bd=2, fg="white")
    signup_password_entry.pack(pady=5)
    tk.Button(app, text="Sign Up", command=submit_signup).pack(pady=20)
    tk.Button(app, text="Back to Main Page", command=main_page).pack(pady=5)

# Function to handle user login
def login():
    def submit_login():
        username = login_username_entry.get()
        password = login_password_entry.get()
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()
        
        if result:
            if username == "admin":
                admin_panel()
            else:
                messagebox.showinfo("Success", "Login successful!")
                main_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")
        
        conn.close()

    clear_frame()
    tk.Label(app, text="Login", font=("Arial", 14)).pack(pady=10)
    tk.Label(app, text="Username").pack()
    login_username_entry = tk.Entry(app, bg="black", bd=2, fg="white")
    login_username_entry.pack(pady=5)
    tk.Label(app, text="Password").pack()
    login_password_entry = tk.Entry(app, show="*", bg="black", bd=2, fg="white")
    login_password_entry.pack(pady=5)
    tk.Button(app, text="Login", command=submit_login).pack(pady=20)
    tk.Button(app, text="Back to Main Page", command=main_page).pack(pady=5)

# Function to clear the frame
def clear_frame():
    for widget in app.winfo_children():
        widget.destroy()

# Function to show the main page
def main_page():
    clear_frame()
    tk.Label(app, text="Main Page", font=("Arial", 14)).pack(pady=20)
    tk.Button(app, text="Sign Up", command=signup).pack(pady=10)
    tk.Button(app, text="Login", command=login).pack(pady=10)

# Function to handle the admin panel
def admin_panel():
    def view_users():
        clear_frame()
        tk.Label(app, text="Admin Panel - View Users", font=("Arial", 14)).pack(pady=10)
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username FROM users WHERE username != "admin"')
        users = cursor.fetchall()
        conn.close()

        for user in users:
            user_frame = tk.Frame(app)
            user_frame.pack(pady=5)
            tk.Label(user_frame, text=user[1]).pack(side=tk.LEFT)
            tk.Button(user_frame, text="Edit", command=lambda u=user: edit_user(u[0])).pack(side=tk.LEFT, padx=5)
            tk.Button(user_frame, text="Delete", command=lambda u=user: delete_user(u[0])).pack(side=tk.LEFT, padx=5)

        tk.Button(app, text="Back to Admin Panel", command=admin_panel).pack(pady=20)

    def edit_user(user_id):
        new_password = simpledialog.askstring("Edit User", "Enter new password")
        if new_password:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password updated successfully")
            view_users()

    def delete_user(user_id):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User deleted successfully")
        view_users()

    clear_frame()
    tk.Label(app, text="Admin Panel", font=("Arial", 20)).pack(pady=20)
    tk.Button(app, text="View Users", command=view_users).pack(pady=10)
    tk.Button(app, text="Back to Main Page", command=main_page).pack(pady=10)

# Main application window
app = tk.Tk()
app.title("Login & Registration App")
app.geometry("300x400")


setup_database()
main_page()

# Run the application
app.mainloop()
