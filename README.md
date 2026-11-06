# DrivePilot AI

A cross-platform Google Drive organizer for Windows 11 and Chromebook.

Repository: https://github.com/andrewholmes2011/DrivePilotAI

## Target architecture

- **Chromebook:** browser-only application using Google OAuth and the Google Drive API. No Linux, Python, or Chromebook installation is required.
- **Windows 11:** browser interface plus a local companion for access to Google Drive for desktop at G:\My Drive.
- **Hybrid AI:** deterministic rules first; optional local AI on Windows; optional Cloudflare Workers AI when explicitly enabled and permitted.
- **Cloud history:** Cloudflare Worker + D1, partitioned by the verified Google account email.
- **Safety:** scan and classify first; show a review queue; require explicit approval before moving; never delete files automatically.

## Existing classification rules

1. Filename starts with 6. -> HHS 2025-2026 / 6th - Fenton APHG.
2. Filename contains CFF -> CFF.
3. Filename contains AVID -> Clausen 1st Hour.
4. Images -> Photos.
5. Google file types -> Sites, Docs, Sheets, Slides, Forms, Drawings, Maps.
6. Remaining files -> content-based AI suggestion or AI Review.

All destination folders belong inside Drive Organizer. Numbered copies such as (1), (2) should be routed into an Extra subfolder.

## Current repository status

The root index.html is the earlier browser prototype. It supports local folder scanning and local moves with confirmation, plus metadata-only Google Drive scanning. **Its Google Drive connection is read-only; it does not yet move cloud Drive files or perform document-content AI classification.**

The cloud backend foundation is in cloudflare/:
- worker.js: Google-token-validated history endpoints and optional Workers AI classification endpoint.
- schema.sql: D1 history table.
- wrangler.toml: deployment template.
- README.md: backend deployment notes.

The Cloudflare backend is a scaffold and must be deployed/configured before cloud history or cloud AI can be used. The browser UI still needs to be connected to these endpoints.

## Chromebook constraints

The Chromebook edition is browser-only. It does not depend on Linux, Python, Node.js, or a local executable. It requires:
- A supported Chrome browser and HTTPS hosting.
- A Google OAuth client ID.
- Google Drive API access permitted by the Workspace administrator.
- OAuth scopes approved by the account owner and administrator.

If the school blocks third-party OAuth or Drive API access, DrivePilot AI cannot bypass that restriction. Use an account and files for which you have authorization.

## Privacy and AI

- Local rules and local file parsing should run on-device where possible.
- Local Windows AI can be an optional Ollama integration; it is not available on a Chromebook without Linux.
- Cloud AI sends the selected document text to Cloudflare Workers AI. Keep it disabled for school or sensitive documents unless permitted.
- Never put provider API secrets in browser JavaScript or a public GitHub repository.
- Do not send files to AI automatically. Require user opt-in and show what content will be transmitted.

## Deployment

### GitHub Pages

1. Open repository Settings -> Pages.
2. Select Deploy from a branch.
3. Select main and /(root).
4. Save and wait for deployment.

### Cloudflare backend

Follow cloudflare/README.md. Replace the placeholder D1 database ID in wrangler.toml, apply schema.sql, deploy the Worker, and configure the exact app origin for CORS before public use.

## Important

The project is under active development. Do not treat the current browser prototype as a completed Google Drive cloud organizer. Back up important files and review every proposed move before approving it.
