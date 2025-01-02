# Keylogger

This python keylogger captures keystrokes and logs them either to a file or sends them via email. It's designed for educational purposes or for monitoring your own machine's input activities.

## Features

- **Keyboard Logging**: Records all keystrokes and formats special keys (e.g., [ENTER], [CTRL], etc.).
- **Reporting Options**: 
  - Saves logs to a file.
  - Optionally sends logs via email (SMTP).
- **Customizable Interval**: The report frequency can be configured (default is 60 seconds).

## Requirements

- Python 3.x
- `keyboard` module for capturing keystrokes.
- Internet connection for email reporting.
- Admin priviledges to run the script

## Next steps

- [ ] Send the reports over https
- [ ] ?

## Installation

1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Configure the script:
   - Set your email credentials:
     ```python
     EMAIL_ADDRESS = "email@provider.tld"
     EMAIL_PASSWORD = "password_here"
     ```
   - Set the reporting interval:
     ```python
     SEND_REPORT_EVERY = 60  # in seconds
     ```

## How to Run

Run the script using Python:

```bash
sudo python3 keylogger.py
```

## Build with pyinstaller

Use `pyinstaller --onefile --windowed keylogger.py` to create an executable
