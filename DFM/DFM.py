import os
import sys
import json
import ctypes
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import filedialog
import subprocess
import psutil
import shutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def log_action(message):
    log_output.insert(tk.END, message + "\n")
    log_output.see(tk.END)

def clear_log():
    log_output.delete('1.0', tk.END)

def update_status_labels(devtools_enabled, window_unlocked, skip_update_enabled):
    devtools_status_label.config(text="Enabled" if devtools_enabled else "Disabled", fg="green" if devtools_enabled else "red")
    window_status_label.config(text="Unlocked" if window_unlocked else "Locked", fg="green" if window_unlocked else "red")
    skip_update_status_label.config(text="Enabled" if skip_update_enabled else "Disabled", fg="green" if skip_update_enabled else "red")

def check_status():
    settings_path = os.path.join(os.getenv('APPDATA'), 'discord', 'settings.json')

    if not os.path.exists(settings_path):
        log_action("Discord settings.json file not found. Creating with default settings.")
        default_settings = {
            "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING": False
        }
        try:
            with open(settings_path, 'w') as file:
                json.dump(default_settings, file, indent=4)
            devtools_enabled = default_settings["DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"]
            update_status_labels(devtools_enabled, False, False)
            log_action(f"DevTools status set to: {'Enabled' if devtools_enabled else 'Disabled'}")
        except Exception as e:
            log_action(f"Error creating settings.json: {str(e)}")
        return

    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)
            devtools_enabled = settings.get("DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING", False)
            window_unlocked = "MIN_WIDTH" in settings and "MIN_HEIGHT" in settings
            skip_update_enabled = settings.get("SKIP_HOST_UPDATE", False)
            update_status_labels(devtools_enabled, window_unlocked, skip_update_enabled)
            log_action(f"DevTools status checked: {'Enabled' if devtools_enabled else 'Disabled'}")
            log_action(f"Window Size status checked: {'Unlocked' if window_unlocked else 'Locked'}")
            log_action(f"Skip Update status checked: {'Enabled' if skip_update_enabled else 'Disabled'}")
    except json.JSONDecodeError as e:
        log_action(f"Error reading settings.json: {str(e)}")
        update_status_labels(False, False, False)
    except Exception as e:
        log_action(f"Unexpected error: {str(e)}")
        update_status_labels(False, False, False)

def set_devtools_status(enable):
    settings_path = os.path.join(os.getenv('APPDATA'), 'discord', 'settings.json')

    if not os.path.exists(settings_path):
        log_action("Discord settings.json file not found. Creating with default settings.")
        settings = {}
    else:
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
        except json.JSONDecodeError as e:
            log_action(f"Error reading settings.json: {str(e)}. Recreating the file.")
            settings = {}
        except Exception as e:
            log_action(f"Unexpected error: {str(e)}. Recreating the file.")
            settings = {}

    if enable:
        if settings.get("DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"):
            log_action("DevTools already enabled.")
        else:
            settings["DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"] = True
            log_action('Added "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING": true')
    else:
        if "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING" in settings:
            settings.pop("DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING")
            log_action('Removed "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"=true')
        else:
            log_action("DevTools already disabled.")

    try:
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)
        update_status_labels(enable, "MIN_WIDTH" in settings and "MIN_HEIGHT" in settings, settings.get("SKIP_HOST_UPDATE", False))
    except Exception as e:
        log_action(f"Error updating settings.json: {str(e)}")

def set_window_status(unlock):
    settings_path = os.path.join(os.getenv('APPDATA'), 'discord', 'settings.json')

    if not os.path.exists(settings_path):
        log_action("Discord settings.json file not found. Creating with default settings.")
        settings = {}
    else:
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
        except json.JSONDecodeError as e:
            log_action(f"Error reading settings.json: {str(e)}. Recreating the file.")
            settings = {}
        except Exception as e:
            log_action(f"Unexpected error: {str(e)}. Recreating the file.")
            settings = {}

    if unlock:
        if "MIN_WIDTH" in settings and "MIN_HEIGHT" in settings:
            log_action("Window Size already unlocked.")
        else:
            settings["MIN_WIDTH"] = 0
            settings["MIN_HEIGHT"] = 0
            log_action('Added\n"MIN_WIDTH": 0,\n"MIN_HEIGHT": 0')
    else:
        if "MIN_WIDTH" in settings and "MIN_HEIGHT" in settings:
            settings.pop("MIN_WIDTH")
            settings.pop("MIN_HEIGHT")
            log_action('Removed\n"MIN_WIDTH": 0,\n"MIN_HEIGHT": 0')
        else:
            log_action("Window Size already locked.")

    try:
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)
        update_status_labels("DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING" in settings and settings["DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"], unlock, settings.get("SKIP_HOST_UPDATE", False))
    except Exception as e:
        log_action(f"Error updating settings.json: {str(e)}")

