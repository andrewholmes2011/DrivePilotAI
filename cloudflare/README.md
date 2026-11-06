# DrivePilot AI Cloudflare backend

This backend provides per-Google-account organization history and an optional Cloudflare Workers AI classification endpoint.

## Deploy

1. Install Wrangler on a computer where Node.js is available.
2. From this directory run: npx wrangler d1 create drivepilot-ai.
3. Copy the returned database ID into wrangler.toml.
4. Run: npx wrangler d1 execute drivepilot-ai --remote --file=schema.sql.
5. Run: npx wrangler deploy.
6. Set the deployed Worker URL in the DrivePilot AI web app.

The Worker validates Google access tokens with Google's tokeninfo endpoint and keys history by verified Google email. It never stores Google access tokens.

## Important

- The browser must request OAuth scopes that permit account identity and Drive operations. Workspace administrators can block the OAuth app or Drive API.
- The AI endpoint sends document text to Cloudflare Workers AI. Do not enable it for school or sensitive documents unless account owner and school policy permit that processing.
- CORS is permissive for initial development. Before public deployment, replace the wildcard origin with the exact GitHub Pages origin.
- Review Cloudflare usage limits and model pricing/availability before enabling AI.
- This backend scaffold does not grant access to a school account or bypass administrator restrictions.
