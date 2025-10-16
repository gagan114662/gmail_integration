# Gmail Push Notifications - Auto-Renewal Cron Job

## ✅ Installed Cron Job

**Schedule:** Every 6 days at midnight (00:00)
**Command:** `/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh`
**Log File:** `/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log`

---

## What It Does

Gmail push notifications expire after 7 days. This cron job automatically renews them every 6 days to ensure continuous real-time monitoring without interruption.

---

## Cron Schedule Details

```cron
0 0 */6 * * /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh
```

**Breakdown:**
- `0` - Minute (00)
- `0` - Hour (midnight)
- `*/6` - Every 6 days
- `*` - Every month
- `*` - Every day of week

**Runs on:** Day 1, 7, 13, 19, 25, 31 of each month at 00:00

---

## Management Commands

### View Installed Cron Jobs
```bash
crontab -l
```

### View Renewal Logs
```bash
tail -f /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```

### View Recent Renewals
```bash
tail -n 50 /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```

### Test Renewal Script Manually
```bash
/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh
```

### Remove Cron Job (if needed)
```bash
crontab -l | grep -v "renew_push.sh" | crontab -
```

### Edit Cron Jobs
```bash
crontab -e
```

---

## Monitoring

### Check if Cron Job Ran Successfully

```bash
grep "✅" /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```

### Check for Failures

```bash
grep "❌" /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```

### View Last Renewal

```bash
tail -n 20 /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```

---

## Troubleshooting

### Cron Job Not Running?

1. **Check if cron is enabled on macOS:**
   ```bash
   sudo launchctl list | grep cron
   ```

2. **Give Terminal Full Disk Access:**
   - System Preferences → Security & Privacy → Privacy
   - Select "Full Disk Access"
   - Add Terminal (or your terminal app)

3. **Check cron logs:**
   ```bash
   log show --predicate 'process == "cron"' --last 1d
   ```

### Script Fails?

1. **Test script manually:**
   ```bash
   /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh
   ```

2. **Check permissions:**
   ```bash
   ls -la /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh
   ```

3. **Verify virtual environment exists:**
   ```bash
   ls -la /Users/gaganarora/Desktop/gagan_projects/gmail_signal/venv/
   ```

### macOS Specific Issues

On macOS, you may need to grant cron permission to run:

1. The first time cron runs, macOS may ask for permission
2. Check System Preferences → Security & Privacy → Privacy → Full Disk Access
3. Ensure your terminal app has access

---

## Alternative: launchd (macOS Native)

For better macOS integration, you can use launchd instead of cron:

### Create launchd plist

```bash
cat > ~/Library/LaunchAgents/com.gmail.signal.renew.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gmail.signal.renew</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>518400</integer>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log</string>
</dict>
</plist>
EOF
```

### Load launchd job

```bash
launchctl load ~/Library/LaunchAgents/com.gmail.signal.renew.plist
```

### Check status

```bash
launchctl list | grep gmail.signal
```

### Unload if needed

```bash
launchctl unload ~/Library/LaunchAgents/com.gmail.signal.renew.plist
```

---

## Log File Format

The renewal log will look like this:

```
=========================================
Thu Oct 16 00:00:01 EDT 2025: Starting push notification renewal
=========================================
Setting up Gmail authentication...
Authentication successful!

Setting up push notifications...
Push notifications enabled. History ID: 39490302
Expiration: 1761241720496
Push notifications enabled successfully!
...
Thu Oct 16 00:00:15 EDT 2025: ✅ Push notifications renewed successfully

```

---

## Current Status

**Cron Job:** ✅ Installed and Active
**Next Run:** Check with `crontab -l`
**Log File:** Created automatically on first run
**Status:** Monitoring system will continue uninterrupted

---

## Important Notes

1. **Keep the project directory intact** - Don't move or delete the folder
2. **Virtual environment required** - Don't delete `venv/` folder
3. **Token.json needed** - Keep authentication token in place
4. **Network required** - Ensure internet connectivity when cron runs
5. **Logs rotate** - Old logs are appended, consider rotating manually if file gets large

---

## Verification

After the first automatic run (within 6 days), check:

```bash
# Should show successful renewal
tail -n 30 /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```

You can also manually trigger a renewal right now to test:

```bash
/Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.sh && tail -n 20 /Users/gaganarora/Desktop/gagan_projects/gmail_signal/renew_push.log
```
