import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import threading

def get_wifi_passwords():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # Get the profiles data using subprocess.PIPE for compatibility
        profiles_data = subprocess.Popen(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo).communicate()[0].decode('utf-8')
        # Extracting the profile names
        profiles = re.findall("All User Profile     : (.*)\r", profiles_data)

        if not profiles:
            log_text.insert(tk.END, "No Wi-Fi profiles found. Please run this as an administrator.\n")
            return

        for profile in profiles:
            profile_info = subprocess.Popen(["netsh", "wlan", "show", "profile", profile, "key=clear"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo).communicate()[0].decode('utf-8')
            password_match = re.search("Key Content            : (.*)\r", profile_info)
            password = password_match[1] if password_match else "Password not set"
            log_text.insert(tk.END, f"Profile: {profile}\nPassword: {password}\n")
            log_text.see(tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        progress_bar.stop()

def start_retrieval():
    progress_bar.start(10)
    threading.Thread(target=get_wifi_passwords).start()

def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(log_text.get("1.0", tk.END))
    messagebox.showinfo("Copied", "Passwords have been copied to clipboard!")

# Create main window
window = tk.Tk()
window.title("Wi-Fi Password Viewer")
window.geometry("600x350")

# Multiline text widget for logs
log_text = tk.Text(window, width=70, height=15)
log_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
scrollbar = tk.Scrollbar(window, command=log_text.yview)
scrollbar.grid(row=0, column=3, sticky='nsew')
log_text.config(yscrollcommand=scrollbar.set)

# Progress bar
progress_bar = ttk.Progressbar(window, length=580, mode='indeterminate')
progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

# Control buttons
start_button = tk.Button(window, text="Start", command=start_retrieval)
start_button.grid(row=2, column=0, padx=10, pady=10)

copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=2, column=1, padx=10, pady=10)

close_button = tk.Button(window, text="Close", command=window.destroy)
close_button.grid(row=2, column=2, padx=10, pady=10)

window.mainloop()
