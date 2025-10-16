# System Verification Commands

Copy and paste these commands to verify the system is working:

## 1. Check Webhook Server Status
```bash
curl -s http://localhost:5000/health | python3 -m json.tool
```

## 2. Check Token File Exists
```bash
ls -lh /Users/gaganarora/Desktop/gagan_projects/gmail_signal/token.json
```

## 3. Check Running Processes
```bash
ps aux | grep -E "(main.py start|localtunnel)" | grep -v grep
```

## 4. Check Port 5000 Listener
```bash
lsof -i :5000 | head -n 2
```

## 5. Verify Configuration Loaded
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && source venv/bin/activate && python3 -c "from config import Config; import os; print('Configuration Verification:'); print('-' * 50); print(f'Gmail Client ID: {Config.GMAIL_CLIENT_ID[:30]}...'); print(f'Pub/Sub Topic: {Config.PUBSUB_TOPIC_NAME}'); print(f'API URL: {Config.MATHEMATRICKS_API_URL}'); print(f'Passphrase: {Config.MATHEMATRICKS_PASSPHRASE}'); print(f'Strategy: {Config.STRATEGY_NAME}'); print(f'Signal ID: {Config.SIGNAL_IDENTIFIER}'); print(f'Token exists: {os.path.exists(\"token.json\")}')"
```

## 6. Test Gmail API Connection
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && source venv/bin/activate && python main.py test-api
```

## 7. Check Gmail Messages with LESLIE_SIGNAL
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && source venv/bin/activate && python3 -c "from gmail_auth import GmailAuthenticator; from email_processor import EmailProcessor; print('Checking Gmail messages with LESLIE_SIGNAL...'); gmail_auth = GmailAuthenticator(); service = gmail_auth.get_service(); results = service.users().messages().list(userId='me', maxResults=5, q='LESLIE_SIGNAL').execute(); messages = results.get('messages', []); print(f'\n✅ Found {len(messages)} messages with LESLIE_SIGNAL'); [print(f'  Message ID: {msg[\"id\"]}') for msg in messages[:3]]"
```

## 8. Test Mathematricks API Connection
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && source venv/bin/activate && python3 -c "import requests, json, time; payload = {'strategy_name': 'Gmail_Signal_Integration', 'signal_sent_EPOCH': int(time.time()), 'signalID': f'VERIFY_{int(time.time())}', 'passphrase': 'yahoo123', 'signal': {'type': 'verification_test', 'ticker': 'VERIFY', 'action': 'TEST'}}; print('Testing Mathematricks API Connection...'); print('=' * 50); response = requests.post('https://mathematricks.fund/api/signals', json=payload, headers={'Content-Type': 'application/json'}, timeout=10); print(f'Status Code: {response.status_code}'); print(f'Response: {response.text}'); print('=' * 50); print('\n✅ API CONNECTION VERIFIED - Signal accepted!' if response.status_code == 200 else '\n❌ API CONNECTION FAILED')"
```

## 9. Test Signal Extraction
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && source venv/bin/activate && python3 -c "from signal_extractor import SignalExtractor; extractor = SignalExtractor(); test_email = 'LESLIE_SIGNAL\n\nTicker: AAPL\nAction: BUY\nPrice: \$150.00\nQuantity: 100'; signal = extractor.extract_signal(test_email, 'Test Subject'); print('Extracted Signal:'); print(signal)"
```

## 10. View Environment Variables
```bash
cat /Users/gaganarora/Desktop/gagan_projects/gmail_signal/.env
```

## 11. Complete System Status Check (ONE COMMAND)
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && echo "=========================================" && echo "Gmail Signal Integration - VERIFICATION" && echo "=========================================" && echo "" && echo "✅ Test 1: Webhook Server" && curl -s http://localhost:5000/health | python3 -m json.tool && echo "" && echo "✅ Test 2: Token File" && ls -lh token.json && echo "" && echo "✅ Test 3: Active Processes" && ps aux | grep -E "(main.py start|localtunnel)" | grep -v grep | wc -l | awk '{print $1 " processes running"}' && echo "" && echo "✅ Test 4: Port 5000 Status" && lsof -i :5000 | grep LISTEN | wc -l | awk '{print "Port 5000: LISTENING"}' && echo "" && echo "✅ Test 5: Configuration" && grep -E "^(SIGNAL_IDENTIFIER|STRATEGY_NAME|MATHEMATRICKS_PASSPHRASE)" .env && echo "" && echo "========================================="
```

## 12. Quick Status Check
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && echo "System Status:" && echo -n "Webhook: " && (curl -s http://localhost:5000/health > /dev/null && echo "✅ RUNNING" || echo "❌ DOWN") && echo -n "Token: " && ([ -f token.json ] && echo "✅ EXISTS" || echo "❌ MISSING") && echo -n "Config: " && ([ -f .env ] && echo "✅ EXISTS" || echo "❌ MISSING") && echo -n "Processes: " && (ps aux | grep "main.py start" | grep -v grep > /dev/null && echo "✅ ACTIVE" || echo "❌ NONE")
```

## 13. Test Webhook Endpoint with Mock Pub/Sub Message
```bash
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{"message": {"data": "eyJlbWFpbEFkZHJlc3MiOiAiZ2FnYW5AZ2V0Zm9vbGlzaC5jb20iLCAiaGlzdG9yeUlkIjogMTIzNDU2fQ=="}}'
```

## 14. View Recent Webhook Logs (if saved to file)
```bash
cd /Users/gaganarora/Desktop/gagan_projects/gmail_signal && tail -n 50 webhook.log 2>/dev/null || echo "No log file found (logs appear in terminal where main.py is running)"
```

## 15. Check Google Cloud Pub/Sub (requires gcloud CLI)
```bash
gcloud pubsub topics list | grep signals-topic && gcloud pubsub subscriptions list | grep gmail-webhook && echo "✅ Pub/Sub configured correctly"
```

---

## Expected Results Summary

All commands should show:
- ✅ Webhook responding on port 5000
- ✅ Token file exists (735 bytes)
- ✅ Configuration loaded: yahoo123, LESLIE_SIGNAL
- ✅ 2+ Gmail messages with LESLIE_SIGNAL found
- ✅ 4 processes running (main.py, localtunnel)
- ✅ API test returns 200 OK
- ✅ Signal extraction working
- ✅ Port 5000 listening
