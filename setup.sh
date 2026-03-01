#!/bin/bash

echo "================================"
echo "Strategic CFO Assistant - Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if data file exists
if [ -f "upi_transactions_2024.csv" ]; then
    echo "✓ Dataset found: upi_transactions_2024.csv"
else
    echo "⚠ Warning: Dataset not found in current directory"
    echo "Please ensure upi_transactions_2024.csv is available"
    echo "Or update the path in cfo_assistant.py (line 648)"
fi
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To run the application:"
echo "  streamlit run cfo_assistant.py"
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo ""
