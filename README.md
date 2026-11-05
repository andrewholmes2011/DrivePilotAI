# DrivePilotAI

A free Windows 11 desktop organizer for reviewing local files and optionally scanning Google Drive metadata.

## Current release: 0.1.0 (starter)

### Included
- Windows desktop interface built with Python and Tkinter.
- Local folder scanning with suggested categories.
- Organization preview before changes.
- Explicit confirmation before moving local files.
- Undo journal for the most recent local organization operation.
- Optional Google Drive metadata scan using Google's official API (read-only).

### Not included yet
- Moving or renaming files inside Google Drive.
- Automatic deletion.
- AI API calls or paid subscriptions.
- Background monitoring.

## Windows 11 setup

1. Install Python 3.11 or newer from https://www.python.org/downloads/.
2. Download this repository to your Windows computer.
3. Double-click `setup.bat`.
4. Choose a local folder, scan it, and review the preview before applying any moves.

The app only scans the folder you select. It does not scan your entire computer automatically.

## Optional Google Drive connection

Google Drive API access can be disabled by school administrators. This app does not bypass school policies or restrictions.

1. Open https://console.cloud.google.com/.
2. Create or select a Google Cloud project, if your account is permitted to do so.
3. Enable the Google Drive API.
4. Configure the OAuth consent screen as required.
5. Create an OAuth Client ID with application type **Desktop app**.
6. Download the client JSON file.
7. Place it at `credentials/client_secret.json` in the project folder.
8. Run `setup.bat` again and select **Connect Google Drive (read-only)**.

The initial Drive connection requests metadata-only read access. The app stores its local token in `credentials/token.json`; that folder is excluded from Git. Never upload OAuth client files or tokens to GitHub.

If your school account blocks the API or OAuth app, stop there and use an account or access method that your administrator permits. Do not try to work around the restriction.

## Safety

- Scanning is read-only.
- Local moves require a separate confirmation.
- No automatic deletion.
- Google Drive scanning is read-only in this starter release.
- Review the preview before moving files.
- Keep a separate backup of important files.

## Project structure

```
DrivePilotAI/
├── app/
│   ├── main.py
│   ├── organizer.py
│   └── drive_api.py
├── .gitignore
├── requirements.txt
├── setup.bat
└── README.md
```

## License

MIT
