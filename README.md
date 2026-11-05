# DrivePilotAI

**A free browser-based file organizer. No Python installation, desktop installer, or paid AI API required.**

## Open the app

After GitHub Pages is enabled, open:

https://andrewholmes2011.github.io/DrivePilotAI/

You can also run it from Visual Studio Code with the Live Server extension, or open `index.html` in a compatible browser. Folder access works best from the hosted HTTPS page or localhost in current Chrome or Edge.

## Features

- Responsive dashboard for Windows, Chromebook, and modern browsers.
- Scan a folder you explicitly choose using the browser File System Access API.
- Categorize documents, spreadsheets, presentations, images, videos, audio, archives, code, and other files.
- Search and filter scan results.
- Preview proposed local moves before applying them.
- Confirm before moving local files. Each file is copied and size-verified before the original is removed.
- Undo recent moves during the current browser session.
- Optional Google Drive metadata scan using Google's official OAuth flow and read-only Drive scope.

## Start using it

1. Open the repository and download the ZIP, or clone it in Visual Studio Code.
2. Open the project folder in VS Code.
3. Open `index.html` with Live Server, or enable GitHub Pages for the repository.
4. In Chrome or Edge, choose **Choose a folder** and select the folder you want to organize.
5. Scan, review the categories, preview the moves, and only then choose **Apply approved local moves**.

No Python, Node.js, build process, or package installation is required.

## Enable GitHub Pages

In the repository, open **Settings → Pages**. Under Build and deployment, choose **Deploy from a branch**, select `main` and `/ (root)`, then save. GitHub will publish the app at:

https://andrewholmes2011.github.io/DrivePilotAI/

## Optional Google Drive scan

Google Drive scanning is metadata-only and read-only. It does not move, rename, or delete Drive files.

1. In Google Cloud Console, create or select a project if permitted.
2. Enable the Google Drive API.
3. Configure the OAuth consent screen.
4. Create an OAuth Client ID with application type **Web application**.
5. Add the exact hosted app origin to **Authorized JavaScript origins** (for example, `https://andrewholmes2011.github.io`). For local testing, add the localhost origin used by Live Server.
6. Copy the client ID into the app's Google OAuth Client ID field and save it in that browser.
7. Choose **Connect Google Drive** and complete Google's sign-in and consent flow.

The app requests only `drive.metadata.readonly`. Do not put client secrets in this project. A browser OAuth client ID is not a client secret. Google Workspace administrators may block third-party OAuth clients or Drive API access. If access is blocked, ask your administrator; this app does not bypass school controls.

## Browser and safety limitations

- Folder scanning and local moves require a browser that supports the File System Access API (current Chrome or Edge recommended) and a secure context such as HTTPS or localhost.
- You must explicitly choose a folder and grant access. The app cannot silently scan your whole computer.
- The browser may ask you to grant access again when reopening the app.
- Undo history is held in memory for the current page session. Do not close or refresh the page before undoing.
- Google Drive connection is read-only. Drive organization features are not enabled yet.
- No automatic deletion, hidden background scanning, or AI upload of file contents.
- Keep a backup of important files before organizing them.

## Project structure

```
DrivePilotAI/
├── index.html
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT
