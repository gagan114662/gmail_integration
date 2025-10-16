# Gmail Signal Integration - Complete Setup Guide

This guide will walk you through setting up the Gmail Signal Integration system for **vandan@mathematricks.fund** from start to finish.

## Quick Start Checklist

- [ ] Google Cloud Project created
- [ ] Gmail API enabled
- [ ] OAuth2 credentials obtained
- [ ] Cloud Pub/Sub topic created
- [ ] Pub/Sub permissions configured
- [ ] Python dependencies installed
- [ ] Environment variables configured
- [ ] Authentication completed
- [ ] Push notifications enabled
- [ ] Webhook server deployed
- [ ] System tested end-to-end

## Detailed Setup Instructions

### Part 1: Google Cloud Console Setup

#### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the project dropdown at the top
3. Click "New Project"
4. Enter project name: `gmail-signal-integration`
5. Click "Create"
6. Wait for project creation to complete
7. **Note your Project ID** (e.g., `gmail-signal-integration-123456`)

#### 1.2 Enable Gmail API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on "Gmail API"
4. Click "Enable"
5. Wait for API to be enabled

#### 1.3 Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. If prompted, configure OAuth consent screen first:
   - User Type: Select "Internal" (if available) or "External"
   - App name: `Gmail Signal Integration`
   - User support email: `vandan@mathematricks.fund`
   - Developer contact: `vandan@mathematricks.fund`
   - Click "Save and Continue"
   - Scopes: Click "Save and Continue" (we'll set this later)
   - Test users (if External): Add `vandan@mathematricks.fund`
   - Click "Save and Continue"
3. Go back to "Credentials" tab
4. Click "Create Credentials" > "OAuth client ID"
5. Application type: "Desktop app"
6. Name: `Gmail Signal Desktop Client`
7. Click "Create"
8. **Download the JSON file**
9. Save it as `credentials.json` in the project directory

**Alternative**: Extract these values and add to `.env`:
```
GMAIL_CLIENT_ID=xxxxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=xxxxx
```

#### 1.4 Set Up Cloud Pub/Sub

1. In the Google Cloud Console, go to "Pub/Sub" > "Topics"
2. Click "Create Topic"
3. Topic ID: `gmail-notifications`
4. Uncheck "Add a default subscription"
5. Click "Create"
6. **Copy the full topic name** shown at the top (e.g., `projects/gmail-signal-integration-123456/topics/gmail-notifications`)
7. Save this for your `.env` file

#### 1.5 Grant Gmail Permission to Pub/Sub

1. While viewing your `gmail-notifications` topic, click "Permissions" tab
2. Click "Add Principal"
3. New principal: `gmail-api-push@system.gserviceaccount.com`
4. Role: "Pub/Sub Publisher"
5. Click "Save"

### Part 2: Local Environment Setup

#### 2.1 Install Python Dependencies

```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal
pip install -r requirements.txt
```

#### 2.2 Configure Environment Variables

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your values:
```bash
# Gmail API Configuration
GMAIL_CLIENT_ID=your_client_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_client_secret

# Google Cloud Pub/Sub Configuration
PUBSUB_TOPIC_NAME=projects/gmail-signal-integration-123456/topics/gmail-notifications

# Mathematricks API Configuration
MATHEMATRICKS_PASSPHRASE=your_passphrase_here

# Strategy Configuration (optional customization)
STRATEGY_NAME=Gmail_Signal_Integration
SIGNAL_IDENTIFIER=SIGNAL
```

**Where to get each value:**
- `GMAIL_CLIENT_ID` & `GMAIL_CLIENT_SECRET`: From OAuth2 credentials (or credentials.json)
- `PUBSUB_TOPIC_NAME`: From Pub/Sub topic creation step
- `MATHEMATRICKS_PASSPHRASE`: Request from strategies@mathematricks.fund

### Part 3: Initial Authentication

#### 3.1 Authenticate with Gmail

```bash
python main.py auth
```

This will:
1. Open your default web browser
2. Ask you to sign in to **vandan@mathematricks.fund**
3. Grant permissions to the application
4. Save authentication token locally

**Important**: Make sure to sign in with `vandan@mathematricks.fund` account.

#### 3.2 Enable Push Notifications

```bash
python main.py setup
```

This will:
1. Authenticate (if not already done)
2. Register webhook with Gmail API
3. Test API connection
4. Display history ID and expiration time

**Expected output:**
```
=== Gmail Signal Integration Setup ===

Setting up Gmail authentication...
Authentication successful!

Setting up push notifications...
Push notifications enabled successfully!
History ID: 123456
Expiration: 1234567890000

Testing API connection...
Sending test signal to https://mathematricks.fund/api/signals
Signal TEST_1234567890 sent successfully
API connection test successful!

=== Setup Complete ===
```

### Part 4: Webhook Deployment

You need to deploy the webhook server to a publicly accessible endpoint. Choose one option:

#### Option A: Local Testing with ngrok (Recommended for initial testing)

1. Install ngrok: https://ngrok.com/download
2. Start the webhook server:
```bash
python main.py start
```
3. In another terminal, expose it:
```bash
ngrok http 5000
```
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
5. Continue to Part 5 to configure Pub/Sub subscription

#### Option B: Deploy to Google Cloud Run

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=8080

CMD ["python", "main.py", "start"]
```

2. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/gmail-signal
gcloud run deploy gmail-signal \
  --image gcr.io/YOUR-PROJECT-ID/gmail-signal \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

3. Note the service URL provided

#### Option C: Deploy to any VPS (DigitalOcean, AWS EC2, etc.)

1. SSH into your server
2. Clone/copy the project
3. Install dependencies
4. Configure `.env`
5. Set up systemd service or supervisor
6. Configure nginx/Apache as reverse proxy with SSL
7. Ensure HTTPS is enabled

### Part 5: Configure Pub/Sub Push Subscription

1. Go to Google Cloud Console > Pub/Sub > Topics
2. Click your `gmail-notifications` topic
3. Go to "Subscriptions" tab
4. Click "Create Subscription"
5. Subscription ID: `gmail-webhook-push`
6. Delivery type: **Push**
7. Endpoint URL: Your webhook URL + `/webhook`
   - Example: `https://abc123.ngrok.io/webhook`
   - Or: `https://your-domain.com/webhook`
8. Click "Create"

### Part 6: Testing the System

#### 6.1 Test API Connection

```bash
python main.py test-api
```

Expected output:
```
Testing API connection...
Sending test signal to https://mathematricks.fund/api/signals
Signal TEST_xxxxx sent successfully
API connection test successful!
```

#### 6.2 Test with Real Email

1. Send a test email to `vandan@mathematricks.fund` with this content:

```
Subject: Test SIGNAL

SIGNAL
Ticker: AAPL
Action: BUY
Price: $150.00
Quantity: 100
```

2. Check webhook server logs:
```bash
# Logs should show:
Received notification: {...}
Processing message: xxxxx
Signal email detected: xxxxx
Extracted signal: xxxxx
Successfully forwarded signal xxxxx
```

3. Verify signal was received by Mathematricks API

#### 6.3 Test Manual Processing

If push notifications aren't working, test directly:

```bash
# Get a message ID from Gmail
# Then test processing:
curl -X POST http://localhost:5000/test \
  -H "Content-Type: application/json" \
  -d '{"message_id": "YOUR_MESSAGE_ID"}'
```

### Part 7: Production Checklist

Before going to production:

- [ ] Webhook deployed with HTTPS
- [ ] `.env` file secured (not committed to git)
- [ ] Push notifications tested and working
- [ ] Signal detection tested with sample emails
- [ ] API forwarding tested and confirmed
- [ ] Monitoring/logging configured
- [ ] Error notifications set up
- [ ] System health checks in place
- [ ] Backup authentication tokens secured
- [ ] Documentation reviewed by team

### Part 8: Monitoring and Maintenance

#### Check System Health

```bash
curl http://localhost:5000/health
```

#### Monitor Logs

```bash
# If running in foreground
python main.py start

# If using systemd
journalctl -u gmail-signal -f

# If using Docker
docker logs -f gmail-signal
```

#### Renew Push Notifications

Gmail push notifications expire after 7 days. Re-run:

```bash
python main.py setup
```

Or set up a cron job:
```bash
# Renew every 6 days
0 0 */6 * * cd /path/to/project && python main.py setup
```

## Troubleshooting

### Issue: "Authentication failed"

**Solution:**
1. Check OAuth credentials are correct
2. Delete `token.json` and re-authenticate
3. Verify Gmail API is enabled in Cloud Console

### Issue: "Push notifications failed to enable"

**Solution:**
1. Verify Pub/Sub topic exists
2. Check `gmail-api-push@system.gserviceaccount.com` has Publisher role
3. Ensure topic name format is correct: `projects/PROJECT-ID/topics/TOPIC-NAME`

### Issue: "No notifications received"

**Solution:**
1. Check Pub/Sub subscription is configured correctly
2. Verify webhook URL is publicly accessible
3. Check subscription endpoint URL includes `/webhook`
4. Look at Pub/Sub metrics in Cloud Console
5. Check webhook server logs for errors

### Issue: "API forwarding failed"

**Solution:**
1. Verify passphrase is correct
2. Test API connection: `python main.py test-api`
3. Check network connectivity
4. Verify API endpoint URL is correct

### Issue: "Signals not being detected"

**Solution:**
1. Verify emails contain the signal identifier (default: "SIGNAL")
2. Check email format matches expected patterns
3. Test with manual processing endpoint
4. Review signal extraction logic in logs

## Support Contacts

- **Mathematricks API Issues**: strategies@mathematricks.fund
- **Gmail API Issues**: [Google Support](https://support.google.com/googleapi)
- **System Issues**: Check logs and troubleshooting section above

## Next Steps

After setup is complete:

1. Monitor the first few signals to ensure correct processing
2. Adjust `SIGNAL_IDENTIFIER` if needed
3. Customize signal extraction logic for your specific format
4. Set up alerts for system failures
5. Document any custom signal formats being used
6. Train team members on system operation

---

**Setup completed for vandan@mathematricks.fund**
