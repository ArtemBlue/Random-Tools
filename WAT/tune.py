import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, message):
        self.widget.insert(tk.END, message, (self.tag,))
        self.widget.yview(tk.END)

    def flush(self):
        pass

class WifiConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Adapter Tuner")
        
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.create_widgets()
        
        sys.stdout = TextRedirector(self.log_text, "stdout")
        sys.stderr = TextRedirector(self.log_text, "stderr")
    
    def create_widgets(self):
        self.nic_label = tk.Label(self.left_frame, text="Select Wi-Fi Adapter:")
        self.nic_label.pack(pady=5)
        
        self.nic_listbox = tk.Listbox(self.left_frame)
        self.nic_listbox.pack(pady=5)
        
        self.refresh_button = tk.Button(self.left_frame, text="Refresh Adapters", command=self.refresh_adapters)
        self.refresh_button.pack(pady=5)
        
        self.config_button = tk.Button(self.left_frame, text="Configure Adapter", command=self.configure_adapter)
        self.config_button.pack(pady=5)

        self.copy_button = tk.Button(self.left_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)
        
        self.log_text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, width=50, height=20)
        self.log_text.pack(padx=10, pady=10)
        
        self.load_adapters()
    
    def refresh_adapters(self):
        self.clear_log()
        self.load_adapters()

    def load_adapters(self):
        self.nic_listbox.delete(0, tk.END)
        try:
            self.log("Loading adapters...")
            command = "Get-NetAdapter | Where-Object {$_.InterfaceType -eq 71} | Select-Object -ExpandProperty Name"
            adapters = self.run_command(command)
            if adapters:
                for adapter in adapters.splitlines():
                    self.nic_listbox.insert(tk.END, adapter)
                self.log("Adapters loaded successfully.")
            else:
                self.log("No adapters found.")
        except Exception as e:
            self.log(f"Failed to load adapters: {e}")
    
    def configure_adapter(self):
        self.clear_log()
        selected_adapter = self.nic_listbox.get(tk.ACTIVE)
        if not selected_adapter:
            messagebox.showerror("Error", "Please select a Wi-Fi adapter.")
            self.log("Configuration failed: No adapter selected.")
            return
        
        self.log(f"Configuring adapter: {selected_adapter}")
        
        advanced_properties = {
            "ARP offload for WoWLAN": "Disabled",
            "MIMO Power Save Mode": "No SMPS",
            "NS offload for WoWLAN": "Disabled"
        }
        
        tcp_parameters = {
            "autotuninglevel": "normal",
            "rss": "enabled"
        }
        
        for name, value in advanced_properties.items():
            self.log(f"Setting {name} to {value}")
            command = f'Set-NetAdapterAdvancedProperty -Name "{selected_adapter}" -DisplayName "{name}" -DisplayValue "{value}"'
            output = self.run_command(command)
            if output is None:
                self.log(f"Skipped setting {name} due to error.")
        
        for key, value in tcp_parameters.items():
            self.log(f"Setting TCP {key} to {value}")
            command = f'netsh int tcp set global {key}={value}'
            output = self.run_command(command)
            if output is None:
                self.log(f"Skipped setting TCP {key} due to error.")
        
        self.log("Resetting Winsock and IP stack")
        if self.run_command('netsh winsock reset') is None:
            self.log("Skipped Winsock reset due to error.")
        if self.run_command('netsh int ip reset') is None:
            self.log("Skipped IP reset due to error.")
        if self.run_command('ipconfig /release') is None:
            self.log("Skipped IP release due to error.")
        
        self.log("Waiting 5 seconds for adapter reset")
        self.root.after(5000, self.renew_ip)
    
    def renew_ip(self):
        if self.run_command('ipconfig /renew') is None:
            self.log("Skipped IP renew due to error.")
        if self.run_command('ipconfig /flushdns') is None:
            self.log("Skipped DNS flush due to error.")
        else:
            messagebox.showinfo("Success", "Wi-Fi adapter configured successfully.")
            self.log("Wi-Fi adapter configured successfully.")
    
    def run_command(self, command):
        try:
            result = subprocess.run(
                ["powershell.exe", "-Command", command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.stdout:
                self.log(result.stdout.strip())
            if result.stderr:
                self.log(result.stderr.strip())
            if result.returncode != 0:
                raise Exception(f"Command '{command}' failed with exit code {result.returncode}")
            return result.stdout.strip()
        except Exception as e:
            self.log(f"Command execution failed: {e}")
            with open("error_log.txt", "a") as f:  # Append to the log file
                f.write(f"Command: {command}\nError: {str(e)}\n")
            return None

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log_text.get(1.0, tk.END))
        messagebox.showinfo("Info", "Log copied to clipboard.")
        self.log("Log copied to clipboard.")

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        root = tk.Tk()
        app = WifiConfigurator(root)
        root.mainloop()