def set_skip_update_status(enable):
    settings_path = os.path.join(os.getenv('APPDATA'), 'discord', 'settings.json')

    if not os.path.exists(settings_path):
        log_action("Discord settings.json file not found. Creating with default settings.")
        settings = {}
    else:
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
        except json.JSONDecodeError as e:
            log_action(f"Error reading settings.json: {str(e)}. Recreating the file.")
            settings = {}
        except Exception as e:
            log_action(f"Unexpected error: {str(e)}. Recreating the file.")
            settings = {}

    if enable:
        if settings.get("SKIP_HOST_UPDATE"):
            log_action("Skip Update already enabled.")
        else:
            settings["SKIP_HOST_UPDATE"] = True
            log_action('Added "SKIP_HOST_UPDATE": true')
    else:
        if "SKIP_HOST_UPDATE" in settings:
            settings.pop("SKIP_HOST_UPDATE")
            log_action('Removed "SKIP_HOST_UPDATE"=true')
        else:
            log_action("Skip Update already disabled.")

    try:
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)
        update_status_labels("DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING" in settings and settings["DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"], "MIN_WIDTH" in settings and "MIN_HEIGHT" in settings, enable)
    except Exception as e:
        log_action(f"Error updating settings.json: {str(e)}")

def check_and_terminate_discord():
    discord_terminated = False
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if process.info["name"] == "Discord.exe":
            response = messagebox.askyesno("Discord is running", "Discord is currently running. Do you want to terminate it?")
            if response:
                process.terminate()
                discord_terminated = True
            else:
                sys.exit()

    # Wait for processes to terminate
    if discord_terminated:
        gone, still_alive = psutil.wait_procs(psutil.process_iter(attrs=["pid", "name"]), timeout=5)
        for p in still_alive:
            log_action(f"Forcefully terminating process {p.info['pid']} - {p.info['name']}")
            p.kill()

    return discord_terminated

def fix_window_pos_size():
    clear_log()
    settings_path = os.path.join(os.getenv('APPDATA'), 'discord', 'settings.json')

    if not os.path.exists(settings_path):
        log_action("Discord settings.json file not found. Creating with default settings.")
        settings = {}
    else:
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
        except json.JSONDecodeError as e:
            log_action(f"Error reading settings.json: {str(e)}. Recreating the file.")
            settings = {}
        except Exception as e:
            log_action(f"Unexpected error: {str(e)}. Recreating the file.")
            settings = {}

    settings["WINDOW_BOUNDS"] = {
        "x": 0,
        "y": 0,
        "width": 1280,
        "height": 800
    }
    log_action('Added\n"WINDOW_BOUNDS": {\n"x": 0,\n"y": 0,\n"width": 1280,\n"height": 800\n}')

    try:
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)
        log_action("Window position and size fixed in settings.json.")
    except Exception as e:
        log_action(f"Error updating settings.json: {str(e)}")

def clear_cache():
    clear_log()
    cache_dirs = [
        os.path.join(os.getenv('APPDATA'), 'discord', 'Cache'),
        os.path.join(os.getenv('APPDATA'), 'discord', 'Code Cache'),
        os.path.join(os.getenv('APPDATA'), 'discord', 'GPUCache')
    ]
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                log_action(f"Cleared cache: {cache_dir}")
            except Exception as e:
                log_action(f"Error clearing cache {cache_dir}: {str(e)}")
        else:
            log_action(f"Cache folder not found: {cache_dir}")

def on_enable_devtools():
    clear_log()
    set_devtools_status(True)

def on_disable_devtools():
    clear_log()
    set_devtools_status(False)

def on_unlock_window():
    clear_log()
    set_window_status(True)

def on_lock_window():
    clear_log()
    set_window_status(False)

def on_enable_skip_update():
    clear_log()
    set_skip_update_status(True)

def on_disable_skip_update():
    clear_log()
    set_skip_update_status(False)

def show_instructions():
    messagebox.showinfo("Instructions", 
        "DevTools will Enable/Disable dev tools such as inspecting elements and console (Ctrl+Shift+I).\n"
        "Window Size will Lock/Unlock minimum window size requirements.\n"
        "Skip Update will Enable/Disable auto updates.\n\n"
        "Tools > Fix Window Pos/Size will set position to 0x,0y if window is offscreen.\n"
        "Tools > Clear Cache will delete cache folders.")

