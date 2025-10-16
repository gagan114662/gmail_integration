# Gmail Signal Integration

Real-time Gmail monitoring system that detects signal emails and forwards them to the Mathematricks API using Gmail Push Notifications (no polling).

## Features

- Real-time email monitoring via Gmail Push Notifications (Cloud Pub/Sub)
- Automatic signal detection and extraction
- Support for JSON and plain text signal formats
- Secure OAuth2 authentication for Gmail
- Automatic forwarding to Mathematricks API
- Plug-and-play configuration management

## Architecture

1. **Gmail API + Cloud Pub/Sub**: Receives instant push notifications when new emails arrive
2. **Flask Webhook**: Processes notifications and fetches email content
3. **Signal Detector**: Identifies emails containing signal data
4. **Signal Extractor**: Parses and extracts trading signal information
5. **API Forwarder**: Sends extracted signals to Mathematricks API

## Prerequisites

1. **Google Cloud Project** with Gmail API enabled
2. **Cloud Pub/Sub topic** configured for Gmail push notifications
3. **Gmail OAuth2 credentials** (Client ID and Secret)
4. **Mathematricks API passphrase**
5. **Python 3.8+**

## Installation

### 1. Clone or download this project

```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example configuration:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```bash
# Gmail API Configuration
GMAIL_CLIENT_ID=your_client_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_client_secret

# Google Cloud Pub/Sub Configuration
PUBSUB_TOPIC_NAME=projects/your-project-id/topics/gmail-notifications

# Mathematricks API Configuration
MATHEMATRICKS_PASSPHRASE=your_passphrase_here

# Optional: Customize these
STRATEGY_NAME=Gmail_Signal_Integration
SIGNAL_IDENTIFIER=SIGNAL
```

## Google Cloud Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Note your Project ID

### Step 2: Enable Gmail API

1. Navigate to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click "Enable"

### Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" as application type
4. Download the JSON file and save as `credentials.json` in the project directory
   - OR extract `client_id` and `client_secret` and add to `.env`

### Step 4: Set Up Cloud Pub/Sub

1. Navigate to "Pub/Sub" > "Topics"
2. Click "Create Topic"
3. Name it (e.g., `gmail-notifications`)
4. Click "Create"
5. Copy the full topic name (e.g., `projects/my-project/topics/gmail-notifications`)
6. Add it to `.env` as `PUBSUB_TOPIC_NAME`

### Step 5: Grant Gmail API Access to Pub/Sub Topic

1. In your Pub/Sub topic, click "Permissions"
2. Click "Add Principal"
3. Add: `gmail-api-push@system.gserviceaccount.com`
4. Grant role: "Pub/Sub Publisher"
5. Save

### Step 6: Create Pub/Sub Subscription

1. In your topic, click "Create Subscription"
2. Subscription ID: `gmail-webhook-subscription`
3. Delivery type: "Push"
4. Endpoint URL: Your webhook URL (e.g., `https://your-domain.com/webhook`)
5. Click "Create"

## Usage

### First-Time Setup

Run the setup command to authenticate and configure push notifications:

```bash
python main.py setup
```

This will:
1. Authenticate with Gmail (opens browser for OAuth)
2. Enable push notifications for your Gmail account
3. Test the connection to Mathematricks API

### Start the Webhook Server

```bash
python main.py start
```

The server will start on `http://0.0.0.0:5000` by default.

### Other Commands

```bash
# Only authenticate (useful for testing)
python main.py auth

# Test API connection
python main.py test-api

# Stop push notifications
python main.py stop
```

## Signal Format

The system supports multiple signal formats:

### JSON Format

```json
{
  "ticker": "AAPL",
  "action": "BUY",
  "price": 150.00,
  "quantity": 100,
  "stop_loss": 145.00,
  "take_profit": 160.00
}
```

### Plain Text Format

```
SIGNAL
Ticker: AAPL
Action: BUY
Price: $150.00
Quantity: 100
Stop Loss: $145.00
Take Profit: $160.00
```

Any email containing the signal identifier (default: "SIGNAL") will be processed and forwarded.

## Configuration Options

Edit `.env` to customize:

- `SIGNAL_IDENTIFIER`: Text to identify signal emails (default: "SIGNAL")
- `STRATEGY_NAME`: Strategy name sent to API (default: "Gmail_Signal_Integration")
- `FLASK_HOST`: Webhook server host (default: "0.0.0.0")
- `FLASK_PORT`: Webhook server port (default: 5000)

## Deployment

### Option 1: Local Development with ngrok

For testing, use ngrok to expose your local server:

```bash
# Start the webhook server
python main.py start

# In another terminal, expose it
ngrok http 5000
```

Use the ngrok URL as your Pub/Sub push endpoint.

### Option 2: Cloud Deployment

Deploy to a cloud provider:

- **Google Cloud Run**: Serverless container platform
- **AWS EC2/ECS**: Virtual machine or container service
- **Heroku**: Platform-as-a-service
- **DigitalOcean**: Virtual private server

Make sure your deployment:
1. Has a public HTTPS endpoint
2. Runs the Flask server (`python main.py start`)
3. Has all environment variables configured

## Troubleshooting

### Authentication Issues

```bash
# Re-authenticate
rm token.json
python main.py auth
```

### Push Notifications Not Working

1. Check Pub/Sub topic permissions
2. Verify subscription endpoint URL is accessible
3. Run `python main.py setup` again to reset

### API Connection Issues

```bash
# Test API connectivity
python main.py test-api
```

Check:
- Passphrase is correct
- Network connectivity
- API endpoint URL

### No Signals Being Detected

1. Verify emails contain the signal identifier (default: "SIGNAL")
2. Check Flask server logs for processing errors
3. Test with a manual message:

```bash
curl -X POST http://localhost:5000/test \
  -H "Content-Type: application/json" \
  -d '{"message_id": "YOUR_GMAIL_MESSAGE_ID"}'
```

## Project Structure

```
gmail_signal/
├── main.py                 # Main application entry point
├── config.py               # Configuration management
├── gmail_auth.py           # Gmail API authentication
├── email_processor.py      # Email fetching and parsing
├── signal_extractor.py     # Signal detection and extraction
├── api_forwarder.py        # Mathematricks API integration
├── webhook.py              # Flask webhook server
├── requirements.txt        # Python dependencies
├── .env.example            # Example configuration
├── .env                    # Your configuration (gitignored)
└── README.md               # This file
```

## API Reference

### Mathematricks API Payload

The system sends the following format to the API:

```json
{
  "strategy_name": "Gmail_Signal_Integration",
  "signal_sent_EPOCH": 1234567890,
  "signalID": "unique_signal_id",
  "passphrase": "your_passphrase",
  "signal": {
    // Extracted signal data
  }
}
```

## Security Notes

- Never commit `.env` or `credentials.json` files
- Keep your passphrase and OAuth credentials secure
- Use HTTPS for your webhook endpoint in production
- Regularly rotate your API credentials
- Monitor logs for unauthorized access

## Support

For issues with:
- **Gmail API**: See [Gmail API Documentation](https://developers.google.com/gmail/api)
- **Cloud Pub/Sub**: See [Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- **Mathematricks API**: Contact strategies@mathematricks.fund

## License

This project is provided as-is for use with the Mathematricks trading platform.
