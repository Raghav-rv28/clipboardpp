import tkinter as tk
import pyperclip
import sqlite3
import os
from datetime import datetime

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
    
    def check_clipboard():
        nonlocal previous_clipboard_content
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != previous_clipboard_content:
            save_to_clipboard_history(current_clipboard_content)
            display_clipboard_history()
            previous_clipboard_content = current_clipboard_content
        root.after(1000, check_clipboard)  # Check clipboard every 1000 milliseconds

    check_clipboard()

# Function to save clipboard history
def save_to_clipboard_history(content):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(clipboard_history_db)
    c = conn.cursor()
    c.execute("INSERT INTO clipboard_history (timestamp, content) VALUES (?, ?)", (timestamp, content))
    conn.commit()
    conn.close()

# Function to display clipboard history in GUI
def display_clipboard_history():
    # Clear existing clipboard history
    for widget in listbox.winfo_children():
        widget.destroy()

    try:
        conn = sqlite3.connect(clipboard_history_db)
        c = conn.cursor()
        c.execute("SELECT * FROM clipboard_history ORDER BY timestamp DESC")
        history = c.fetchall()
        conn.close()
        for entry in history:
            add_clipboard_entry(entry[0], entry[1])  # Entry[0] is timestamp, entry[1] is content
    except sqlite3.Error as e:
        print("SQLite error:", e)

# Function to add a clipboard entry to the GUI
def add_clipboard_entry(timestamp, content):
    entry_frame = tk.Frame(listbox, bg="gray", bd=2, relief=tk.RAISED, borderwidth=2)
    entry_frame.pack(fill=tk.X, padx=5, pady=5)

    timestamp_label = tk.Label(entry_frame, text=timestamp, bg="gray", fg="white", anchor="e")
    timestamp_label.pack(side=tk.TOP, fill=tk.X)

    content_label = tk.Label(entry_frame, text=content, bg="gray", wraplength=500)
    content_label.pack(fill=tk.X, padx=11, pady=(0, 10))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Clipboard History")

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Frame(root)
    listbox.pack(expand=True, fill=tk.BOTH)

    initialize_clipboard_history_db()
    monitor_clipboard_changes()
    display_clipboard_history()

    root.mainloop()
