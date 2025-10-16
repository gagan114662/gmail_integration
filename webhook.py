import json
import base64
from flask import Flask, request, jsonify
from gmail_auth import GmailAuthenticator
from email_processor import EmailProcessor
from signal_extractor import SignalExtractor
from api_forwarder import APIForwarder
from config import Config

app = Flask(__name__)

# Initialize components
gmail_auth = GmailAuthenticator()
signal_extractor = SignalExtractor()
api_forwarder = APIForwarder()

# Global state to track history ID
last_history_id = None


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming Gmail push notifications from Cloud Pub/Sub

    Pub/Sub sends notifications in this format:
    {
        "message": {
            "data": base64-encoded-json,
            "messageId": "...",
            "publishTime": "..."
        }
    }
    """
    global last_history_id

    try:
        # Parse Pub/Sub message
        envelope = request.get_json()

        if not envelope:
            return jsonify({'error': 'No Pub/Sub message received'}), 400

        if 'message' not in envelope:
            return jsonify({'error': 'Invalid Pub/Sub message format'}), 400

        # Decode the message data
        pubsub_message = envelope['message']

        if 'data' in pubsub_message:
            message_data = base64.b64decode(pubsub_message['data']).decode('utf-8')
            notification = json.loads(message_data)
        else:
            notification = {}

        print(f"Received notification: {notification}")

        # Get Gmail service
        gmail_service = gmail_auth.get_service()
        email_processor = EmailProcessor(gmail_service)

        # Get email address from notification
        email_address = notification.get('emailAddress', 'me')
        history_id = notification.get('historyId')

        # Process new messages
        if history_id:
            if last_history_id:
                # Get history since last notification
                history = email_processor.get_history(last_history_id)

                for history_record in history:
                    if 'messagesAdded' in history_record:
                        for message_info in history_record['messagesAdded']:
                            message_id = message_info['message']['id']
                            process_message(message_id, email_processor)
            else:
                # First notification - just update history ID
                print(f"Initialized with history ID: {history_id}")

            last_history_id = history_id

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500


def process_message(message_id, email_processor):
    """
    Process a single email message

    Args:
        message_id: Gmail message ID
        email_processor: EmailProcessor instance
    """
    try:
        print(f"Processing message: {message_id}")

        # Fetch the message
        message = email_processor.get_message(message_id)

        if not message:
            print(f"Could not fetch message {message_id}")
            return

        # Check if it's a signal email
        if not email_processor.is_signal_email(message):
            print(f"Message {message_id} is not a signal email")
            return

        print(f"Signal email detected: {message_id}")

        # Get message details
        headers = email_processor.get_message_headers(message)
        subject = headers.get('Subject', '')
        body = email_processor.get_message_body(message)

        # Extract and format signal
        payload = signal_extractor.extract_and_format(body, subject, message_id)

        if not payload:
            print(f"Could not extract signal from message {message_id}")
            return

        print(f"Extracted signal: {payload['signalID']}")
        print(f"Signal data: {json.dumps(payload['signal'], indent=2)}")

        # Forward to API
        success, response = api_forwarder.send_signal(payload)

        if success:
            print(f"Successfully forwarded signal {payload['signalID']}")
        else:
            print(f"Failed to forward signal: {response}")

    except Exception as e:
        print(f"Error processing message {message_id}: {str(e)}")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Gmail Signal Integration'
    }), 200


@app.route('/test', methods=['POST'])
def test():
    """
    Test endpoint to manually trigger signal processing

    Send a POST request with:
    {
        "message_id": "gmail_message_id"
    }
    """
    try:
        data = request.get_json()
        message_id = data.get('message_id')

        if not message_id:
            return jsonify({'error': 'message_id required'}), 400

        gmail_service = gmail_auth.get_service()
        email_processor = EmailProcessor(gmail_service)

        process_message(message_id, email_processor)

        return jsonify({'status': 'processed', 'message_id': message_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def run_webhook_server():
    """Start the Flask webhook server"""
    print(f"Starting webhook server on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=False)


if __name__ == '__main__':
    run_webhook_server()
