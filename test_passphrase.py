#!/usr/bin/env python3
"""
Test different passphrase formats to identify potential issues
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

def test_passphrase_variant(passphrase, description):
    """Test a passphrase variant"""
    api_url = "https://mathematricks.fund/api/signals"

    payload = {
        "strategy_name": "Gmail_Signal_Integration",
        "signal_sent_EPOCH": int(time.time()),
        "signalID": f"TEST_{int(time.time())}",
        "passphrase": passphrase,
        "signal": {
            "type": "test",
            "ticker": "TEST",
            "action": "BUY"
        }
    }

    print(f"\nTesting: {description}")
    print(f"Passphrase: '{passphrase}'")
    print(f"Length: {len(passphrase)}")

    try:
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✓ SUCCESS!")
            return True
        else:
            print("✗ Failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Read current passphrase from .env
current_passphrase = os.getenv('MATHEMATRICKS_PASSPHRASE', '')

print("=" * 60)
print("Passphrase Format Testing")
print("=" * 60)

print(f"\nOriginal from .env: '{current_passphrase}'")
print(f"Length: {len(current_passphrase)}")
has_quotes = '"' in current_passphrase
print(f"Contains quotes: {has_quotes}")

# Test variations
variants = [
    (current_passphrase, "Original from .env"),
    (current_passphrase.strip(), "Trimmed whitespace"),
    (current_passphrase.strip('"'), "Without surrounding quotes"),
    (current_passphrase.strip("'"), "Without single quotes"),
    (current_passphrase.replace('"', ''), "All quotes removed"),
]

print("\n" + "=" * 60)
print("Testing Variants")
print("=" * 60)

success = False
for passphrase, desc in variants:
    if test_passphrase_variant(passphrase, desc):
        success = True
        break
    time.sleep(1)  # Brief delay between requests

if not success:
    print("\n" + "=" * 60)
    print("All variants failed")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Contact strategies@mathematricks.fund")
    print("2. Verify the passphrase for strategy: 'Gmail_Signal_Integration'")
    print("3. Ask specifically if there are:")
    print("   - Special characters")
    print("   - Case sensitivity requirements")
    print("   - Whitespace at beginning/end")
    print("   - Account-specific passphrase needed")
    print("\n4. Once confirmed, update .env:")
    print("   MATHEMATRICKS_PASSPHRASE=correct_passphrase_here")
    print("\n5. Test again:")
    print("   python main.py test-api")
