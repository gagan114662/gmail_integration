import requests
import json
from config import Config

class APIForwarder:
    """Forward signals to the Mathematricks API"""

    def __init__(self):
        self.api_url = Config.MATHEMATRICKS_API_URL

    def send_signal(self, payload):
        """
        Send signal to Mathematricks API

        Args:
            payload: Formatted signal payload

        Returns:
            tuple: (success: bool, response: dict)
        """
        try:
            # Validate payload
            required_fields = ['strategy_name', 'signal_sent_EPOCH', 'signalID', 'passphrase', 'signal']
            missing_fields = [field for field in required_fields if field not in payload]

            if missing_fields:
                return False, {
                    'error': f"Missing required fields: {', '.join(missing_fields)}"
                }

            # Send POST request
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            # Check response
            if response.status_code == 200:
                print(f"Signal {payload['signalID']} sent successfully")
                return True, {
                    'status': 'success',
                    'signal_id': payload['signalID'],
                    'response': response.text
                }
            else:
                error_msg = f"API returned status code {response.status_code}: {response.text}"
                print(f"Error sending signal: {error_msg}")
                return False, {
                    'error': error_msg,
                    'status_code': response.status_code
                }

        except requests.exceptions.Timeout:
            error_msg = "Request timed out"
            print(f"Error sending signal: {error_msg}")
            return False, {'error': error_msg}

        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"Error sending signal: {error_msg}")
            return False, {'error': error_msg}

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"Error sending signal: {error_msg}")
            return False, {'error': error_msg}

    def send_test_signal(self):
        """
        Send a test signal to verify API connectivity

        Returns:
            tuple: (success: bool, response: dict)
        """
        import time

        test_payload = {
            "strategy_name": Config.STRATEGY_NAME,
            "signal_sent_EPOCH": int(time.time()),
            "signalID": f"TEST_{int(time.time())}",
            "passphrase": Config.MATHEMATRICKS_PASSPHRASE,
            "signal": {
                "type": "test",
                "ticker": "TEST",
                "action": "BUY",
                "note": "Test signal from Gmail Signal Integration"
            }
        }

        print(f"Sending test signal to {self.api_url}")
        print(f"Payload: {json.dumps(test_payload, indent=2)}")
        return self.send_signal(test_payload)
