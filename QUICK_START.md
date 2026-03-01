# Strategic CFO Assistant - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Terminal/Command Prompt

---

## Step 1: Download the Files

Make sure you have these files in your project folder:
```
strategic-cfo-assistant/
├── cfo_assistant.py          # Main application
├── requirements.txt          # Dependencies
├── upi_transactions_2024.csv # Dataset
├── README.md                 # Documentation
└── setup.sh                  # Setup script (optional)
```

---

## Step 2: Install Dependencies

### Option A: Using setup script (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Manual installation
```bash
pip install -r requirements.txt
```

This will install:
- streamlit (Web framework)
- pandas (Data processing)
- numpy (Numerical computing)
- plotly (Visualizations)
- scipy (Statistical analysis)

---

## Step 3: Configure Data Path

Open `cfo_assistant.py` and find line 648:

```python
df = pd.read_csv('/mnt/user-data/uploads/upi_transactions_2024.csv')
```

**Update the path to match your data file location:**

**Example paths:**
```python
# Windows
df = pd.read_csv('C:/Users/YourName/Documents/upi_transactions_2024.csv')

# Mac/Linux
df = pd.read_csv('/home/username/data/upi_transactions_2024.csv')

# Same directory as script
df = pd.read_csv('./upi_transactions_2024.csv')

# Relative path
df = pd.read_csv('../data/upi_transactions_2024.csv')
```

---

## Step 4: Run the Application

```bash
streamlit run cfo_assistant.py
```

The application will:
1. Start the Streamlit server
2. Load and process the data
3. Open your default browser automatically
4. Navigate to http://localhost:8501

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## Step 5: Start Asking Questions!

### Try These Example Queries:

**Revenue Analysis:**
- "Why did revenue drop last week?"
- "Show me revenue trends for the last month"
- "Compare this week to last week"

**Root Cause Investigation:**
- "What caused the revenue decline?"
- "Which regions are performing poorly?"
- "What's driving the change?"

**Impact Quantification:**
- "How much money are we losing?"
- "What's the financial impact?"
- "Show me revenue leakage"

**Risk Analysis:**
- "What are the high-risk segments?"
- "Where should we focus attention?"
- "Which areas are most problematic?"

**Counterfactual Analysis:**
- "If success rate hadn't changed, what would revenue be?"
- "What if the failure rate was lower?"
- "Show me alternative scenarios"

---

## Common First-Time Issues

### Issue 1: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Use a different port
streamlit run cfo_assistant.py --server.port 8502
```

### Issue 2: Module Not Found
**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue 3: Data File Not Found
**Error:** `FileNotFoundError: [Errno 2] No such file or directory`

**Solution:**
- Check the file path in line 648 of `cfo_assistant.py`
- Make sure `upi_transactions_2024.csv` exists
- Use absolute path for clarity

### Issue 4: Permission Denied (Linux/Mac)
**Error:** `Permission denied: 'upi_transactions_2024.csv'`

**Solution:**
```bash
chmod 644 upi_transactions_2024.csv
```

### Issue 5: Slow Loading
**Problem:** Application takes long to load

**Solution:**
- Dataset is large (250K rows) - first load takes 5-10 seconds
- Subsequent queries are fast (data is cached)
- This is normal behavior

---

## Understanding the Interface

### Sidebar (Left)
- **Dataset Overview**: Key metrics about your data
- **Try These Questions**: Pre-configured example queries
- **Clear Conversation**: Reset the chat

### Main Area (Center)
- **Chat Interface**: Ask questions and see responses
- **Metrics Cards**: Key numbers displayed prominently
- **Confidence Indicators**: Color-coded trust levels
  - 🟢 Green = High confidence (75%+)
  - 🟠 Orange = Medium confidence (50-74%)
  - 🔴 Red = Low confidence (<50%)

### Expandable Sections
- **📋 Assumptions & Limitations**: What the analysis assumes
- **💡 Recommendations**: Suggested actions

---

## Tips for Best Results

### 1. Be Specific with Time Periods
❌ "Show me data"
✅ "Show me revenue for last week"

### 2. Ask Follow-up Questions
The AI remembers context:
- First: "Why did revenue drop?"
- Then: "Which region caused this?"
- Then: "How much are we losing?"

### 3. Use Natural Language
You don't need technical jargon:
- ✅ "Why are we making less money?"
- ✅ "What went wrong last week?"
- ✅ "Where are we losing customers?"

### 4. Check Confidence Levels
Always look at the confidence indicator:
- **High**: Trust the analysis
- **Medium**: Good directional insight
- **Low**: More data needed

### 5. Read the Assumptions
Expand the "Assumptions & Limitations" section to understand:
- What data was used
- What was assumed
- What limitations exist

---

## Next Steps

### Explore More Features
1. Try counterfactual analysis
2. Ask about specific regions/categories
3. Request risk assessments
4. Compare different time periods

### Customize the Experience
1. Modify example questions in the sidebar
2. Adjust confidence thresholds
3. Add your own analysis dimensions
4. Integrate with your own data

### Share Your Results
1. Take screenshots of insights
2. Export conversation history (future feature)
3. Share findings with leadership

---

## Getting Help

### Resources
- **README.md**: Full documentation
- **DEMO_FLOW.md**: Demo scenarios
- **TECHNICAL_ARCHITECTURE.md**: Technical details

### Troubleshooting
1. Check console for error messages
2. Verify data file path
3. Ensure all dependencies installed
4. Restart the application

### Support Channels
- GitHub Issues: Report bugs
- Documentation: Check FAQs
- Community: Ask questions

---

## What to Expect

### First Query (30 seconds)
- Data loads and caches
- Analysis runs
- Response generated

### Subsequent Queries (<2 seconds)
- Data already cached
- Instant responses
- Smooth conversation

### Data Processing
- 250,000 transactions analyzed
- Multi-dimensional aggregations
- Statistical confidence calculated
- Natural language narrative generated

---

## Advanced Usage

### Running on Custom Port
```bash
streamlit run cfo_assistant.py --server.port 8888
```

### Running on Network
```bash
streamlit run cfo_assistant.py --server.address 0.0.0.0
```

### Headless Mode (No Browser)
```bash
streamlit run cfo_assistant.py --server.headless true
```

### Development Mode (Auto-reload)
```bash
streamlit run cfo_assistant.py --server.runOnSave true
```

---

## Performance Expectations

### Load Time
- Initial load: 5-10 seconds
- Data caching: One-time cost
- Subsequent loads: Instant

### Query Response
- Simple queries: <1 second
- Complex analysis: 1-2 seconds
- Root cause analysis: 2-3 seconds

### Memory Usage
- Dataset: ~100-200 MB
- Application: ~50 MB
- Total: ~150-250 MB

---

## Success Checklist

✅ Python 3.8+ installed
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ Data file path configured
✅ Application running (`streamlit run cfo_assistant.py`)
✅ Browser opened to http://localhost:8501
✅ Can see dataset overview in sidebar
✅ Can ask questions and get responses
✅ Confidence indicators showing
✅ Metrics displaying correctly

---

## You're Ready! 🎉

Start with a simple question like:
**"Show me revenue trends for the last week"**

Then explore more complex queries as you get comfortable.

Remember: This is your CFO assistant - ask it anything about your business metrics!

---

**Need more help?** Check the full README.md or TECHNICAL_ARCHITECTURE.md
