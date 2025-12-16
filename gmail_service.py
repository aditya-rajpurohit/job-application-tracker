from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Read-only access to Gmail
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_service(account_label: str = "default") -> Any:
    """
    Build and return an authorized Gmail API service instance.

    - `account_label` is used to separate tokens for different accounts.
      Example: "personal", "university", "work"
    - Expects 'credentials.json' in the project root.
    """
    creds: Optional[Credentials] = None
    token_path = f"token_{account_label}.json"
    credentials_path = "credentials.json"

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "credentials.json not found. "
            "Download it from Google Cloud Console and place it in the project root."
        )

    # token_<account_label>.json stores this account's access and refresh tokens
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no valid credentials, let the user log in via the browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"[{account_label}] Refreshing expired token...")
            creds.refresh(Request())
        else:
            print(f"[{account_label}] No valid token found. Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
            print(f"[{account_label}] Saved new token to {token_path}")

    service = build("gmail", "v1", credentials=creds)
    return service


def list_all_messages(
    service: Any,
    user_id: str = "me",
    query: str = "",
    max_per_page: int = 500,
) -> List[Dict[str, Any]]:
    """
    Fetch all messages matching the Gmail search query.

    Returns a list of objects like: {"id": "...", "threadId": "..."}
    """
    messages: List[Dict[str, Any]] = []
    next_page_token: Optional[str] = None

    while True:
        response = (
            service.users()
            .messages()
            .list(
                userId=user_id,
                q=query,
                pageToken=next_page_token,
                maxResults=max_per_page,
            )
            .execute()
        )

        msgs = response.get("messages", [])
        messages.extend(msgs)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return messages


def get_message_metadata(
    service: Any,
    message_id: str,
    user_id: str = "me",
    metadata_headers: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """
    Fetch metadata for a single message.
    """
    if metadata_headers is None:
        metadata_headers = ["Subject"]

    msg = (
        service.users()
        .messages()
        .get(
            userId=user_id,
            id=message_id,
            format="metadata",
            metadataHeaders=metadata_headers,
        )
        .execute()
    )
    return msg