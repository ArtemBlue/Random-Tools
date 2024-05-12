# Router Gateway Access Checker

## Overview

This Python script checks for access to router gateways on a local network. It attempts to connect to known default gateway IP addresses and common router IP addresses to verify connectivity.

## Features

- Detects default gateway IPs based on the operating system.
- Checks common router IP addresses for accessibility.
- Logs connection attempts and results.
- Provides a simple graphical user interface (GUI) for interaction.

## Usage

### Running the compiled executable:

1. Download the compiled executable from the releases section of the GitHub repository.
2. Double-click the executable file `find_router_login.exe`.
3. The GUI will open, and the script will automatically start scanning for router IPs.
4. Results will be displayed in the GUI and logged.

### Running the Python script:

1. Clone or download the repository to your local machine.
2. Make sure you have Python installed.
3. Install the required Python packages by running: `pip install -r requirements.txt`
4. Run the script: `python find_router_login.py`
5. The script will attempt to connect to known router IPs. Results will be displayed in the GUI and logged.

## Requirements for running on Python

- Python 3.x
- Required Python packages: `tkinter`, `requests`, `webbrowser`, `pyperclip`
- For the compiled executable: Windows operating system




