# Router Gateway Access Checker

This application checks for access to router gateways on a local network by attempting to connect to known default gateway IP addresses and common router IP addresses, verifying connectivity.

## Features

- Automatically detects default gateway IPs based on the operating system.
- Checks accessibility of common router IP addresses.
- Logs each connection attempt and the results.
- Features a simple graphical user interface (GUI) for easy interaction.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

For running the executable:
- A Windows operating system is required for the compiled executable.

For running the script:
- Python 3.x
- Required Python packages (tkinter, requests, webbrowser, pyperclip). These can be installed via pip:
  ```bash
  pip install -r requirements.txt
