"""Optional read-only Google Drive API access.

Create a Desktop OAuth client in Google Cloud Console, download its JSON file,
and place it at credentials/client_secret.json. School administrators may
restrict OAuth/API access; this app does not bypass those restrictions.
"""
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def connect_and_list(max_results=500):
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError as exc:
        raise RuntimeError("Install dependencies first: run setup.bat") from exc

    credential_file = Path("credentials/client_secret.json")
    token_file = Path("credentials/token.json")
    if not credential_file.exists():
        raise FileNotFoundError(
            "OAuth client file not found. See README.md for setup instructions."
        )

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(credential_file), SCOPES)
        creds = flow.run_local_server(port=0)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    response = service.files().list(
        pageSize=min(max_results, 1000),
        fields="files(id,name,mimeType,size,modifiedTime,webViewLink),nextPageToken",
        orderBy="name"
    ).execute()
    return response.get("files", [])
