# DrivePilot AI Cloudflare backend

Optional Cloudflare Worker service for shared organization history and opt-in Workers AI classification.

## Setup

1. Run `npx wrangler d1 create drivepilot-ai` from this directory.
2. Copy the returned database ID into `wrangler.toml`.
3. Run `npx wrangler d1 execute drivepilot-ai --remote --file=schema.sql`.
4. Configure Worker variables:
   - `GOOGLE_CLIENT_ID`: the same OAuth Web client ID used by the browser.
   - `ALLOWED_ORIGINS`: exact site origin(s), comma-separated, such as `https://andrewholmes2011.github.io`.
5. Run `npx wrangler deploy`.

The Worker checks Google access tokens with Google's tokeninfo endpoint, validates the OAuth audience when `GOOGLE_CLIENT_ID` is configured, and partitions history by verified Google email. It does not persist access tokens.

## Notes

- The browser requires the Google Drive `drive` scope to move files. Google verification or Workspace administrator approval may be required.
- Never put a Google client secret in browser code or this repository.
- The history endpoint stores file metadata and action details, not file contents.
- The AI endpoint sends submitted text to Cloudflare Workers AI. The current browser interface does not call it automatically.
- CORS allows only origins configured in `ALLOWED_ORIGINS`.
- This service does not bypass school account restrictions.
