import tkinter as tk
import sqlite3
import secrets
import string
import os
from cryptography.fernet import Fernet
from viewall import view_data

def login():
    # Function to handle login button click event
    entered_password = master_password_entry.get()

    if entered_password == master_password:
        # Correct master password entered, enable password manager features
        enable_password_manager()
    else:
        # Incorrect master password entered, show error message
        login_error_label.config(text="Incorrect password")

def enable_password_manager():
    # Enable the password manager features by setting state to NORMAL for relevant widgets
    website_entry.config(state=tk.NORMAL)
    username_entry.config(state=tk.NORMAL)
    password_entry.config(state=tk.NORMAL)
    confirm_password_entry.config(state=tk.NORMAL)
    result_entry.config(state=tk.NORMAL)
    submit_button.config(state=tk.NORMAL)
    get_button.config(state=tk.NORMAL)
    generate_button.config(state=tk.NORMAL)
    login_frame.pack_forget()

def create_table():
    # Function to create the table if it doesn't exist
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            website TEXT,
            username TEXT,
            encrypted_password TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def onsubmit():
    # Function to handle button click events
    # Access the input field values and perform necessary actions
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if any of the fields are empty
    if not website or not username or not password or not confirm_password:
        return

    if password == confirm_password:

        # Encrypt the password
        encrypted_password = crypt_key.encrypt(password.encode())
    
        # Connect to the database
        conn = sqlite3.connect("passwords.db")
        c = conn.cursor()
        
        # Insert the values into the table
        c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (website, username, encrypted_password))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)


    elif password != confirm_password:
        confirm_password_entry.delete(0, tk.END)

        confirm_password_entry.insert(0, "*")


def onget():
    # Function to handle button click events
    # Access the input field values and perform necessary actions
    website = website_entry.get()
    username = username_entry.get()
    
    # Connect to the database
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    
    # Retrieve the password from the database based on the website and username
    c.execute("SELECT encrypted_password FROM passwords WHERE website = ? AND username = ?", (website, username))
    result = c.fetchone()
    
    # Check if a password is found
    if result is not None:
        # Retrieve the password from the query result
        encrypted_password = result[0]
        password = crypt_key.decrypt(encrypted_password).decode()
        # Set the retrieved password in the password entry field
        #password_entry.configure(show="")
        result_entry.delete(0, tk.END)  # Clear the existing text
        result_entry.insert(0, password)
    else:
        # No matching password found
        password_entry.configure(show="")
        password_entry.delete(0, tk.END)  # Clear the existing text
        password_entry.insert(0, "Password not found")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def ongenerate():
    # Function to handle button click events
    # Generate a strong password and set it in the password entry field
    website = website_entry.get()
    username = username_entry.get()

    if not website or not username:
        result_entry.delete(0, tk.END)
    else:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(16))
        result_entry.configure(show="")
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)


key_file_path = "key.txt"

# Check if the key file exists
if not os.path.exists(key_file_path):
    # Generate a new key
    key = Fernet.generate_key()
    
    # Save the key to a new file
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
else:
    # Read the key from the existing file
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()

# Create the Fernet instance
crypt_key = Fernet(key)

# Create the main window
window = tk.Tk()
window.title("Password Manager")

# Create login frame
login_frame = tk.Frame(window)

# Create labels for login frame
master_password_label = tk.Label(login_frame, text="Master Pass:")
master_password_label.grid(row=0, column=0)

# Create entry field for login frame
master_password_entry = tk.Entry(login_frame, show="*")
master_password_entry.grid(row=0, column=1)

# Create login button for login frame
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=0, column=2)

login_error_label = tk.Label(login_frame, text="")
login_error_label.grid(row=1, column=1)

login_frame.pack()

# Create password manager frame
password_manager_frame = tk.Frame(window)
password_manager_frame.pack(pady=10)

# Create labels and entries for password manager frame
website_label = tk.Label(password_manager_frame, text="Website:")
website_label.grid(row=0, column=0)

username_label = tk.Label(password_manager_frame, text="Username:")
username_label.grid(row=1, column=0)

password_label = tk.Label(password_manager_frame, text="Password:")
password_label.grid(row=2, column=0)

confirm_password_label = tk.Label(password_manager_frame, text="Confirm Password:")
confirm_password_label.grid(row=3, column=0)

website_entry = tk.Entry(password_manager_frame, state=tk.DISABLED)
website_entry.grid(row=0, column=1)

username_entry = tk.Entry(password_manager_frame, state=tk.DISABLED)
username_entry.grid(row=1, column=1)

password_entry = tk.Entry(password_manager_frame, show="*", state=tk.DISABLED)
password_entry.grid(row=2, column=1)

confirm_password_entry = tk.Entry(password_manager_frame, show="*", state=tk.DISABLED)
confirm_password_entry.grid(row=3, column=1)

result_entry = tk.Entry(password_manager_frame, show="", state=tk.DISABLED)
result_entry.grid(row=5, column=1)

# Create buttons for password manager frame
submit_button = tk.Button(password_manager_frame, text="Submit", command=onsubmit, state=tk.DISABLED)
submit_button.grid(row=4, column=0)

get_button = tk.Button(password_manager_frame, text="Get", command=onget, state=tk.DISABLED)
get_button.grid(row=4, column=1)

generate_button = tk.Button(password_manager_frame, text="Generate", command=ongenerate, state=tk.DISABLED)
generate_button.grid(row=4, column=2)

master_password = "Passw0rd!"

create_table()

view_data()

window.mainloop()
