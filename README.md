# DrivePilot AI

A browser-first Google Drive organizer for Windows 11 and Chromebooks.

Repository: https://github.com/andrewholmes2011/DrivePilotAI

## Implemented in this update

- Browser-only interface; no Chromebook Linux, Python, Node.js, or executable is required.
- Google OAuth sign-in using a Web client ID.
- Scans only files inside the Google Drive folder named "Unsorted", including nested folders.
- Applies the requested filename and file-type classification rules.
- Creates destination folders under "My Drive/Drive Organizer".
- Displays a selectable review list and requires confirmation before moving files.
- Moves files using Google Drive API parent-folder updates; supports undo during the current browser session.
- Optional Cloudflare D1 history and AI backend scaffold.

## Classification order

1. Filename begins with 6. → Drive Organizer/HHS 2025-2026/6th - Fenton APHG.
2. Filename contains CFF → Drive Organizer/CFF.
3. Filename contains AVID → Drive Organizer/Clausen 1st Hour.
4. Numbered copies ending in (1), (2), etc. → an Extra subfolder inside the matched category.
5. Images → Photos.
6. Google Workspace types → Docs, Sheets, Slides, Forms, Drawings, Maps, or Sites.
7. Common remaining file types → matching type folder; uncertain types → AI Review.

All destinations are under Drive Organizer. Only files inside Unsorted are eligible. The app does not delete files. A move updates Drive folder parents; it does not download and re-upload file contents.

## Google OAuth setup

1. In Google Cloud Console, create/select a project and enable the Google Drive API.
2. Configure the OAuth consent screen for the account audience.
3. Create an OAuth Client ID of type Web application.
4. Add the exact hosted site origin under Authorized JavaScript origins. For GitHub Pages this is normally https://andrewholmes2011.github.io (no path).
5. Enter the client ID in the app and save it.
6. Connect Google Drive and approve the requested drive scope.

The drive scope is needed because organizing requires write permission. Google may require OAuth app verification. A school Google Workspace administrator can block third-party OAuth apps or Drive API access. If blocked, ask the administrator or use an account where API access is authorized. This app does not bypass restrictions.

## GitHub Pages

In repository Settings → Pages, choose Deploy from a branch, branch main, folder /(root). Wait for the Pages deployment to finish.

## Optional Cloudflare backend

See cloudflare/README.md. The Worker requires a D1 database, GOOGLE_CLIENT_ID, and ALLOWED_ORIGINS. Set the deployed Worker URL in the app only after deployment.

## Privacy and limitations

- Classification currently uses filenames and MIME types, not document contents. The app does not automatically send document text to AI.
- The Worker has an optional AI endpoint, but the browser interface does not invoke it.
- Google OAuth access tokens remain in memory for the current page session; they are not stored in localStorage.
- The current interface does not yet connect the optional Worker history endpoint.
- Windows uses the same browser-based Drive API flow; native G:\My Drive filesystem integration and local Ollama companion are not implemented.
- Back up important files and review the selected destination list before confirming moves.
