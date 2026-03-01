# Strategic CFO Assistant

A functional conversational AI prototype that processes ~250,000 digital payment transactions and delivers leadership-level financial insights through natural language conversation.

## 🎯 Overview

The Strategic CFO Assistant transforms raw UPI transaction data into actionable business intelligence through:
- **What happened** - Clear metrics and trends
- **Why it happened** - Root cause analysis
- **How serious the impact is** - Revenue quantification
- **What decision to consider** - Strategic recommendations
- **How confident the system is** - Transparency and trust

## ✨ Key Features

### 1. Conversational Leadership Queries
Ask questions in plain English:
- "Why did revenue drop last week?"
- "Which regions caused the biggest loss?"
- "Is this a volume issue or a failure-rate issue?"
- "How much money are we losing if this continues?"

### 2. Revenue & Risk Intelligence
- Revenue trends over time with detailed breakdowns
- Transaction success rate analysis
- Revenue leakage due to failures, refunds, chargebacks
- High-risk regions, channels, and merchant categories

### 3. Root Cause Narratives
Natural language explanations like:
> "Revenue declined mainly because UPI failure rates increased by 5% in North India, leading to an estimated ₹X loss."

Automatically ranks causes by impact across multiple dimensions:
- Regional analysis
- Transaction type breakdown
- Merchant category patterns
- Banking channel performance
- Device and network analysis

### 4. Impact Quantification
Every major insight includes:
- Estimated revenue loss or risk
- Comparison to previous period
- Business significance (Minor / Moderate / Critical)
- Clear metrics for decision-making

### 5. Confidence & Assumptions Indicator
Each response clearly states:
- Confidence level (High / Medium / Low with percentage)
- Factors affecting confidence (sample size, stability)
- Any assumptions made
- Data limitations detected

Example:
> **Confidence: High (85%)** - Based on 48,000 transactions with strong sample size and high metric stability

### 6. Counterfactual Insights
Scenario analysis:
> "If the success rate had remained at last week's level, revenue would have been ₹X higher."

Shows decision-grade analytics, not just reporting.

### 7. Leadership-Safe Design
- Never takes actions automatically
- Never judges individuals
- Never claims absolute causality
- Always keeps humans in control
- Professional, boardroom-ready language

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Ensure the dataset is available:**
The application expects the dataset at:
```
/mnt/user-data/uploads/upi_transactions_2024.csv
```

Or modify the path in `cfo_assistant.py` line 648:
```python
df = pd.read_csv('path/to/your/upi_transactions_2024.csv')
```

4. **Run the application:**
```bash
streamlit run cfo_assistant.py
```

5. **Open your browser:**
The app will automatically open at `http://localhost:8501`

## 📊 Dataset Context

The system works with a synthetic dataset containing ~250,000 payment transactions with fields:
- Transaction ID, timestamp/date
- Transaction amount
- Success/failure status
- Payment channel (UPI types)
- Region/state
- Merchant category
- Customer/merchant identifiers
- Device type, network type
- Fraud flags

## 💡 Usage Examples

### Example 1: Revenue Decline Analysis
```
User: "Why did revenue drop last week?"

AI: Revenue DECLINED by ₹2,345,678 (12.3%) last week compared to the previous week.

What Changed:
- Revenue: ₹16,789,234 (from ₹19,134,912)
- Transaction Volume: 15,234 (-1,456 transactions)
- Success Rate: 94.2% (-3.1%)
- Average Transaction: ₹1,102 (+₹45)

Primary Driver: The change appears to be driven by success rate change.

Confidence: High (87%) - Based on 15,234 transactions with strong sample size
```

### Example 2: Root Cause Investigation
```
User: "What caused this?"

AI: Root Cause Analysis for Nov 15-21, 2024:

I've identified the following factors that significantly impacted revenue:

1. Region: Uttar Pradesh
   - Revenue Impact: ₹-1,234,567 (decreased)
   - Success Rate Change: -4.5% (from 95.2% to 90.7%)
   - Lost Revenue: ₹567,890
   - Transaction Volume: 3,456
   - Confidence: High (91%)

2. Transaction Type: P2M
   - Revenue Impact: ₹-876,543 (decreased)
   - Success Rate Change: -3.2% (from 96.1% to 92.9%)
   ...
```

