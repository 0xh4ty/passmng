import tkinter as tk
import sqlite3
from viewall import view_data

def create_table():
    # Function to create the table if it doesn't exist
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            website TEXT,
            username TEXT,
            password TEXT
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
    
        # Connect to the database
        conn = sqlite3.connect("passwords.db")
        c = conn.cursor()
        
        # Insert the values into the table
        c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (website, username, password))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)

        #I tried this but it prints a space over the X
        """
        wrong_password_label = tk.Label(window, text="")
        wrong_password_label.grid(row=2, column=2)
        
        wrong_confirm_password_label = tk.Label(window, text="")
        wrong_confirm_password_label.grid(row=3, column=2)
        """

        wrong_password_label.grid_forget()
        wrong_confirm_password_label.grid_forget()


    elif password != confirm_password:
        confirm_password_entry.delete(0, tk.END)

        wrong_password_label = tk.Label(window, text="X")
        wrong_password_label.grid(row=2, column=2)
        
        wrong_confirm_password_label = tk.Label(window, text="X")
        wrong_confirm_password_label.grid(row=3, column=2)

def onget():
    # Function to handle button click events
    # Access the input field values and perform necessary actions
    website = website_entry.get()
    username = username_entry.get()
    
    # Connect to the database
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    
    # Retrieve the password from the database based on the website and username
    c.execute("SELECT password FROM passwords WHERE website = ? AND username = ?", (website, username))
    result = c.fetchone()
    
    # Check if a password is found
    if result is not None:
        # Retrieve the password from the query result
        password = result[0]
        # Set the retrieved password in the password entry field
        password_entry.configure(show="")
        password_entry.delete(0, tk.END)  # Clear the existing text
        password_entry.insert(0, password)
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
    # Access the input field values and perform necessary actions
    website = website_entry.get()
    username = username_entry.get()
    
    print("Generated password")

# Create the main window
window = tk.Tk()
window.title("Password Manager")

# Create labels
website_label = tk.Label(window, text="Website:")
website_label.grid(row=0, column=0)

username_label = tk.Label(window, text="Username:")
username_label.grid(row=1, column=0)

password_label = tk.Label(window, text="Password:")
password_label.grid(row=2, column=0)

confirm_password_label = tk.Label(window, text="Confirm Password:")
confirm_password_label.grid(row=3, column=0)

# Create entry fields
website_entry = tk.Entry(window)
website_entry.grid(row=0, column=1)

username_entry = tk.Entry(window)
username_entry.grid(row=1, column=1)

password_entry = tk.Entry(window, show="*")  # Use show="*" to hide the password input
password_entry.grid(row=2, column=1)

confirm_password_entry = tk.Entry(window, show="*")
confirm_password_entry.grid(row=3, column=1)

# Create buttons
submit_button = tk.Button(window, text="Submit", command=onsubmit)
submit_button.grid(row=4, column=0)

get_button = tk.Button(window, text="Get", command=onget)
get_button.grid(row=4, column=1)

generate_button = tk.Button(window, text="Generate", command=ongenerate)
generate_button.grid(row=4, column=2)

create_table()

view_data()

# Start the main GUI event loop
window.mainloop()
