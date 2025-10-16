# Gmail Signal Integration - Deployment Guide

## Current Status

✓ Gmail authentication configured
✓ Push notifications enabled
✓ Pub/Sub topic permissions set
⚠️ API passphrase needs verification

## Next Steps

### Step 1: Configure Pub/Sub Push Subscription

You need to create a Pub/Sub subscription that forwards notifications to your webhook endpoint.

#### Option A: Using ngrok for Local Testing (Recommended First)

1. **Start the webhook server locally:**
   ```bash
   source venv/bin/activate
   python main.py start
   ```

2. **In another terminal, expose it with ngrok:**
   ```bash
   # Install ngrok from https://ngrok.com if not already installed
   ngrok http 5000
   ```

3. **Copy the ngrok HTTPS URL** (e.g., `https://abc123.ngrok.io`)

4. **Create Pub/Sub subscription:**
   - Go to: [Google Cloud Console](https://console.cloud.google.com)
   - Navigate to: **Pub/Sub > Topics**
   - Click on: **signals-topic**
   - Go to **"SUBSCRIPTIONS"** tab
   - Click **"CREATE SUBSCRIPTION"**
   - Subscription ID: `gmail-webhook-subscription`
   - Delivery type: **Push**
   - Endpoint URL: `https://YOUR-NGROK-URL.ngrok.io/webhook`
   - Click **"CREATE"**

5. **Test by sending an email to gagan@getfoolish.com** with "LESLIE_SIGNAL" in the subject or body

6. **Check the webhook logs** for incoming notifications

#### Option B: Deploy to Cloud Run (Production)

1. **Create a Dockerfile:**
   Already created in the project root:
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

2. **Build and deploy to Google Cloud Run:**
   ```bash
   # Authenticate with gcloud
   gcloud auth login

   # Set project
   gcloud config set project experiments-442603

   # Build container
   gcloud builds submit --tag gcr.io/experiments-442603/gmail-signal

   # Deploy to Cloud Run
   gcloud run deploy gmail-signal \
     --image gcr.io/experiments-442603/gmail-signal \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

3. **Set environment variables in Cloud Run:**
   - Go to Cloud Run service
   - Click "EDIT & DEPLOY NEW REVISION"
   - Go to "Variables & Secrets" tab
   - Add all variables from `.env`:
     - GMAIL_CLIENT_ID
     - GMAIL_CLIENT_SECRET
     - PUBSUB_TOPIC_NAME
     - MATHEMATRICKS_API_URL
     - MATHEMATRICKS_PASSPHRASE
     - STRATEGY_NAME
     - SIGNAL_IDENTIFIER

4. **Upload token.json as a secret:**
   ```bash
   # Create secret
   gcloud secrets create gmail-token --data-file=token.json

   # Grant Cloud Run access
   gcloud secrets add-iam-policy-binding gmail-token \
     --member=serviceAccount:YOUR-SERVICE-ACCOUNT@experiments-442603.iam.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor
   ```

5. **Get the Cloud Run service URL** and use it for the Pub/Sub subscription endpoint

#### Option C: Deploy to Any Server (VPS, EC2, etc.)

1. **Copy project to server**
2. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure .env file** with your credentials

4. **Copy token.json** to the server

5. **Set up as a systemd service:**
   Create `/etc/systemd/system/gmail-signal.service`:
   ```ini
   [Unit]
   Description=Gmail Signal Integration
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/gmail_signal
   ExecStart=/path/to/gmail_signal/venv/bin/python main.py start
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Enable and start:**
   ```bash
   sudo systemctl enable gmail-signal
   sudo systemctl start gmail-signal
   ```

7. **Set up nginx reverse proxy with SSL:**
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       location /webhook {
           proxy_pass http://localhost:5000/webhook;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /health {
           proxy_pass http://localhost:5000/health;
       }
   }
   ```

### Step 2: Verify Mathematricks API Passphrase

Contact strategies@mathematricks.fund to verify your passphrase. The current passphrase in `.env` is being rejected by the API.

Once you have the correct passphrase, update `.env`:
```bash
MATHEMATRICKS_PASSPHRASE=your_correct_passphrase_here
```

Test the connection:
```bash
source venv/bin/activate
python main.py test-api
```

### Step 3: Test End-to-End

1. **Ensure webhook server is running**
2. **Send a test email** to `gagan@getfoolish.com`:
   ```
   Subject: Test LESLIE_SIGNAL

   LESLIE_SIGNAL
   Ticker: AAPL
   Action: BUY
   Price: $150.00
   Quantity: 100
   ```

3. **Check webhook logs** for:
   - Notification received
   - Signal detected
   - Signal forwarded to API

4. **Verify signal in Mathematricks system**

## Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

### Manual Message Processing
```bash
curl -X POST http://localhost:5000/test \
  -H "Content-Type: application/json" \
  -d '{"message_id": "GMAIL_MESSAGE_ID"}'
```

### View Logs
If running locally:
```bash
# Logs appear in the terminal running main.py start
```

If using systemd:
```bash
sudo journalctl -u gmail-signal -f
```

If using Cloud Run:
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

## Renewing Push Notifications

Gmail push notifications expire after 7 days. To renew:

```bash
source venv/bin/activate
python main.py setup
```

Set up a cron job to auto-renew every 6 days:
```bash
0 0 */6 * * cd /path/to/gmail_signal && source venv/bin/activate && python main.py setup
```

## Troubleshooting

### No notifications received
1. Check Pub/Sub subscription is configured correctly
2. Verify webhook endpoint is publicly accessible
3. Check subscription metrics in Google Cloud Console
4. Look at Pub/Sub undelivered messages

### Signals not detected
1. Verify email contains "LESLIE_SIGNAL"
2. Check signal extraction logic in logs
3. Test manual processing with `/test` endpoint

### API forwarding fails
1. Verify passphrase is correct
2. Check network connectivity
3. Review API response in logs

## Production Checklist

- [ ] Webhook deployed with HTTPS
- [ ] Pub/Sub subscription configured
- [ ] Environment variables secured
- [ ] Correct Mathematricks passphrase verified
- [ ] Push notifications tested
- [ ] Signal detection tested
- [ ] API forwarding tested
- [ ] Monitoring/alerting configured
- [ ] Auto-renewal cron job set up
- [ ] Backup strategy for token.json
- [ ] Documentation reviewed

## Security Notes

- Never commit `.env` or `token.json` to git
- Use HTTPS for webhook endpoint in production
- Regularly rotate OAuth credentials
- Monitor logs for unauthorized access
- Keep dependencies updated
