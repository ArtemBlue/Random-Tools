import tkinter as tk
from tkinter import ttk
import requests
import subprocess
import threading
import webbrowser
import pyperclip
import netifaces as ni

def get_gateway_ips():
    """Retrieve all possible default gateway IPs based on the operating system."""
    gateways = []
    try:
        if subprocess.os.name == 'nt':  # Windows
            gateways.extend(ni.gateways()['default'][ni.AF_INET])
            if ni.AF_INET6 in ni.gateways()['default']:
                gateways.extend(ni.gateways()['default'][ni.AF_INET6])
        else:  # Unix/Linux
            gateways.extend(ni.gateways()['default'][ni.AF_INET])
            if ni.AF_INET6 in ni.gateways()['default']:
                gateways.extend(ni.gateways()['default'][ni.AF_INET6])
        # Filter out IPv6 link-local address (fe80::1)
        gateways = [gateway for gateway in gateways if '%' not in gateway]
    except KeyError:
        pass
    return gateways

def try_open_ip(ip, update_ui):
    """Attempt to open the given IP in a browser if it responds with status 200, 302, or 401."""
    try:
        response = requests.get(f"http://{ip}", timeout=5)
        status_code = response.status_code
        if status_code in [200, 302, 401]:
            update_ui(f"Opening browser to {ip}")
            webbrowser.open_new_tab(f"http://{ip}")
            return True
        else:
            update_ui(f"Failed to connect to {ip}: HTTP status code {status_code}")
    except requests.RequestException as e:
        update_ui(f"Failed to connect to {ip}: {e}")
    return False


def scan_ips(update_ui, on_complete):
    """Scan all detected and common IP addresses."""
    ips_to_check = get_gateway_ips() + ["192.168.1.1", "192.168.0.1", "192.168.2.1", "10.0.0.1", "10.0.1.1", "172.16.0.1", "192.168.1.254"]
    total_ips = len(ips_to_check)
    for i, ip in enumerate(ips_to_check):
        update_ui(f"Checking {ip}...")
        if try_open_ip(ip, update_ui):
            update_ui(f"Successfully opened {ip}")
            on_complete()
            return
        update_ui(f"Progress: {int((i + 1) / total_ips * 100)}%")
    update_ui("All IPs checked. None successful.")
    on_complete()


class App(tk.Tk):
    """Main application class for the router access checker GUI."""
    def __init__(self):
        super().__init__()
        self.title("Router Access Checker")
        self.geometry("500x485")
        self.resizable(False, False)  # Locks the window dimensions

        # Multiline text box
        self.log = tk.Text(self, height=12, state='disabled')  # Adjusted height to 12 lines
        self.log.place(x=10, y=10, width=470, height=400)  # Adjusted width to 470px
        self.log_scrollbar = ttk.Scrollbar(self, command=self.log.yview)
        self.log_scrollbar.place(x=480, y=10, height=400)  # Adjusted x-coordinate to 480px

        # Connect the scrollbar to the multiline text box
        self.log['yscrollcommand'] = self.log_scrollbar.set

        # Progress bar
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.place(x=10, y=420, width=480)  # Adjusted position and width
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=470, mode="determinate")  # Adjusted length to fit the frame
        self.progress_bar.pack(side='left', fill='x', expand=True)

        threading.Thread(target=scan_ips, args=(self.update_status, self.on_scan_complete), daemon=True).start()

        # Copy to Clipboard button
        self.copy_button = ttk.Button(self, text="Copy to Clipboard", command=self.copy_log)
        self.copy_button.place(x=130, y=450)  # Adjusted position

        # Close button
        self.close_button = ttk.Button(self, text="Close", command=self.destroy)
        self.close_button.place(x=250, y=450)  # Adjusted position

    def update_status(self, status):
        """Update the log text area with the current status."""
        self.log['state'] = 'normal'
        self.log.insert('end', status + '\n')
        self.log.see('end')
        self.log['state'] = 'disabled'
        if "Progress" in status:
            parts = status.split(":")
            if len(parts) > 1:
                progress_part = parts[1].strip()
                if progress_part:
                    try:
                        percentage = int(progress_part.split(" ")[0].strip('%'))
                        self.progress_bar['value'] = percentage
                    except ValueError:
                        pass  # Ignore if the percentage cannot be parsed



    def on_scan_complete(self):
        """Update GUI when scanning is complete."""
        self.progress_bar['value'] = 100

    def copy_log(self):
        """Copy log contents to clipboard."""
        log_content = self.log.get("1.0", "end-1c")
        pyperclip.copy(log_content)



if __name__ == "__main__":
    app = App()
    app.mainloop()
