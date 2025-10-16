#!/bin/bash
# Quick Start Script for Gmail Signal Integration

echo "==================================="
echo "Gmail Signal Integration Quick Start"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please edit .env and fill in your credentials:"
    echo "   - GMAIL_CLIENT_ID"
    echo "   - GMAIL_CLIENT_SECRET"
    echo "   - PUBSUB_TOPIC_NAME"
    echo "   - MATHEMATRICKS_PASSPHRASE"
    echo ""
    echo "After configuring .env, run this script again."
    exit 0
fi

echo "✓ .env file found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo ""

# Check if setup has been run
if [ ! -f token.json ]; then
    echo "Running initial setup..."
    echo ""
    python3 main.py setup
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Setup completed successfully"
    else
        echo ""
        echo "✗ Setup failed. Please check the error messages above."
        exit 1
    fi
else
    echo "✓ Already authenticated (token.json exists)"
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "To start the webhook server, run:"
echo "  python3 main.py start"
echo ""
echo "Other useful commands:"
echo "  python3 main.py test-api    # Test API connection"
echo "  python3 main.py stop        # Stop push notifications"
echo ""
echo "For detailed setup instructions, see:"
echo "  SETUP_GUIDE.md"
echo ""
