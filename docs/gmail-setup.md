# Gmail Setup

MailFlow Parser uses the Gmail API to fetch messages that match a configurable query.

## Scope

```text
https://www.googleapis.com/auth/gmail.readonly
```

The application only reads messages. It does not send, modify, delete, or mark emails.

## Local Setup

1. Create a Google Cloud project.
2. Enable the Gmail API.
3. Configure OAuth consent screen.
4. Add your Gmail account as a test user.
5. Create OAuth credentials for a desktop app.
6. Save the downloaded file as `credentials.json`.
7. Run `POST /process/gmail` once to generate `token.json`.

## Production Setup

For hosted environments, use environment variables:

```env
GMAIL_CREDENTIALS_JSON={...}
GMAIL_TOKEN_JSON={...}
```

These values should contain the full JSON content from your local credential and token files.

## Query Examples

```env
GMAIL_QUERY=subject:Pedido newer_than:7d
```

```env
GMAIL_QUERY=from:client@example.com newer_than:30d
```

```env
GMAIL_QUERY=subject:Pedido is:unread
```

## Security Notes

- Treat `token.json`, `credentials.json`, `GMAIL_CREDENTIALS_JSON`, and `GMAIL_TOKEN_JSON` as secrets.
- If a token is exposed, revoke it in your Google account and generate a new one.
- Keep the OAuth app in testing mode if this is only for portfolio/demo usage.
