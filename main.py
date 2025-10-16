#!/usr/bin/env python3
"""
Gmail Signal Integration - Main Application

This application monitors Gmail for signal emails and forwards them to the Mathematricks API.
"""

import sys
import argparse
from gmail_auth import GmailAuthenticator
from api_forwarder import APIForwarder
from webhook import run_webhook_server
from config import Config


def setup_authentication():
    """Set up Gmail API authentication"""
    print("Setting up Gmail authentication...")

    try:
        gmail_auth = GmailAuthenticator()
        service = gmail_auth.authenticate()
        print("Authentication successful!")
        return service
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)


def setup_push_notifications():
    """Enable Gmail push notifications"""
    print("Setting up push notifications...")

    if not Config.PUBSUB_TOPIC_NAME:
        print("Error: PUBSUB_TOPIC_NAME not set in configuration")
        print("Please set up a Google Cloud Pub/Sub topic and configure it in .env")
        sys.exit(1)

    try:
        gmail_auth = GmailAuthenticator()
        gmail_auth.authenticate()
        watch_response = gmail_auth.setup_push_notifications(Config.PUBSUB_TOPIC_NAME)
        print(f"Push notifications enabled successfully!")
        print(f"History ID: {watch_response.get('historyId')}")
        print(f"Expiration: {watch_response.get('expiration')}")
    except Exception as e:
        print(f"Failed to set up push notifications: {e}")
        sys.exit(1)


def stop_push_notifications():
    """Stop Gmail push notifications"""
    print("Stopping push notifications...")

    try:
        gmail_auth = GmailAuthenticator()
        gmail_auth.authenticate()
        gmail_auth.stop_push_notifications()
        print("Push notifications stopped successfully")
    except Exception as e:
        print(f"Failed to stop push notifications: {e}")
        sys.exit(1)


def test_api_connection():
    """Test connection to Mathematricks API"""
    print("Testing API connection...")

    try:
        api_forwarder = APIForwarder()
        success, response = api_forwarder.send_test_signal()

        if success:
            print("API connection test successful!")
            print(f"Response: {response}")
        else:
            print("API connection test failed!")
            print(f"Error: {response}")
            sys.exit(1)
    except Exception as e:
        print(f"API test failed: {e}")
        sys.exit(1)


def start_webhook():
    """Start the webhook server"""
    print("Starting webhook server...")
    run_webhook_server()


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description='Gmail Signal Integration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First-time setup
  python main.py setup

  # Start the webhook server
  python main.py start

  # Test API connection
  python main.py test-api

  # Stop push notifications
  python main.py stop
        """
    )

    parser.add_argument(
        'command',
        choices=['setup', 'start', 'test-api', 'stop', 'auth'],
        help='Command to execute'
    )

    args = parser.parse_args()

    # Validate configuration (except for auth command)
    if args.command != 'auth':
        try:
            Config.validate()
        except ValueError as e:
            print(f"Configuration error: {e}")
            print("\nPlease copy .env.example to .env and fill in the required values")
            sys.exit(1)

    # Execute command
    if args.command == 'auth':
        setup_authentication()

    elif args.command == 'setup':
        print("=== Gmail Signal Integration Setup ===\n")
        setup_authentication()
        print("\n")
        setup_push_notifications()
        print("\n")
        test_api_connection()
        print("\n=== Setup Complete ===")
        print("You can now start the webhook server with: python main.py start")

    elif args.command == 'start':
        print("=== Gmail Signal Integration ===")
        print(f"Strategy: {Config.STRATEGY_NAME}")
        print(f"Signal Identifier: {Config.SIGNAL_IDENTIFIER}")
        print(f"API URL: {Config.MATHEMATRICKS_API_URL}\n")
        start_webhook()

    elif args.command == 'test-api':
        test_api_connection()

    elif args.command == 'stop':
        stop_push_notifications()


if __name__ == '__main__':
    main()