### Example 3: Impact Quantification
```
User: "How much money are we losing?"

AI: Financial Impact Analysis for Last Week:

Revenue Leakage:
- Actual Revenue: ₹16,789,234
- Potential Revenue: ₹18,234,567
- Lost Revenue: ₹1,445,333

Transaction Metrics:
- Total Transactions: 15,234
- Failed Transactions: 892
- Failure Rate: 5.85%

Business Impact: MODERATE - Revenue leakage is between 5-10% of potential
```

### Example 4: Counterfactual Analysis
```
User: "What if the success rate hadn't changed?"

AI: Counterfactual Analysis for Last Week:

Scenario: If the success rate had remained at previous week's level (97.3%):

- Expected Revenue: ₹18,967,234
- Actual Revenue: ₹16,789,234
- Difference: ₹2,178,000

Revenue would have been ₹2,178,000 higher if the success rate had not 
declined from 97.3% to 94.2%.

Confidence: High (80%) - Counterfactual assumes all other factors remain constant
```

## 🏗️ Architecture

### Tech Stack
- **Backend & Analytics:** Python with Pandas for fast data aggregation
- **Conversational Layer:** Custom NLP query understanding and response generation
- **Statistical Analysis:** SciPy for trend analysis and confidence calculation
- **Frontend:** Streamlit for lightweight, interactive web interface
- **Visualization:** Plotly for interactive charts (when needed)

### Key Components

1. **DataAnalytics Class**
   - Core analytics engine
   - Revenue trend analysis
   - Root cause identification
   - Risk assessment
   - Confidence calculation

2. **ConversationalAI Class**
   - Query understanding and intent detection
   - Natural language response generation
   - Context management for follow-up questions
   - Narrative construction

3. **Streamlit UI**
   - Chat-style interface
   - Real-time metric display
   - Confidence indicators
   - Assumption transparency

## 🎓 Key Design Principles

### 1. Explainability First
Every response includes:
- Clear narrative explanation
- Supporting metrics
- Confidence assessment
- Stated assumptions

### 2. Confidence Transparency
Confidence calculated based on:
- Sample size (more data = higher confidence)
- Metric stability (consistent patterns = higher confidence)
- Clearly communicated to users

### 3. Leadership-Grade Output
- Boardroom-ready language
- Focus on business impact, not technical details
- Actionable insights
- No jargon or complex terminology

### 4. Safe and Responsible
- No automatic actions
- No individual attribution
- Acknowledges limitations
- Human remains in control

## 📈 Supported Analysis Types

1. **Revenue Analysis**
   - Trend identification
   - Period-over-period comparison
   - Growth/decline analysis

2. **Root Cause Analysis**
   - Multi-dimensional investigation
   - Impact ranking
   - Causal factor identification

3. **Risk Assessment**
   - High-risk segment identification
   - Failure pattern analysis
   - Revenue at risk quantification

4. **Counterfactual Analysis**
   - Scenario modeling
   - What-if analysis
   - Impact estimation

5. **Impact Quantification**
   - Revenue leakage calculation
   - Business severity assessment
   - Financial impact metrics

## 🔒 Limitations & Assumptions

- **Data Quality:** Analysis quality depends on input data accuracy
- **Causation:** System identifies correlations, not definitive causation
- **External Factors:** Cannot account for external market conditions
- **Time Lag:** Analysis based on historical data only
- **Scope:** Limited to transaction data dimensions available

## 🤝 Contributing

This is a prototype designed for demonstration and evaluation purposes.

## 📄 License

This project is created for hackathon/competition purposes.

## 👥 Support

For questions or issues, please refer to the project documentation or contact the development team.

---

**Built with ❤️ for CFOs and Finance Leaders**
