
import tkinter as tk
import sqlite3
import pyperclip

# File to store clipboard history
clipboard_history_db = "clipboard_history.db"

# Function to display clipboard history in GUI
def display_clipboard_history():
    # Clear existing clipboard history
    for widget in entries_frame.winfo_children():
        widget.destroy()
    try:
        conn = sqlite3.connect(clipboard_history_db)
        c = conn.cursor()
        c.execute("SELECT * FROM clipboard_history ORDER BY timestamp DESC LIMIT 25")
        history = c.fetchall()
        conn.close()
        for entry in history:
            add_clipboard_entry(entry[0], entry[1])  # Entry[0] is timestamp, entry[1] is content
    except sqlite3.Error as e:
        print("SQLite error:", e)

# Function to add a clipboard entry to the GUI
def add_clipboard_entry(timestamp, content):
    # Create a frame to contain the clipboard entry
    entry_frame = tk.Frame(entries_frame, bg="gray", bd=2, relief=tk.RAISED, borderwidth=2)
    entry_frame.pack(fill=tk.X, padx=5, pady=5)

    # Create timestamp label
    timestamp_label = tk.Label(entry_frame, text=timestamp, bg="gray", fg="white", anchor="e")
    timestamp_label.pack(side=tk.TOP, fill=tk.X)

    # Create a Text widget for displaying the content
    content_text = tk.Text(entry_frame, bg="gray", wrap=tk.WORD, height=2, width=50, bd=0)
    content_text.insert(tk.END, content)
    content_text.pack(fill=tk.BOTH, padx=11, pady=(0, 5))
    content_text.config(state=tk.DISABLED)

# Function to clear clipboard history
def clear_clipboard_history():
    conn = sqlite3.connect(clipboard_history_db)
    c = conn.cursor()
    c.execute("DELETE FROM clipboard_history")
    conn.commit()
    conn.close()
    display_clipboard_history()

# Function to monitor clipboard changes and update history
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
    conn = sqlite3.connect(clipboard_history_db)
    c = conn.cursor()
    c.execute("INSERT INTO clipboard_history (timestamp, content) VALUES (datetime('now'), ?)", (content,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Clipboard History")

    # Create a frame for the button
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Add a "Clear All" button to the button frame
    clear_button = tk.Button(button_frame, text="Clear All", command=clear_clipboard_history)
    clear_button.pack(side=tk.RIGHT)

    # Create a canvas to contain the clipboard entries
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame to contain the clipboard entries inside the canvas
    entries_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=entries_frame, anchor=tk.NW)

    # Function to update the scroll region of the canvas
    def update_scroll_region(event):
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    # Bind the update_scroll_region function to the <Configure> event of the entries frame
    entries_frame.bind("<Configure>", update_scroll_region)

    # Initialize clipboard history database
    conn = sqlite3.connect(clipboard_history_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clipboard_history
                 (timestamp TEXT, content TEXT)''')
    conn.commit()
    conn.close()

    # Monitor clipboard changes and update clipboard history
    monitor_clipboard_changes()

    # Display initial clipboard history
    display_clipboard_history()

    root.mainloop()
