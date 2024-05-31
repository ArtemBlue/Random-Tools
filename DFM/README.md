# Discord Feature Manager

This application allows users to manage and configure various Discord settings, such as enabling/disabling DevTools, unlocking/locking window size, and enabling/disabling skip updates. It is available in two formats:
1. A standalone executable file for users who do not want to run the Python script manually.
2. A Python script for those who prefer to execute the script or modify it.

## Features

- Enable or disable Discord DevTools.
- Unlock or lock Discord window size.
- Enable or disable auto updates.
- Clear Discord cache.
- Fix Discord window position and size.
- Easy-to-use graphical user interface.
- Detailed logging of actions performed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

For running the executable:
- No prerequisites needed, just the executable.

For running the script:
- Python 3.6 or higher
- `tkinter` library (usually comes with Python)
- `psutil` library
- `shutil` library
- Windows OS (as it uses Windows commands)

### Installing

#### For the Executable

1. Download the `DiscordFeatureManager.exe` from the releases section.
2. Double-click the executable to run.

#### For the Script

1. Clone this repository or download `DFM.py` directly.
2. Ensure Python, `tkinter`, `psutil`, and `shutil` are installed on your system.
3. Run the script using a command prompt or terminal:
   ```bash
   python DFM.py