def open_settings_file():
    settings_path = os.path.join(os.getenv('APPDATA'), 'discord', 'settings.json')
    if os.path.exists(settings_path):
        os.startfile(settings_path)
    else:
        messagebox.showerror("Error", "settings.json file not found.")

def open_folder_location():
    folder_path = os.path.join(os.getenv('APPDATA'), 'discord')
    if os.path.exists(folder_path):
        subprocess.Popen(f'explorer "{folder_path}"')
    else:
        messagebox.showerror("Error", "Discord folder not found.")

def on_copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(log_output.get('1.0', tk.END))

def on_close():
    root.destroy()

def initialize_gui():
    global root, log_output, devtools_status_label, window_status_label, skip_update_status_label

    root = tk.Tk()
    root.title('Discord Feature Manager')

    window_width = 600
    window_height = 425

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate center position
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Set geometry
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.resizable(False, False)

    menu_bar = tk.Menu(root)
    
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open File", command=open_settings_file)
    file_menu.add_command(label="Open Folder Location", command=open_folder_location)
    menu_bar.add_cascade(label="File", menu=file_menu)
    
    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label="Fix Window Pos/Size", command=fix_window_pos_size)
    tools_menu.add_command(label="Clear Cache", command=clear_cache)
    menu_bar.add_cascade(label="Tools", menu=tools_menu)
    
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Instructions", command=show_instructions)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    
    root.config(menu=menu_bar)

    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

    section_label = tk.Label(left_frame, text="DevTools Status", font=("Helvetica", 10, "bold", "underline"), fg="black")
    section_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

    label1 = tk.Label(left_frame, text="DevTools: ", font=("Helvetica", 10), fg="black")
    label1.grid(row=1, column=0, sticky=tk.W)
    devtools_status_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
    devtools_status_label.grid(row=1, column=1, sticky=tk.W)

    button_frame = tk.Frame(left_frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)
    enable_button = tk.Button(button_frame, text="Enable", command=on_enable_devtools)
    enable_button.pack(side=tk.LEFT, padx=10)
    disable_button = tk.Button(button_frame, text="Disable", command=on_disable_devtools)
    disable_button.pack(side=tk.LEFT, padx=10)

    section_label = tk.Label(left_frame, text="Window Size Status", font=("Helvetica", 10, "bold", "underline"), fg="black")
    section_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

    label2 = tk.Label(left_frame, text="Window Size: ", font=("Helvetica", 10), fg="black")
    label2.grid(row=4, column=0, sticky=tk.W)
    window_status_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
    window_status_label.grid(row=4, column=1, sticky=tk.W)

    button_frame = tk.Frame(left_frame)
    button_frame.grid(row=5, column=0, columnspan=2, pady=10)
    unlock_button = tk.Button(button_frame, text="Unlock", command=on_unlock_window)
    unlock_button.pack(side=tk.LEFT, padx=10)
    lock_button = tk.Button(button_frame, text="Lock", command=on_lock_window)
    lock_button.pack(side=tk.LEFT, padx=10)

    section_label = tk.Label(left_frame, text="Skip Update Status", font=("Helvetica", 10, "bold", "underline"), fg="black")
    section_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

    label3 = tk.Label(left_frame, text="Skip Update: ", font=("Helvetica", 10), fg="black")
    label3.grid(row=7, column=0, sticky=tk.W)
    skip_update_status_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
    skip_update_status_label.grid(row=7, column=1, sticky=tk.W)

    button_frame = tk.Frame(left_frame)
    button_frame.grid(row=8, column=0, columnspan=2, pady=10)
    enable_skip_update_button = tk.Button(button_frame, text="Enable", command=on_enable_skip_update)
    enable_skip_update_button.pack(side=tk.LEFT, padx=10)
    disable_skip_update_button = tk.Button(button_frame, text="Disable", command=on_disable_skip_update)
    disable_skip_update_button.pack(side=tk.LEFT, padx=10)

    log_frame = tk.Frame(main_frame)
    log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    log_output = scrolledtext.ScrolledText(log_frame, width=50, height=20, wrap=tk.WORD)
    log_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    bottom_button_frame = tk.Frame(root)
    bottom_button_frame.pack(pady=10)

    copy_button = tk.Button(bottom_button_frame, text="Copy to Clipboard", command=on_copy_to_clipboard)
    copy_button.pack(side=tk.LEFT, padx=10)

    close_button = tk.Button(bottom_button_frame, text="Close", command=on_close)
    close_button.pack(side=tk.LEFT, padx=10)

    check_status()
    root.after(100, check_and_terminate_discord)
    root.mainloop()

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        initialize_gui()
