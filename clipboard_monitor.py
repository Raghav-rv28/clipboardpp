import pyperclip
import sqlite3
import os
from datetime import datetime
import time

# File to store clipboard history
clipboard_history_db = "clipboard_history.db"

# Function to initialize clipboard history database
def initialize_clipboard_history_db():
    if not os.path.exists(clipboard_history_db):
        conn = sqlite3.connect(clipboard_history_db)
        c = conn.cursor()
        c.execute('''CREATE TABLE clipboard_history
                     (timestamp TEXT, content TEXT)''')
        conn.commit()
        conn.close()

# Function to monitor clipboard changes
def monitor_clipboard_changes():
    previous_clipboard_content = pyperclip.paste()
    
    while True:
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != previous_clipboard_content:
            save_to_clipboard_history(current_clipboard_content)
            previous_clipboard_content = current_clipboard_content
        time.sleep(1)  # Check clipboard every second

# Function to save clipboard history
def save_to_clipboard_history(content):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(clipboard_history_db)
    c = conn.cursor()
    c.execute("INSERT INTO clipboard_history (timestamp, content) VALUES (?, ?)", (timestamp, content))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_clipboard_history_db()
    monitor_clipboard_changes()
