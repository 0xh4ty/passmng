import sqlite3

def view_data():
    # Function to view all the data stored in the database
    # Connect to the database
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    
    # Retrieve all the data from the table
    c.execute("SELECT * FROM passwords")
    data = c.fetchall()
    
    # Print the data (you can modify this to display it in a different format)
    for row in data:
        print("Website:", row[0])
        print("Username:", row[1])
        print("Password:", row[2])
        print()
    
    # Close the connection
    conn.close()