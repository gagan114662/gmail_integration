#!/bin/bash
# Quick script to update and test passphrase

echo "=========================================="
echo "Mathematricks API Passphrase Update"
echo "=========================================="
echo ""

if [ -z "$1" ]; then
    echo "Usage: ./update_passphrase.sh \"your_new_passphrase\""
    echo ""
    echo "Example:"
    echo "  ./update_passphrase.sh \"correct_passphrase_123\""
    echo ""
    exit 1
fi

NEW_PASSPHRASE="$1"

echo "New passphrase: $NEW_PASSPHRASE"
echo ""

# Update .env file
if [ -f .env ]; then
    # Create backup
    cp .env .env.backup
    echo "✓ Backed up .env to .env.backup"

    # Update passphrase
    if grep -q "MATHEMATRICKS_PASSPHRASE=" .env; then
        sed -i.tmp "s/MATHEMATRICKS_PASSPHRASE=.*/MATHEMATRICKS_PASSPHRASE=$NEW_PASSPHRASE/" .env
        rm .env.tmp 2>/dev/null
        echo "✓ Updated passphrase in .env"
    else
        echo "MATHEMATRICKS_PASSPHRASE=$NEW_PASSPHRASE" >> .env
        echo "✓ Added passphrase to .env"
    fi
else
    echo "✗ .env file not found!"
    exit 1
fi

echo ""
echo "Testing API connection..."
echo "------------------------------------------"

source venv/bin/activate
python main.py test-api

echo ""
echo "=========================================="
echo "If test was successful, you're ready to go!"
echo "Start webhook: python main.py start"
echo "=========================================="
