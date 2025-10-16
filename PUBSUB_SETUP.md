# Pub/Sub Setup for Gmail Push Notifications

## Error: User not authorized to perform this action

If you see "Error sending test message to Cloud PubSub... User not authorized to perform this action", you need to grant the Gmail API permission to publish to your Pub/Sub topic.

## Steps to Fix:

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com

### 2. Select Your Project
Select: **experiments-442603**

### 3. Navigate to Pub/Sub Topics
- Click on the left menu: **Pub/Sub**
- Click: **Topics**

### 4. Select Your Topic
- Find and click on: **signals-topic**

### 5. Go to Permissions Tab
- Click the **"PERMISSIONS"** tab at the top

### 6. Add Gmail API Service Account
- Click **"ADD PRINCIPAL"** button
- In the "New principals" field, enter exactly:
  ```
  gmail-api-push@system.gserviceaccount.com
  ```

### 7. Assign Publisher Role
- In the "Select a role" dropdown, search for: **Pub/Sub Publisher**
- Select: **Pub/Sub Publisher**

### 8. Save
- Click **SAVE**

### 9. Try Setup Again
```bash
source venv/bin/activate
python main.py setup
```

## Verification

After adding the permission, your topic's permissions should show:

```
Principal: gmail-api-push@system.gserviceaccount.com
Role: Pub/Sub Publisher
```

## Why This Is Needed

Gmail's push notification system works by:
1. Gmail detects a new email
2. Gmail publishes a notification message to your Pub/Sub topic
3. Pub/Sub forwards the notification to your webhook endpoint
4. Your application processes the notification and fetches the email

For step 2 to work, Gmail needs permission to publish to your topic. This is why we grant the `gmail-api-push@system.gserviceaccount.com` service account the "Pub/Sub Publisher" role.

## Troubleshooting

### "Permission denied" after adding principal
- Make sure you entered the exact email: `gmail-api-push@system.gserviceaccount.com`
- Check that the role is "Pub/Sub Publisher" (not Subscriber or Editor)
- Wait a few seconds for permissions to propagate

### "Topic not found"
- Verify your topic name in `.env` matches the actual topic name
- Format should be: `projects/experiments-442603/topics/signals-topic`

### Still getting 403 errors
- Ensure you're using the correct project: **experiments-442603**
- Verify the Gmail API is enabled in APIs & Services
- Check that your OAuth token has the gmail.readonly scope
