import os
import sys
import winreg
import ctypes
import tkinter as tk
from tkinter import messagebox, scrolledtext

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def enable_windows_copilot():
    copilot_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot"
    context_registry_path = r"SOFTWARE\Policies\Microsoft\Edge"
    sidebar_registry_path = r"Software\Microsoft\Windows\Shell\Copilot\BingChat"

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, copilot_registry_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteKey(key, "")
            log_action(f"Deleted registry key: {copilot_registry_path}")
    except FileNotFoundError:
        log_action(f"Registry key {copilot_registry_path} not found.")
        log_action("Windows CoPilot was already enabled.")

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, context_registry_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteKey(key, "")
            log_action(f"Deleted registry key: {context_registry_path}")
    except FileNotFoundError:
        log_action(f"Registry key {context_registry_path} not found.")
        log_action("Context clues were already enabled.")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sidebar_registry_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteKey(key, "")
            log_action(f"Deleted registry key: {sidebar_registry_path}")
    except FileNotFoundError:
        log_action(f"Registry key {sidebar_registry_path} not found.")
        log_action("Sidebar was already enabled.")
    
    log_action("Windows CoPilot Enabled successfully.")
    update_status_labels(True, True, True)
    return True

def disable_windows_copilot():
    copilot_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot"
    context_registry_path = r"SOFTWARE\Policies\Microsoft\Edge"
    context_value_name = "ClickOnceEnabled"
    sidebar_registry_path = r"Software\Microsoft\Windows\Shell\Copilot\BingChat"
    sidebar_value_name = "IsUserEligible"

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, copilot_registry_path) as key:
            try:
                value, _ = winreg.QueryValueEx(key, "TurnOffWindowsCopilot")
                if value == 1:
                    log_action(f"Registry key {copilot_registry_path} found.")
                    log_action(f"Registry value: {copilot_registry_path}\\TurnOffWindowsCopilot found with value set to {value}.")
                    log_action("Windows CoPilot was already disabled.")
            except FileNotFoundError:
                pass
            
            winreg.SetValueEx(key, "TurnOffWindowsCopilot", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {copilot_registry_path}\\TurnOffWindowsCopilot = 1")

        log_action("Windows CoPilot Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Windows CoPilot. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, context_registry_path) as key:
            try:
                value, _ = winreg.QueryValueEx(key, context_value_name)
                if value == 0:
                    log_action(f"Registry key {context_registry_path} found.")
                    log_action(f"Registry value: {context_registry_path}\\{context_value_name} found with value set to {value}.")
                    log_action("Context clues were already disabled.")
            except FileNotFoundError:
                pass
            
            winreg.SetValueEx(key, context_value_name, 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {context_registry_path}\\{context_value_name} = 0")

        log_action("Context clues Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Context clues. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, sidebar_registry_path) as key:
            try:
                value, _ = winreg.QueryValueEx(key, sidebar_value_name)
                if value == 0:
                    log_action(f"Registry key {sidebar_registry_path} found.")
                    log_action(f"Registry value: {sidebar_registry_path}\\{sidebar_value_name} found with value set to {value}.")
                    log_action("Sidebar was already disabled.")
            except FileNotFoundError:
                pass
            
            winreg.SetValueEx(key, sidebar_value_name, 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {sidebar_registry_path}\\{sidebar_value_name} = 0")

        log_action("Sidebar Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Sidebar. Error: {str(e)}")
        return False

    update_status_labels(False, False, False)
    return True

def enable_cortana():
    cortana_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    consent_registry_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
    location_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, cortana_registry_path) as key:
            winreg.SetValueEx(key, "AllowCortana", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {cortana_registry_path}\\AllowCortana = 1")

        log_action("Cortana Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Cortana. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, consent_registry_path) as key:
            winreg.SetValueEx(key, "CortanaConsent", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {consent_registry_path}\\CortanaConsent = 1")

        log_action("Cortana Consent Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Cortana Consent. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, location_registry_path) as key:
            winreg.SetValueEx(key, "AllowSearchToUseLocation", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {location_registry_path}\\AllowSearchToUseLocation = 1")

        log_action("Cortana Location Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Cortana Location. Error: {str(e)}")
        return False

    update_cortana_status_labels(True, True, True)
    return True

def disable_cortana():
    cortana_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    consent_registry_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
    location_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, cortana_registry_path) as key:
            winreg.SetValueEx(key, "AllowCortana", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {cortana_registry_path}\\AllowCortana = 0")

        log_action("Cortana Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Cortana. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, consent_registry_path) as key:
            winreg.SetValueEx(key, "CortanaConsent", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {consent_registry_path}\\CortanaConsent = 0")

        log_action("Cortana Consent Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Cortana Consent. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, location_registry_path) as key:
            winreg.SetValueEx(key, "AllowSearchToUseLocation", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {location_registry_path}\\AllowSearchToUseLocation = 0")

        log_action("Cortana Location Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Cortana Location. Error: {str(e)}")
        return False

    update_cortana_status_labels(False, False, False)
    return True

def enable_web_search():
    web_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    bing_search_registry_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
    connected_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    metered_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, web_search_registry_path) as key:
            winreg.SetValueEx(key, "DisableWebSearch", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {web_search_registry_path}\\DisableWebSearch = 0")

        log_action("Web Search Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Web Search. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, bing_search_registry_path) as key:
            winreg.SetValueEx(key, "BingSearchEnabled", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {bing_search_registry_path}\\BingSearchEnabled = 1")

        log_action("Bing Search Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Bing Search. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, connected_search_registry_path) as key:
            winreg.SetValueEx(key, "ConnectedSearchUseWeb", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {connected_search_registry_path}\\ConnectedSearchUseWeb = 1")

        log_action("Connected Search Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Connected Search. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, metered_search_registry_path) as key:
            winreg.SetValueEx(key, "ConnectedSearchUseWebOverMeteredConnections", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {metered_search_registry_path}\\ConnectedSearchUseWebOverMeteredConnections = 1")

        log_action("Metered Search Enabled successfully.")
    except Exception as e:
        log_action(f"Failed to Enable Metered Search. Error: {str(e)}")
        return False

    update_web_search_status_labels(True, True, True, True)
    return True

def disable_web_search():
    web_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    bing_search_registry_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
    connected_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    metered_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, web_search_registry_path) as key:
            winreg.SetValueEx(key, "DisableWebSearch", 0, winreg.REG_DWORD, 1)
            log_action(f"Set registry value: {web_search_registry_path}\\DisableWebSearch = 1")

        log_action("Web Search Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Web Search. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, bing_search_registry_path) as key:
            winreg.SetValueEx(key, "BingSearchEnabled", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {bing_search_registry_path}\\BingSearchEnabled = 0")

        log_action("Bing Search Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Bing Search. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, connected_search_registry_path) as key:
            winreg.SetValueEx(key, "ConnectedSearchUseWeb", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {connected_search_registry_path}\\ConnectedSearchUseWeb = 0")

        log_action("Connected Search Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Connected Search. Error: {str(e)}")
        return False

    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, metered_search_registry_path) as key:
            winreg.SetValueEx(key, "ConnectedSearchUseWebOverMeteredConnections", 0, winreg.REG_DWORD, 0)
            log_action(f"Set registry value: {metered_search_registry_path}\\ConnectedSearchUseWebOverMeteredConnections = 0")

        log_action("Metered Search Disabled successfully.")
    except Exception as e:
        log_action(f"Failed to Disable Metered Search. Error: {str(e)}")
        return False

    update_web_search_status_labels(False, False, False, False)
    return True

def log_action(message):
    log_output.insert(tk.END, message + "\n")
    log_output.see(tk.END)

def clear_log():
    log_output.delete('1.0', tk.END)

def update_status_labels(copilot_enabled, context_enabled, sidebar_enabled):
    windows_value_label.config(text="Enabled" if copilot_enabled else "Disabled", fg="green" if copilot_enabled else "red")
    context_value_label.config(text="Enabled" if context_enabled else "Disabled", fg="green" if context_enabled else "red")
    sidebar_value_label.config(text="Enabled" if sidebar_enabled else "Disabled", fg="green" if sidebar_enabled else "red")

def update_cortana_status_labels(cortana_enabled, consent_enabled, location_enabled):
    cortana_value_label_value.config(text="Enabled" if cortana_enabled else "Disabled", fg="green" if cortana_enabled else "red")
    consent_value_label.config(text="Enabled" if consent_enabled else "Disabled", fg="green" if consent_enabled else "red")
    location_value_label.config(text="Enabled" if location_enabled else "Disabled", fg="green" if location_enabled else "red")

def update_web_search_status_labels(web_search_enabled, bing_search_enabled, connected_search_enabled, metered_search_enabled):
    web_search_value_label_value.config(text="Enabled" if web_search_enabled else "Disabled", fg="green" if web_search_enabled else "red")
    bing_search_value_label.config(text="Enabled" if bing_search_enabled else "Disabled", fg="green" if bing_search_enabled else "red")
    connected_search_value_label.config(text="Enabled" if connected_search_enabled else "Disabled", fg="green" if connected_search_enabled else "red")
    metered_search_value_label.config(text="Enabled" if metered_search_enabled else "Disabled", fg="green" if metered_search_enabled else "red")

def check_initial_status():
    copilot_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot"
    context_registry_path = r"SOFTWARE\Policies\Microsoft\Edge"
    context_value_name = "ClickOnceEnabled"
    sidebar_registry_path = r"Software\Microsoft\Windows\Shell\Copilot\BingChat"
    sidebar_value_name = "IsUserEligible"
    
    copilot_enabled = True
    context_enabled = True
    sidebar_enabled = True

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, copilot_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "TurnOffWindowsCopilot")
            if value == 1:
                copilot_enabled = False
    except FileNotFoundError:
        copilot_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Co-Pilot status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, context_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, context_value_name)
            if value == 0:
                context_enabled = False
    except FileNotFoundError:
        context_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Context clues status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sidebar_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, sidebar_value_name)
            if value == 0:
                sidebar_enabled = False
    except FileNotFoundError:
        sidebar_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Sidebar status: {str(e)}")

    update_status_labels(copilot_enabled, context_enabled, sidebar_enabled)

def check_initial_cortana_status():
    cortana_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    consent_registry_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
    location_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    
    cortana_enabled = True
    consent_enabled = True
    location_enabled = True

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cortana_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "AllowCortana")
            if value == 0:
                cortana_enabled = False
    except FileNotFoundError:
        cortana_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Cortana status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, consent_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "CortanaConsent")
            if value == 0:
                consent_enabled = False
    except FileNotFoundError:
        consent_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Cortana Consent status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, location_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "AllowSearchToUseLocation")
            if value == 0:
                location_enabled = False
    except FileNotFoundError:
        location_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Cortana Location status: {str(e)}")

    update_cortana_status_labels(cortana_enabled, consent_enabled, location_enabled)

def check_initial_web_search_status():
    web_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    bing_search_registry_path = r"Software\Microsoft\Windows\CurrentVersion\Search"
    connected_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    metered_search_registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    
    web_search_enabled = True
    bing_search_enabled = True
    connected_search_enabled = True
    metered_search_enabled = True

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, web_search_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "DisableWebSearch")
            if value == 1:
                web_search_enabled = False
    except FileNotFoundError:
        web_search_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Web Search status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, bing_search_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "BingSearchEnabled")
            if value == 0:
                bing_search_enabled = False
    except FileNotFoundError:
        bing_search_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Bing Search status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, connected_search_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "ConnectedSearchUseWeb")
            if value == 0:
                connected_search_enabled = False
    except FileNotFoundError:
        connected_search_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Connected Search status: {str(e)}")

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, metered_search_registry_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "ConnectedSearchUseWebOverMeteredConnections")
            if value == 0:
                metered_search_enabled = False
    except FileNotFoundError:
        metered_search_enabled = True
    except Exception as e:
        log_action(f"Error checking initial Metered Search status: {str(e)}")

    update_web_search_status_labels(web_search_enabled, bing_search_enabled, connected_search_enabled, metered_search_enabled)

def on_enable_copilot():
    clear_log()
    if enable_windows_copilot():
        log_action("Action completed: Enable Windows CoPilot")
    else:
        log_action("Action failed: Enable Windows CoPilot")

def on_disable_copilot():
    clear_log()
    if disable_windows_copilot():
        log_action("Action completed: Disable Windows CoPilot")
    else:
        log_action("Action failed: Disable Windows CoPilot")

def on_enable_cortana():
    clear_log()
    if enable_cortana():
        log_action("Action completed: Enable Cortana")
    else:
        log_action("Action failed: Enable Cortana")

def on_disable_cortana():
    clear_log()
    if disable_cortana():
        log_action("Action completed: Disable Cortana")
    else:
        log_action("Action failed: Disable Cortana")

def on_enable_web_search():
    clear_log()
    if enable_web_search():
        log_action("Action completed: Enable Web Search")
    else:
        log_action("Action failed: Enable Web Search")

def on_disable_web_search():
    clear_log()
    if disable_web_search():
        log_action("Action completed: Disable Web Search")
    else:
        log_action("Action failed: Disable Web Search")

def on_copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(log_output.get('1.0', tk.END))

def on_close():
    root.destroy()

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        root = tk.Tk()
        root.title('Windows "Feature" Manager')
        root.geometry("900x600")

        main_frame = tk.Frame(root)
        main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Left Frame for Status and Buttons
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # Co-Pilot Section
        copilot_label = tk.Label(left_frame, text="Co-Pilot Status", font=("Helvetica", 10, "bold", "underline"), fg="black")
        copilot_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        windows_label = tk.Label(left_frame, text="Windows: ", font=("Helvetica", 10), fg="black")
        windows_label.grid(row=1, column=0, sticky=tk.W)
        windows_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        windows_value_label.grid(row=1, column=1, sticky=tk.W)

        context_label = tk.Label(left_frame, text="Context: ", font=("Helvetica", 10), fg="black")
        context_label.grid(row=2, column=0, sticky=tk.W)
        context_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        context_value_label.grid(row=2, column=1, sticky=tk.W)

        sidebar_label = tk.Label(left_frame, text="Sidebar: ", font=("Helvetica", 10), fg="black")
        sidebar_label.grid(row=3, column=0, sticky=tk.W)
        sidebar_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        sidebar_value_label.grid(row=3, column=1, sticky=tk.W)

        copilot_button_frame = tk.Frame(left_frame)
        copilot_button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        enable_button = tk.Button(copilot_button_frame, text="Enable", command=on_enable_copilot)
        enable_button.pack(side=tk.LEFT, padx=10)
        disable_button = tk.Button(copilot_button_frame, text="Disable", command=on_disable_copilot)
        disable_button.pack(side=tk.LEFT, padx=10)

        # Cortana Section
        cortana_label = tk.Label(left_frame, text="Cortana Status", font=("Helvetica", 10, "bold", "underline"), fg="black")
        cortana_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))

        cortana_value_label = tk.Label(left_frame, text="Cortana: ", font=("Helvetica", 10), fg="black")
        cortana_value_label.grid(row=6, column=0, sticky=tk.W)
        cortana_value_label_value = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        cortana_value_label_value.grid(row=6, column=1, sticky=tk.W)

        consent_label = tk.Label(left_frame, text="Consent: ", font=("Helvetica", 10), fg="black")
        consent_label.grid(row=7, column=0, sticky=tk.W)
        consent_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        consent_value_label.grid(row=7, column=1, sticky=tk.W)

        location_label = tk.Label(left_frame, text="Location: ", font=("Helvetica", 10), fg="black")
        location_label.grid(row=8, column=0, sticky=tk.W)
        location_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        location_value_label.grid(row=8, column=1, sticky=tk.W)

        cortana_button_frame = tk.Frame(left_frame)
        cortana_button_frame.grid(row=9, column=0, columnspan=2, pady=10)
        enable_button = tk.Button(cortana_button_frame, text="Enable", command=on_enable_cortana)
        enable_button.pack(side=tk.LEFT, padx=10)
        disable_button = tk.Button(cortana_button_frame, text="Disable", command=on_disable_cortana)
        disable_button.pack(side=tk.LEFT, padx=10)

        # Web Search Section
        web_search_label = tk.Label(left_frame, text="Web Search Status", font=("Helvetica", 10, "bold", "underline"), fg="black")
        web_search_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))

        web_search_value_label = tk.Label(left_frame, text="Web Search: ", font=("Helvetica", 10), fg="black")
        web_search_value_label.grid(row=11, column=0, sticky=tk.W)
        web_search_value_label_value = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        web_search_value_label_value.grid(row=11, column=1, sticky=tk.W)

        bing_search_label = tk.Label(left_frame, text="Bing Search: ", font=("Helvetica", 10), fg="black")
        bing_search_label.grid(row=12, column=0, sticky=tk.W)
        bing_search_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        bing_search_value_label.grid(row=12, column=1, sticky=tk.W)

        connected_search_label = tk.Label(left_frame, text="Connected Search: ", font=("Helvetica", 10), fg="black")
        connected_search_label.grid(row=13, column=0, sticky=tk.W)
        connected_search_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        connected_search_value_label.grid(row=13, column=1, sticky=tk.W)

        metered_search_label = tk.Label(left_frame, text="Metered Search: ", font=("Helvetica", 10), fg="black")
        metered_search_label.grid(row=14, column=0, sticky=tk.W)
        metered_search_value_label = tk.Label(left_frame, text="Unknown", font=("Helvetica", 10))
        metered_search_value_label.grid(row=14, column=1, sticky=tk.W)

        web_search_button_frame = tk.Frame(left_frame)
        web_search_button_frame.grid(row=15, column=0, columnspan=2, pady=10)
        enable_button = tk.Button(web_search_button_frame, text="Enable", command=on_enable_web_search)
        enable_button.pack(side=tk.LEFT, padx=10)
        disable_button = tk.Button(web_search_button_frame, text="Disable", command=on_disable_web_search)
        disable_button.pack(side=tk.LEFT, padx=10)

        # Right Frame for Log Output
        log_frame = tk.Frame(main_frame)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        log_output = scrolledtext.ScrolledText(log_frame, width=50, height=30, wrap=tk.WORD)
        log_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Bottom Buttons
        bottom_button_frame = tk.Frame(root)
        bottom_button_frame.pack(pady=10)

        copy_button = tk.Button(bottom_button_frame, text="Copy to Clipboard", command=on_copy_to_clipboard)
        copy_button.pack(side=tk.LEFT, padx=10)

        close_button = tk.Button(bottom_button_frame, text="Close", command=on_close)
        close_button.pack(side=tk.LEFT, padx=10)

        check_initial_status()
        check_initial_cortana_status()
        check_initial_web_search_status()
        root.mainloop()
