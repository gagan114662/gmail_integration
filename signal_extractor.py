import re
import json
from datetime import datetime
from config import Config

class SignalExtractor:
    """Extract and parse signal data from email content"""

    def __init__(self):
        self.signal_identifier = Config.SIGNAL_IDENTIFIER

    def extract_signal(self, email_body, email_subject=""):
        """
        Extract signal data from email body

        Args:
            email_body: Email body text
            email_subject: Email subject line

        Returns:
            dict: Extracted signal data or None if no valid signal found
        """
        # Combine subject and body for processing
        full_content = f"{email_subject}\n{email_body}"

        # Check if this is a signal email
        if self.signal_identifier not in full_content:
            return None

        # Try to extract JSON signal
        json_signal = self._extract_json_signal(full_content)
        if json_signal:
            return json_signal

        # Try to extract structured text signal
        text_signal = self._extract_text_signal(full_content)
        if text_signal:
            return text_signal

        # Fallback: return entire content as signal
        return {
            "type": "raw",
            "content": full_content.strip()
        }

    def _extract_json_signal(self, content):
        """
        Try to extract JSON-formatted signal from content

        Args:
            content: Email content

        Returns:
            dict: Parsed JSON signal or None
        """
        # Look for JSON objects in the content
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'

        matches = re.finditer(json_pattern, content, re.DOTALL)

        for match in matches:
            try:
                signal_data = json.loads(match.group())
                # Validate that it looks like a trading signal
                if any(key in signal_data for key in ['ticker', 'symbol', 'action', 'trade', 'signal']):
                    return signal_data
            except json.JSONDecodeError:
                continue

        return None

    def _extract_text_signal(self, content):
        """
        Extract structured signal from plain text format

        Args:
            content: Email content

        Returns:
            dict: Parsed signal data or None
        """
        signal_data = {}

        # Common patterns for trading signals
        patterns = {
            'ticker': r'(?:ticker|symbol|stock)[\s:]+([A-Z]{1,5})',
            'action': r'(?:action|side|direction)[\s:]+(\w+)',
            'price': r'(?:price|entry)[\s:]+\$?([\d.]+)',
            'quantity': r'(?:quantity|qty|shares|size)[\s:]+(\d+)',
            'stop_loss': r'(?:stop[\s-]?loss|sl)[\s:]+\$?([\d.]+)',
            'take_profit': r'(?:take[\s-]?profit|tp|target)[\s:]+\$?([\d.]+)',
            'type': r'(?:type|order[\s-]?type)[\s:]+(\w+)',
        }

        # Extract fields using patterns
        for field, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                signal_data[field] = match.group(1).strip()

        # Only return if we found at least ticker and action
        if 'ticker' in signal_data or 'action' in signal_data:
            return signal_data

        return None

    def format_for_api(self, signal_data, message_id):
        """
        Format extracted signal for Mathematricks API

        Args:
            signal_data: Extracted signal data
            message_id: Gmail message ID

        Returns:
            dict: Formatted API payload
        """
        # Generate unique signal ID based on message ID and timestamp
        timestamp = int(datetime.now().timestamp())
        signal_id = f"{message_id}_{timestamp}"

        # Build API payload
        payload = {
            "strategy_name": Config.STRATEGY_NAME,
            "signal_sent_EPOCH": timestamp,
            "signalID": signal_id,
            "passphrase": Config.MATHEMATRICKS_PASSPHRASE,
            "signal": signal_data
        }

        return payload

    def extract_and_format(self, email_body, email_subject, message_id):
        """
        Extract signal and format for API in one step

        Args:
            email_body: Email body text
            email_subject: Email subject line
            message_id: Gmail message ID

        Returns:
            dict: Formatted API payload or None if no signal found
        """
        signal_data = self.extract_signal(email_body, email_subject)

        if not signal_data:
            return None

        return self.format_for_api(signal_data, message_id)
