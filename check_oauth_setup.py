#!/usr/bin/env python3
"""
OAuth Setup Checker - Diagnose OAuth configuration issues
"""

import os
from config import Config

print("=" * 60)
print("Gmail Signal Integration - OAuth Setup Checker")
print("=" * 60)
print()

# Check environment variables
print("1. Checking Environment Variables:")
print("-" * 60)

if Config.GMAIL_CLIENT_ID:
    print(f"✓ GMAIL_CLIENT_ID: {Config.GMAIL_CLIENT_ID[:20]}...")
else:
    print("✗ GMAIL_CLIENT_ID: NOT SET")

if Config.GMAIL_CLIENT_SECRET:
    print(f"✓ GMAIL_CLIENT_SECRET: {Config.GMAIL_CLIENT_SECRET[:10]}...")
else:
    print("✗ GMAIL_CLIENT_SECRET: NOT SET")

print()

# Check for credentials.json
print("2. Checking credentials.json:")
print("-" * 60)

if os.path.exists('credentials.json'):
    print("✓ credentials.json file found")
    import json
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
        if 'installed' in creds:
            print(f"  Client ID: {creds['installed'].get('client_id', 'N/A')[:30]}...")
        elif 'web' in creds:
            print(f"  Client ID: {creds['web'].get('client_id', 'N/A')[:30]}...")
else:
    print("✗ credentials.json file NOT found")

print()

# Check token
print("3. Checking Existing Token:")
print("-" * 60)

if os.path.exists('token.json'):
    print("✓ token.json file found (previously authenticated)")
    print("  To re-authenticate, delete this file: rm token.json")
else:
    print("○ token.json file NOT found (need to authenticate)")

print()

# Configuration summary
print("4. OAuth Configuration Status:")
print("-" * 60)

if Config.GMAIL_CLIENT_ID and Config.GMAIL_CLIENT_SECRET:
    print("✓ OAuth credentials configured via environment variables")
    print()
    print("If you're getting 'Access blocked' errors:")
    print()
    print("  1. Go to: https://console.cloud.google.com")
    print("  2. Navigate to: APIs & Services > OAuth consent screen")
    print("  3. Check 'Publishing status' - should be 'Testing' or 'In Production'")
    print("  4. If 'Testing', add your Gmail address to 'Test users':")
    print("     - Click 'Add Users'")
    print("     - Add: gagan@getfoolish.com")
    print("     - Save")
    print()
    print("  5. Verify these scopes are configured:")
    print("     - https://www.googleapis.com/auth/gmail.readonly")
    print()
    print("  6. Try authentication again:")
    print("     python main.py auth")
    print()
elif os.path.exists('credentials.json'):
    print("✓ OAuth credentials configured via credentials.json")
    print()
    print("Same troubleshooting steps apply (see above)")
else:
    print("✗ No OAuth credentials found")
    print()
    print("Please configure OAuth credentials:")
    print("  Option A: Set environment variables in .env")
    print("  Option B: Download credentials.json from Google Cloud Console")

print()
print("=" * 60)
print("Next Steps:")
print("=" * 60)
print()
print("After fixing OAuth consent screen configuration:")
print("  python main.py auth")
print()
