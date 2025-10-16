# OAuth Redirect URI Configuration

## Error: redirect_uri_mismatch

If you see "Error 400: redirect_uri_mismatch", you need to configure the authorized redirect URIs in Google Cloud Console.

## Steps to Fix:

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com

### 2. Select Your Project
Select: **experiments-442603**

### 3. Navigate to Credentials
- Click on the left menu: **APIs & Services**
- Click: **Credentials**

### 4. Edit OAuth 2.0 Client ID
- Find your OAuth 2.0 Client ID in the list
- Client ID: `257847153861-8b2ln56q7d0dcfer0jaq703jo7cgis9a.apps.googleusercontent.com`
- Click on it to edit

### 5. Add Authorized Redirect URIs
Under **Authorized redirect URIs**, click **"+ ADD URI"** and add these four URIs:

```
http://localhost:8080/
http://localhost:8080
http://localhost/
http://localhost
```

**Important:** Add all four variations to ensure compatibility

### 6. Save
Click **SAVE** at the bottom of the page

### 7. Try Authentication Again
```bash
source venv/bin/activate
python main.py auth
```

## Screenshot Reference
Your OAuth client configuration should look like this:

```
Authorized redirect URIs:
  http://localhost:8080/
  http://localhost:8080
  http://localhost/
  http://localhost
```

## Why This Happens
Desktop applications use OAuth with a local redirect to `http://localhost` on a specific port. Google requires these URIs to be explicitly authorized for security reasons.

## After Adding the URIs
The authentication flow will:
1. Open your browser
2. Ask you to sign in with your Google account (gagan@getfoolish.com)
3. Show permission request
4. Redirect back to localhost:8080
5. Save the authentication token locally

You'll only need to do this once. The token will be saved in `token.json` for future use.
