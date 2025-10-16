# ngrok Setup Instructions

## Issue: SSL Certificate Errors

ngrok is experiencing SSL authentication errors. Here are the solutions:

## Option 1: Authenticate ngrok (Recommended)

1. **Sign up for ngrok** (free): https://dashboard.ngrok.com/signup
2. **Get your authtoken** from: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure ngrok:**
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
   ```
4. **Start ngrok:**
   ```bash
   ngrok http 5000
   ```

## Option 2: Use localtunnel (Alternative - No signup needed)

```bash
# Install localtunnel
npm install -g localtunnel

# Start tunnel
lt --port 5000
```

This will give you a URL like: `https://random-name-123.loca.lt/webhook`

## Option 3: Deploy to Cloud Run (Production)

Skip local tunneling entirely and deploy to Google Cloud Run:

```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal

# Build and deploy
gcloud builds submit --tag gcr.io/experiments-442603/gmail-signal
gcloud run deploy gmail-signal \
  --image gcr.io/experiments-442603/gmail-signal \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars="GMAIL_CLIENT_ID=YOUR_CLIENT_ID_HERE" \
  --set-env-vars="GMAIL_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE" \
  --set-env-vars="PUBSUB_TOPIC_NAME=projects/experiments-442603/topics/signals-topic" \
  --set-env-vars="MATHEMATRICKS_API_URL=https://mathematricks.fund/api/signals" \
  --set-env-vars="MATHEMATRICKS_PASSPHRASE=YOUR_PASSPHRASE_HERE" \
  --set-env-vars="STRATEGY_NAME=Gmail_Signal_Integration" \
  --set-env-vars="SIGNAL_IDENTIFIER=LESLIE_SIGNAL"
```

**Note:** You'll need to upload token.json as a secret separately.

## Quick Decision Matrix

- **Testing locally for a few hours:** Use localtunnel (no signup)
- **Testing for longer or repeatedly:** Authenticate ngrok (best local option)
- **Production deployment:** Use Cloud Run (recommended)

## Current Status

- ✅ Webhook server running on localhost:5000
- ✅ Health check passing
- ⚠️ ngrok has SSL errors (needs authentication)

Choose one of the options above to proceed.
