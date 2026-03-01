"""
Strategic CFO Assistant
A conversational AI prototype for leadership-level financial insights from UPI transaction data.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional
import json
import re

# Page configuration
st.set_page_config(
    page_title="Strategic CFO Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimalist professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean white background */
    .main {
        background: #ffffff;
    }
    
    /* Minimal sidebar */
    [data-testid="stSidebar"] {
        background: #fafafa;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Clean headers */
    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #111827 !important;
    }
    
    /* Minimal header styling */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 2rem;
        line-height: 1.5;
        font-weight: 400;
    }
    
    /* Clean insight cards */
    .insight-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 3px solid #3b82f6;
        margin-bottom: 1rem;
    }
    
    /* Minimal metric cards */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    /* Simple confidence indicators */
    .confidence-high {
        color: #059669;
        font-weight: 600;
    }
    
    .confidence-medium {
        color: #d97706;
        font-weight: 600;
    }
    
    .confidence-low {
        color: #dc2626;
        font-weight: 600;
    }
    
    /* Clean chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: #f9fafb;
        border-left: 3px solid #6b7280;
    }
    
    .assistant-message {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 3px solid #3b82f6;
    }
    
    /* Minimal buttons */
    .stButton>button {
        background: #3b82f6;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        transition: background 0.2s ease;
    }
    
    .stButton>button:hover {
        background: #2563eb;
    }
    
    /* Clean expanders */
    .streamlit-expanderHeader {
        background: #f9fafb;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        font-weight: 500;
    }
    
    /* Minimal info boxes */
    .stAlert {
        background: #f0f9ff;
        border-radius: 6px;
        border-left: 3px solid #3b82f6;
    }
    
    /* Clean sidebar metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
        color: #111827;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Simple scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Clean section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)


class DataAnalytics:
    """Core analytics engine for processing transaction data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._prepare_data()
        
    def _prepare_data(self):
        """Prepare and clean the dataset"""
        # Convert timestamp
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
        # Extract time features
        self.df['date'] = self.df['timestamp'].dt.date
        self.df['week'] = self.df['timestamp'].dt.isocalendar().week
        self.df['month'] = self.df['timestamp'].dt.month
        self.df['month_name'] = self.df['timestamp'].dt.strftime('%B')
        self.df['hour'] = self.df['timestamp'].dt.hour
        
        # Calculate revenue (only successful transactions)
        self.df['revenue'] = self.df.apply(
            lambda x: x['amount (INR)'] if x['transaction_status'] == 'SUCCESS' else 0, 
            axis=1
        )
        
        # Create failure flag
        self.df['is_failure'] = (self.df['transaction_status'] != 'SUCCESS').astype(int)
        
        # Potential revenue if transaction succeeded
        self.df['potential_revenue'] = self.df['amount (INR)']
        
        # Lost revenue (for combinations analysis)
        self.df['lost_revenue'] = self.df['potential_revenue'] - self.df['revenue']
        
    def get_revenue_trend(self, period: str = 'daily', last_n: int = 30) -> pd.DataFrame:
        """Get revenue trends over time"""
        if period == 'daily':
            trend = self.df.groupby('date').agg({
                'revenue': 'sum',
                'transaction id': 'count',
                'is_failure': 'sum',
                'potential_revenue': 'sum'
            }).tail(last_n)
            
        elif period == 'weekly':
            trend = self.df.groupby('week').agg({
                'revenue': 'sum',
                'transaction id': 'count',
                'is_failure': 'sum',
                'potential_revenue': 'sum'
            }).tail(last_n)
            
        else:  # monthly
            trend = self.df.groupby('month_name').agg({
                'revenue': 'sum',
                'transaction id': 'count',
                'is_failure': 'sum',
                'potential_revenue': 'sum'
            })
        
        # Calculate metrics
        trend['success_rate'] = (1 - trend['is_failure'] / trend['transaction id']) * 100
        trend['lost_revenue'] = trend['potential_revenue'] - trend['revenue']
        
        return trend
    
    def analyze_revenue_change(self, period1: Tuple, period2: Tuple) -> Dict:
        """Compare revenue between two periods"""
        # Filter data for periods
        df1 = self.df[(self.df['date'] >= period1[0]) & (self.df['date'] <= period1[1])]
        df2 = self.df[(self.df['date'] >= period2[0]) & (self.df['date'] <= period2[1])]
        
        # Calculate metrics
        revenue1 = df1['revenue'].sum()
        revenue2 = df2['revenue'].sum()
        
        transactions1 = len(df1)
        transactions2 = len(df2)
        
        success_rate1 = (df1['transaction_status'] == 'SUCCESS').mean() * 100
        success_rate2 = (df2['transaction_status'] == 'SUCCESS').mean() * 100
        
        avg_transaction1 = df1[df1['transaction_status'] == 'SUCCESS']['amount (INR)'].mean()
        avg_transaction2 = df2[df2['transaction_status'] == 'SUCCESS']['amount (INR)'].mean()
        
        return {
            'revenue_change': revenue2 - revenue1,
            'revenue_change_pct': ((revenue2 - revenue1) / revenue1 * 100) if revenue1 > 0 else 0,
            'revenue1': revenue1,
            'revenue2': revenue2,
            'transaction_change': transactions2 - transactions1,
            'transaction_change_pct': ((transactions2 - transactions1) / transactions1 * 100) if transactions1 > 0 else 0,
            'success_rate_change': success_rate2 - success_rate1,
            'success_rate1': success_rate1,
            'success_rate2': success_rate2,
            'avg_transaction_change': avg_transaction2 - avg_transaction1,
            'avg_transaction1': avg_transaction1,
            'avg_transaction2': avg_transaction2,
            'n_samples1': transactions1,
            'n_samples2': transactions2
        }
    
    def find_root_causes(self, period: Tuple, comparison_period: Tuple = None) -> List[Dict]:
        """Identify root causes of revenue changes"""
        causes = []
        
        # Filter data
        current_df = self.df[(self.df['date'] >= period[0]) & (self.df['date'] <= period[1])]
        
        if comparison_period:
            prev_df = self.df[(self.df['date'] >= comparison_period[0]) & (self.df['date'] <= comparison_period[1])]
        else:
            # Use previous period of same length
            period_length = (period[1] - period[0]).days + 1
            comp_end = period[0] - timedelta(days=1)
            comp_start = comp_end - timedelta(days=period_length - 1)
            prev_df = self.df[(self.df['date'] >= comp_start) & (self.df['date'] <= comp_end)]
        
        # Analyze by different dimensions
        dimensions = [
            ('sender_state', 'Region'),
            ('transaction type', 'Transaction Type'),
            ('merchant_category', 'Merchant Category'),
            ('sender_bank', 'Sender Bank'),
            ('receiver_bank', 'Receiver Bank'),
            ('device_type', 'Device Type'),
            ('network_type', 'Network Type'),
            ('sender_age_group', 'Customer Age Group')
        ]
        
        for dim, dim_name in dimensions:
            # Current period metrics by dimension
            current_metrics = current_df.groupby(dim).agg({
                'revenue': 'sum',
                'transaction id': 'count',
                'is_failure': 'sum',
                'potential_revenue': 'sum'
            })
            current_metrics['success_rate'] = (1 - current_metrics['is_failure'] / current_metrics['transaction id']) * 100
            current_metrics['lost_revenue'] = current_metrics['potential_revenue'] - current_metrics['revenue']
            
            # Previous period metrics
            prev_metrics = prev_df.groupby(dim).agg({
                'revenue': 'sum',
                'transaction id': 'count',
                'is_failure': 'sum',
                'potential_revenue': 'sum'
            })
            prev_metrics['success_rate'] = (1 - prev_metrics['is_failure'] / prev_metrics['transaction id']) * 100
            
            # Compare
            for category in current_metrics.index:
                if category in prev_metrics.index:
                    revenue_change = current_metrics.loc[category, 'revenue'] - prev_metrics.loc[category, 'revenue']
                    success_rate_change = current_metrics.loc[category, 'success_rate'] - prev_metrics.loc[category, 'success_rate']
                    
                    # Only track significant changes
                    if abs(revenue_change) > 10000 or abs(success_rate_change) > 2:
                        causes.append({
                            'dimension': dim_name,
                            'category': category,
                            'revenue_impact': revenue_change,
                            'success_rate_change': success_rate_change,
                            'current_success_rate': current_metrics.loc[category, 'success_rate'],
                            'prev_success_rate': prev_metrics.loc[category, 'success_rate'],
                            'current_revenue': current_metrics.loc[category, 'revenue'],
                            'lost_revenue': current_metrics.loc[category, 'lost_revenue'],
                            'transaction_count': current_metrics.loc[category, 'transaction id'],
                            'confidence': self._calculate_confidence(current_metrics.loc[category, 'transaction id'], 
                                                                     current_metrics.loc[category, 'success_rate'])
                        })
        
        # Sort by absolute revenue impact
        causes.sort(key=lambda x: abs(x['revenue_impact']), reverse=True)
        
        return causes[:10]  # Return top 10 causes
    
    def _calculate_confidence(self, n_samples: int, success_rate: float) -> Dict:
        """Calculate confidence level based on sample size and variance"""
        # More samples = higher confidence
        # Success rate near 50% = higher variance = lower confidence
        
        sample_score = min(n_samples / 10000, 1.0)  # Normalize to 0-1
        
        # Variance is highest at 50%, lowest at 0% or 100%
        variance_score = 1 - abs(success_rate - 50) / 50
        stability_score = 1 - variance_score
        
        confidence_score = (sample_score * 0.6 + stability_score * 0.4) * 100
        
        if confidence_score >= 75:
            level = "High"
        elif confidence_score >= 50:
            level = "Medium"
        else:
            level = "Low"
        
        return {
            'score': confidence_score,
            'level': level,
            'n_samples': n_samples,
            'factors': {
                'sample_size': 'Strong' if sample_score > 0.7 else 'Moderate' if sample_score > 0.3 else 'Weak',
                'stability': 'Strong' if stability_score > 0.7 else 'Moderate' if stability_score > 0.3 else 'Weak'
            }
        }
    
    def calculate_counterfactual(self, period: Tuple, comparison_period: Tuple = None) -> Dict:
        """Calculate what revenue would be if conditions remained the same"""
        current_df = self.df[(self.df['date'] >= period[0]) & (self.df['date'] <= period[1])]
        
        if comparison_period:
            prev_df = self.df[(self.df['date'] >= comparison_period[0]) & (self.df['date'] <= comparison_period[1])]
        else:
            period_length = (period[1] - period[0]).days + 1
            comp_end = period[0] - timedelta(days=1)
            comp_start = comp_end - timedelta(days=period_length - 1)
            prev_df = self.df[(self.df['date'] >= comp_start) & (self.df['date'] <= comp_end)]
        
        # Get previous success rate
        prev_success_rate = (prev_df['transaction_status'] == 'SUCCESS').mean()
        
        # Apply to current volume
        counterfactual_revenue = current_df['potential_revenue'].sum() * prev_success_rate
        actual_revenue = current_df['revenue'].sum()
        
        return {
            'counterfactual_revenue': counterfactual_revenue,
            'actual_revenue': actual_revenue,
            'difference': counterfactual_revenue - actual_revenue,
            'prev_success_rate': prev_success_rate * 100,
            'current_success_rate': (current_df['transaction_status'] == 'SUCCESS').mean() * 100
        }
    
    def get_high_risk_combinations(self, top_n: int = 10) -> List[Dict]:
        """Find riskiest combinations of region, device type, and network condition"""
        # Group by all three dimensions
        combinations = self.df.groupby(['sender_state', 'device_type', 'network_type']).agg({
            'transaction id': 'count',  # Column name has a space
            'is_failure': 'sum',
            'lost_revenue': 'sum'
        }).reset_index()
        
        combinations.columns = ['region', 'device_type', 'network_type', 'total_txns', 'failures', 'lost_revenue']
        
        # Calculate failure rate
        combinations['failure_rate'] = (combinations['failures'] / combinations['total_txns'] * 100)
        
        # Calculate risk score (failure_rate * lost_revenue)
        combinations['risk_score'] = combinations['failure_rate'] * combinations['lost_revenue']
        
        # Filter for significance (at least 100 transactions)
        combinations = combinations[combinations['total_txns'] >= 100]
        
        # Sort by risk score
        combinations = combinations.sort_values('risk_score', ascending=False)
        
        results = []
        for _, row in combinations.head(top_n).iterrows():
            confidence = self._calculate_confidence(
                int(row['total_txns']),
                100 - row['failure_rate']
            )
            
            results.append({
                'combination': f"{row['region']} + {row['device_type']} + {row['network_type']}",
                'region': row['region'],
                'device_type': row['device_type'],
                'network_type': row['network_type'],
                'failure_rate': row['failure_rate'],
                'total_transactions': int(row['total_txns']),
                'failed_transactions': int(row['failures']),
                'lost_revenue': row['lost_revenue'],
                'risk_score': row['risk_score'],
                'confidence': confidence
            })
        
        return results
    
    def get_high_risk_segments(self, top_n: int = 5) -> List[Dict]:
        """Identify high-risk segments by failure rate and volume"""
        segments = []
        
        dimensions = [
            ('sender_state', 'Region'),
            ('merchant_category', 'Merchant Category'),
            ('transaction type', 'Transaction Type'),
            ('sender_age_group', 'Customer Age Group')
        ]
        
        for dim, dim_name in dimensions:
            segment_metrics = self.df.groupby(dim).agg({
                'is_failure': ['sum', 'mean'],
                'transaction id': 'count',
                'potential_revenue': 'sum',
                'revenue': 'sum'
            })
            
            segment_metrics.columns = ['failures', 'failure_rate', 'volume', 'potential', 'actual']
            segment_metrics['lost_revenue'] = segment_metrics['potential'] - segment_metrics['actual']
            segment_metrics['risk_score'] = segment_metrics['failure_rate'] * segment_metrics['lost_revenue']
            
            # Get top risky segments
            top_segments = segment_metrics.nlargest(top_n, 'risk_score')
            
            for category in top_segments.index:
                segments.append({
                    'dimension': dim_name,
                    'category': category,
                    'failure_rate': top_segments.loc[category, 'failure_rate'] * 100,
                    'failures': top_segments.loc[category, 'failures'],
                    'volume': top_segments.loc[category, 'volume'],
                    'lost_revenue': top_segments.loc[category, 'lost_revenue'],
                    'risk_score': top_segments.loc[category, 'risk_score']
                })
        
        # Sort by lost revenue
        segments.sort(key=lambda x: x['lost_revenue'], reverse=True)
        
        return segments[:top_n]


class ConversationalAI:
    """Natural language query understanding and response generation"""
    
    def __init__(self, analytics: DataAnalytics):
        self.analytics = analytics
        self.conversation_history = []
        self.conversation_context = {
            'last_topic': None,
            'last_period': None,
            'analysis_count': 0
        }
        
    def understand_query(self, query: str) -> Dict:
        """Parse user query and extract intent and parameters"""
        query_lower = query.lower()
        
        intent = {
            'type': None,
            'time_period': None,
            'comparison': False,
            'specific_dimension': None,
            'specific_value': None
        }
        
        # Detect query type
        if any(word in query_lower for word in ['revenue', 'sales', 'income', 'earning']):
            if any(word in query_lower for word in ['drop', 'decline', 'decrease', 'fall', 'down', 'lower']):
                intent['type'] = 'revenue_decline'
            elif any(word in query_lower for word in ['increase', 'rise', 'grow', 'up', 'higher']):
                intent['type'] = 'revenue_increase'
            else:
                intent['type'] = 'revenue_analysis'
                
        elif any(word in query_lower for word in ['why', 'reason', 'cause', 'explain']):
            intent['type'] = 'root_cause'
            
        elif any(word in query_lower for word in ['impact', 'loss', 'cost', 'money', 'much']):
            intent['type'] = 'impact_quantification'
            
        elif any(word in query_lower for word in ['risk', 'danger', 'problem', 'issue']):
            # Check if asking for combinations
            if any(word in query_lower for word in ['combination', 'combinations', 'together', 'combined']):
                intent['type'] = 'risk_combination'
            else:
                intent['type'] = 'risk_analysis'
            
        elif any(word in query_lower for word in ['if', 'would', 'could', 'scenario']):
            intent['type'] = 'counterfactual'
            
        elif any(word in query_lower for word in ['region', 'state', 'location', 'where']):
            intent['type'] = 'regional_analysis'
            intent['specific_dimension'] = 'region'
            
        elif any(word in query_lower for word in ['channel', 'method', 'type']):
            intent['type'] = 'channel_analysis'
            intent['specific_dimension'] = 'channel'
            
        else:
            intent['type'] = 'general_overview'
        
        # Detect time period
        if 'last week' in query_lower or 'past week' in query_lower:
            intent['time_period'] = 'last_week'
        elif 'last month' in query_lower or 'past month' in query_lower:
            intent['time_period'] = 'last_month'
        elif 'this week' in query_lower:
            intent['time_period'] = 'this_week'
        elif 'this month' in query_lower:
            intent['time_period'] = 'this_month'
        elif 'today' in query_lower:
            intent['time_period'] = 'today'
        elif 'yesterday' in query_lower:
            intent['time_period'] = 'yesterday'
        else:
            intent['time_period'] = 'last_7_days'  # Default
        
        # Detect comparison request
        if any(word in query_lower for word in ['compare', 'vs', 'versus', 'than', 'previous']):
            intent['comparison'] = True
        
        return intent
    
    def get_time_range(self, period: str) -> Tuple:
        """Convert period string to date range"""
        today = self.analytics.df['date'].max()
        
        if period == 'today':
            return (today, today)
        elif period == 'yesterday':
            yesterday = today - timedelta(days=1)
            return (yesterday, yesterday)
        elif period == 'this_week':
            week_start = today - timedelta(days=today.weekday())
            return (week_start, today)
        elif period == 'last_week':
            week_start = today - timedelta(days=today.weekday() + 7)
            week_end = week_start + timedelta(days=6)
            return (week_start, week_end)
        elif period == 'this_month':
            month_start = today.replace(day=1)
            return (month_start, today)
        elif period == 'last_month':
            month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            month_end = today.replace(day=1) - timedelta(days=1)
            return (month_start, month_end)
        else:  # last_7_days
            start = today - timedelta(days=6)
            return (start, today)
    
    def generate_response(self, query: str) -> Dict:
        """Generate comprehensive response to user query"""
        # Understand the query
        intent = self.understand_query(query)
        
        # Get time periods
        current_period = self.get_time_range(intent['time_period'])
        
        # Calculate comparison period if needed
        if intent['comparison'] or intent['type'] in ['revenue_decline', 'revenue_increase', 'root_cause']:
            period_length = (current_period[1] - current_period[0]).days + 1
            comp_end = current_period[0] - timedelta(days=1)
            comp_start = comp_end - timedelta(days=period_length - 1)
            comparison_period = (comp_start, comp_end)
        else:
            comparison_period = None
        
        # Generate response based on intent
        response = {
            'query': query,
            'intent': intent,
            'narrative': '',
            'insights': [],
            'metrics': {},
            'confidence': {},
            'recommendations': [],
            'assumptions': [],
            'visualizations': [],
            'context_summary': '',
            'decision_suggestions': []
        }
        
        # Add conversational context if this is a follow-up
        if self.conversation_context['analysis_count'] > 0 and self.conversation_context['last_topic']:
            response['context_summary'] = f"📌 **Context:** Building on your previous analysis of {self.conversation_context['last_topic']}"
        
        # Update context
        self.conversation_context['analysis_count'] += 1
        self.conversation_context['last_period'] = current_period
        
        if intent['type'] == 'revenue_decline' or intent['type'] == 'revenue_analysis':
            response = self._analyze_revenue_change(current_period, comparison_period, response)
            self.conversation_context['last_topic'] = 'revenue trends'
            
        elif intent['type'] == 'root_cause':
            response = self._analyze_root_causes(current_period, comparison_period, response)
            self.conversation_context['last_topic'] = 'root causes'
            
        elif intent['type'] == 'impact_quantification':
            response = self._quantify_impact(current_period, comparison_period, response)
            self.conversation_context['last_topic'] = 'financial impact'
            
        elif intent['type'] == 'risk_analysis':
            response = self._analyze_risks(response)
            self.conversation_context['last_topic'] = 'risk assessment'
        
        elif intent['type'] == 'risk_combination':
            response = self._analyze_risk_combinations(response)
            self.conversation_context['last_topic'] = 'multi-dimensional risk analysis'
            
        elif intent['type'] == 'counterfactual':
            response = self._generate_counterfactual(current_period, comparison_period, response)
            self.conversation_context['last_topic'] = 'scenario analysis'
            
        else:
            response = self._general_overview(current_period, response)
            self.conversation_context['last_topic'] = 'executive summary'
        
        return response
    
    def _analyze_revenue_change(self, current_period, comparison_period, response):
        """Analyze revenue changes between periods"""
        if comparison_period:
            analysis = self.analytics.analyze_revenue_change(comparison_period, current_period)
            
            # Build narrative
            period_label = self._get_period_label(current_period)
            prev_label = self._get_period_label(comparison_period)
            
            change_direction = "increased" if analysis['revenue_change'] > 0 else "declined"
            
            narrative = f"## 📌 Leadership Insight\n\n"
            narrative += f"**Revenue {change_direction.upper()} by ₹{abs(analysis['revenue_change']):,.0f} ({abs(analysis['revenue_change_pct']):.1f}%)** {period_label} compared to {prev_label}.\n\n"
            
            # Add details
            narrative += f"**What Changed:**\n"
            narrative += f"- Revenue: ₹{analysis['revenue2']:,.0f} (from ₹{analysis['revenue1']:,.0f})\n"
            narrative += f"- Transaction Volume: {analysis['n_samples2']:,} ({analysis['transaction_change']:+,} transactions)\n"
            narrative += f"- Success Rate: {analysis['success_rate2']:.1f}% ({analysis['success_rate_change']:+.1f}%)\n"
            narrative += f"- Average Transaction: ₹{analysis['avg_transaction2']:,.0f} ({analysis['avg_transaction_change']:+,.0f})\n\n"
            
            # Determine primary driver
            if abs(analysis['success_rate_change']) > 1:
                driver = "success rate change"
                response['decision_suggestions'].append("Investigate and address factors causing transaction failures")
                response['decision_suggestions'].append("Review payment gateway performance and reliability")
            elif abs(analysis['transaction_change_pct']) > 5:
                driver = "transaction volume change"
                response['decision_suggestions'].append("Analyze customer engagement and retention metrics")
                response['decision_suggestions'].append("Review marketing and acquisition strategies")
            else:
                driver = "average transaction value change"
                response['decision_suggestions'].append("Examine product mix and pricing strategies")
                response['decision_suggestions'].append("Review customer purchase behavior patterns")
            
            narrative += f"**Primary Driver:** The change appears to be driven by {driver}."
            
            response['narrative'] = narrative
            response['metrics'] = analysis
            
            # Calculate confidence
            response['confidence'] = self.analytics._calculate_confidence(
                analysis['n_samples2'],
                analysis['success_rate2']
            )
            
            response['assumptions'] = [
                f"Analysis based on {analysis['n_samples2']:,} transactions in current period",
                f"Comparing to {analysis['n_samples1']:,} transactions in previous period",
                "All monetary values are in INR",
                "Only successful transactions counted as revenue"
            ]
            
        return response
    
    def _analyze_root_causes(self, current_period, comparison_period, response):
        """Identify and explain root causes"""
        causes = self.analytics.find_root_causes(current_period, comparison_period)
        
        if causes:
            period_label = self._get_period_label(current_period)
            
            narrative = f"## 📌 Leadership Insight\n\n"
            narrative += f"**Root Cause Analysis** for {period_label}:\n\n"
            narrative += "I've identified the following factors that significantly impacted revenue:\n\n"
            
            for i, cause in enumerate(causes[:5], 1):
                impact_direction = "decreased" if cause['revenue_impact'] < 0 else "increased"
                narrative += f"**{i}. {cause['dimension']}: {cause['category']}**\n"
                narrative += f"   - Revenue Impact: ₹{abs(cause['revenue_impact']):,.0f} ({impact_direction})\n"
                narrative += f"   - Success Rate Change: {cause['success_rate_change']:+.1f}% (from {cause['prev_success_rate']:.1f}% to {cause['current_success_rate']:.1f}%)\n"
                narrative += f"   - Lost Revenue: ₹{cause['lost_revenue']:,.0f}\n"
                narrative += f"   - Transaction Volume: {cause['transaction_count']:,}\n"
                narrative += f"   - Confidence: {cause['confidence']['level']} ({cause['confidence']['score']:.0f}%)\n\n"
            
            # Add summary
            total_impact = sum(abs(c['revenue_impact']) for c in causes[:5])
            narrative += f"**Summary:** These top 5 factors account for ₹{total_impact:,.0f} in revenue variation."
            
            response['narrative'] = narrative
            response['insights'] = causes
            
            # Generate decision suggestions based on top causes
            top_cause = causes[0]
            if top_cause['dimension'] == 'Region':
                response['decision_suggestions'].append(f"Prioritize operational improvements in {top_cause['category']}")
                response['decision_suggestions'].append("Deploy regional support teams to investigate local issues")
            elif top_cause['dimension'] == 'Transaction Type':
                response['decision_suggestions'].append(f"Focus on improving {top_cause['category']} transaction reliability")
                response['decision_suggestions'].append("Review and optimize payment flows for this transaction type")
            elif top_cause['dimension'] == 'Sender Bank' or top_cause['dimension'] == 'Receiver Bank':
                response['decision_suggestions'].append(f"Engage with {top_cause['category']} to address integration issues")
                response['decision_suggestions'].append("Monitor and improve bank-specific transaction success rates")
            elif top_cause['dimension'] == 'Network Type':
                response['decision_suggestions'].append(f"Optimize transaction processing for {top_cause['category']} connections")
                response['decision_suggestions'].append("Implement network-specific retry mechanisms")
            else:
                response['decision_suggestions'].append(f"Investigate operational issues in {top_cause['category']}")
                response['decision_suggestions'].append("Implement targeted monitoring and alerts")
            
            # Overall confidence (average of top causes)
            avg_confidence = sum(c['confidence']['score'] for c in causes[:3]) / min(3, len(causes))
            response['confidence'] = {
                'score': avg_confidence,
                'level': 'High' if avg_confidence >= 75 else 'Medium' if avg_confidence >= 50 else 'Low',
                'note': 'Based on transaction volume and metric stability across analyzed segments'
            }
            
        else:
            response['narrative'] = "## 📌 Leadership Insight\n\nNo significant root causes identified for the selected period."
            response['confidence'] = {'score': 50, 'level': 'Medium'}
        
        return response
    
    def _quantify_impact(self, current_period, comparison_period, response):
        """Quantify financial impact"""
        current_df = self.analytics.df[
            (self.analytics.df['date'] >= current_period[0]) & 
            (self.analytics.df['date'] <= current_period[1])
        ]
        
        actual_revenue = current_df['revenue'].sum()
        potential_revenue = current_df['potential_revenue'].sum()
        lost_revenue = potential_revenue - actual_revenue
        
        failure_count = current_df['is_failure'].sum()
        total_transactions = len(current_df)
        failure_rate = (failure_count / total_transactions * 100) if total_transactions > 0 else 0
        
        period_label = self._get_period_label(current_period)
        
        narrative = f"## 📌 Leadership Insight\n\n"
        narrative += f"**Financial Impact Analysis** for {period_label}:\n\n"
        narrative += f"**Revenue Leakage:**\n"
        narrative += f"- Actual Revenue: ₹{actual_revenue:,.0f}\n"
        narrative += f"- Potential Revenue: ₹{potential_revenue:,.0f}\n"
        narrative += f"- **Lost Revenue: ₹{lost_revenue:,.0f}**\n\n"
        
        narrative += f"**Transaction Metrics:**\n"
        narrative += f"- Total Transactions: {total_transactions:,}\n"
        narrative += f"- Failed Transactions: {failure_count:,}\n"
        narrative += f"- Failure Rate: {failure_rate:.2f}%\n"
        
        # Fraud analysis if fraud_flag column exists
        if 'fraud_flag' in current_df.columns:
            fraud_count = current_df['fraud_flag'].sum()
            fraud_rate = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
            fraud_revenue_at_risk = current_df[current_df['fraud_flag'] == 1]['amount (INR)'].sum()
            
            if fraud_count > 0:
                narrative += f"- Flagged for Review: {fraud_count:,} transactions ({fraud_rate:.2f}%)\n"
                narrative += f"- Revenue at Risk from Flagged Transactions: ₹{fraud_revenue_at_risk:,.0f}\n"
        
        narrative += "\n"
        
        # Severity assessment
        loss_pct = (lost_revenue / potential_revenue * 100) if potential_revenue > 0 else 0
        if loss_pct > 10:
            severity = "**CRITICAL**"
            severity_note = "Revenue leakage exceeds 10% of potential"
            response['decision_suggestions'].append("Immediate action required - convene cross-functional crisis team")
            response['decision_suggestions'].append("Implement emergency measures to restore transaction success rates")
        elif loss_pct > 5:
            severity = "**MODERATE**"
            severity_note = "Revenue leakage is between 5-10% of potential"
            response['decision_suggestions'].append("Schedule urgent review with operations and technology teams")
            response['decision_suggestions'].append("Prioritize initiatives to reduce transaction failures")
        else:
            severity = "**MINOR**"
            severity_note = "Revenue leakage is under 5% of potential"
            response['decision_suggestions'].append("Continue monitoring trends and maintain current improvement efforts")
            response['decision_suggestions'].append("Document learnings for future optimization")
        
        # Add fraud-specific suggestions if applicable
        if 'fraud_flag' in current_df.columns and fraud_count > 0 and fraud_rate > 1:
            response['decision_suggestions'].append(f"Review and enhance fraud detection mechanisms ({fraud_count:,} transactions flagged)")
        
        narrative += f"**Business Impact:** {severity} - {severity_note}"
        
        response['narrative'] = narrative
        response['metrics'] = {
            'actual_revenue': actual_revenue,
            'potential_revenue': potential_revenue,
            'lost_revenue': lost_revenue,
            'failure_count': failure_count,
            'total_transactions': total_transactions,
            'failure_rate': failure_rate,
            'loss_percentage': loss_pct,
            'severity': severity
        }
        
        # Add fraud metrics if available
        if 'fraud_flag' in current_df.columns:
            response['metrics']['fraud_count'] = fraud_count
            response['metrics']['fraud_rate'] = fraud_rate
            response['metrics']['fraud_revenue_at_risk'] = fraud_revenue_at_risk
        
        response['confidence'] = self.analytics._calculate_confidence(total_transactions, 100 - failure_rate)
        
        return response
    
    def _analyze_risks(self, response):
        """Identify and analyze risk segments"""
        risks = self.analytics.get_high_risk_segments(top_n=5)
        
        narrative = "**High-Risk Segment Analysis:**\n\n"
        narrative += "Based on failure rates and transaction volume, these segments require immediate attention:\n\n"
        
        for i, risk in enumerate(risks, 1):
            narrative += f"**{i}. {risk['dimension']}: {risk['category']}**\n"
            narrative += f"   - Failure Rate: {risk['failure_rate']:.1f}%\n"
            narrative += f"   - Failed Transactions: {risk['failures']:,} out of {risk['volume']:,}\n"
            narrative += f"   - Lost Revenue: ₹{risk['lost_revenue']:,.0f}\n"
            narrative += f"   - Risk Score: {risk['risk_score']:,.0f}\n\n"
        
        total_at_risk = sum(r['lost_revenue'] for r in risks)
        narrative += f"**Total Revenue at Risk:** ₹{total_at_risk:,.0f} across these high-risk segments."
        
        response['narrative'] = narrative
        response['insights'] = risks
        response['metrics'] = {'total_at_risk': total_at_risk}
        
        # Confidence based on data volume
        total_volume = sum(r['volume'] for r in risks)
        response['confidence'] = self.analytics._calculate_confidence(total_volume, 50)
        
        response['recommendations'] = [
            f"Investigate and resolve issues in {risks[0]['category']} ({risks[0]['dimension']})",
            "Implement enhanced monitoring for high-risk segments",
            "Consider temporary intervention measures to reduce failure rates",
            "Review and optimize processes in affected areas"
        ]
        
        return response
    
    def _analyze_risk_combinations(self, response):
        """Identify riskiest combinations of region, device type, and network"""
        combinations = self.analytics.get_high_risk_combinations(top_n=10)
        
        narrative = "## 📌 Leadership Insight\n\n"
        narrative += "**Multi-Dimensional Risk Combination Analysis:**\n\n"
        narrative += "These specific combinations of region, device type, and network condition pose the highest operational risk:\n\n"
        
        for i, combo in enumerate(combinations, 1):
            narrative += f"**{i}. {combo['region']} + {combo['device_type']} + {combo['network_type']}**\n"
            narrative += f"   - Failure Rate: {combo['failure_rate']:.1f}%\n"
            narrative += f"   - Failed Transactions: {combo['failed_transactions']:,} out of {combo['total_transactions']:,}\n"
            narrative += f"   - Lost Revenue: ₹{combo['lost_revenue']:,.0f}\n"
            narrative += f"   - Risk Score: {combo['risk_score']:,.0f}\n"
            narrative += f"   - Confidence: {combo['confidence']['level']} ({combo['confidence']['score']:.0f}%)\n\n"
        
        # Calculate totals
        total_at_risk = sum(c['lost_revenue'] for c in combinations)
        total_failures = sum(c['failed_transactions'] for c in combinations)
        
        narrative += f"**Summary:**\n"
        narrative += f"- Total combinations analyzed: {len(combinations)}\n"
        narrative += f"- Total failed transactions: {total_failures:,}\n"
        narrative += f"- Total revenue at risk: ₹{total_at_risk:,.0f}\n"
        
        response['narrative'] = narrative
        response['insights'] = combinations
        response['metrics'] = {
            'total_at_risk': total_at_risk,
            'total_failures': total_failures,
            'combinations_count': len(combinations)
        }
        
        # Average confidence across top combinations
        avg_confidence = sum(c['confidence']['score'] for c in combinations[:3]) / min(3, len(combinations))
        response['confidence'] = {
            'score': avg_confidence,
            'level': 'High' if avg_confidence >= 75 else 'Medium' if avg_confidence >= 50 else 'Low',
            'note': 'Based on transaction volume across multi-dimensional combinations'
        }
        
        # Specific decision suggestions
        top_combo = combinations[0]
        response['decision_suggestions'] = [
            f"Immediate priority: Address failures in {top_combo['region']} using {top_combo['device_type']} on {top_combo['network_type']} network",
            f"Deploy regional technical support for {top_combo['region']}",
            f"Optimize transaction processing for {top_combo['device_type']} devices",
            f"Investigate and improve {top_combo['network_type']} network reliability",
            "Implement targeted monitoring for these specific combinations"
        ]
        
        response['assumptions'] = [
            "Combinations with at least 100 transactions included",
            "Risk score calculated as failure_rate × lost_revenue",
            "All three dimensions analyzed simultaneously",
            "Regional, device, and network factors assumed independent"
        ]
        
        return response
    
    def _generate_counterfactual(self, current_period, comparison_period, response):
        """Generate counterfactual analysis"""
        counterfactual = self.analytics.calculate_counterfactual(current_period, comparison_period)
        
        period_label = self._get_period_label(current_period)
        prev_label = self._get_period_label(comparison_period) if comparison_period else "previous period"
        
        narrative = f"## 📌 Leadership Insight\n\n"
        narrative += f"**Counterfactual Analysis** for {period_label}:\n\n"
        narrative += f"**Scenario:** If the success rate had remained at {prev_label}'s level ({counterfactual['prev_success_rate']:.1f}%):\n\n"
        
        narrative += f"- Expected Revenue: ₹{counterfactual['counterfactual_revenue']:,.0f}\n"
        narrative += f"- Actual Revenue: ₹{counterfactual['actual_revenue']:,.0f}\n"
        narrative += f"- **Difference: ₹{abs(counterfactual['difference']):,.0f}**\n\n"
        
        if counterfactual['difference'] > 0:
            narrative += f"Revenue would have been **₹{counterfactual['difference']:,.0f} higher** if the success rate had not declined from {counterfactual['prev_success_rate']:.1f}% to {counterfactual['current_success_rate']:.1f}%."
            response['decision_suggestions'].append("Focus on restoring success rates to previous baseline levels")
            response['decision_suggestions'].append("Identify and replicate conditions from the higher-performing period")
        else:
            narrative += f"Revenue is **₹{abs(counterfactual['difference']):,.0f} higher** due to improved success rate (from {counterfactual['prev_success_rate']:.1f}% to {counterfactual['current_success_rate']:.1f}%)."
            response['decision_suggestions'].append("Document and maintain the factors driving improved success rates")
            response['decision_suggestions'].append("Share best practices across teams to sustain performance")
        
        response['narrative'] = narrative
        response['metrics'] = counterfactual
        response['confidence'] = {'score': 80, 'level': 'High', 'note': 'Counterfactual assumes all other factors remain constant'}
        response['assumptions'] = [
            "Transaction volume remains the same",
            "Average transaction amount remains constant",
            "Only success rate changes to previous period's level",
            "No external market factors considered"
        ]
        
        return response
    
    def _general_overview(self, current_period, response):
        """Provide general overview"""
        trend = self.analytics.get_revenue_trend('daily', last_n=30)
        
        latest = trend.iloc[-1]
        period_label = self._get_period_label(current_period)
        
        # Get current period data for additional insights
        current_df = self.analytics.df[
            (self.analytics.df['date'] >= current_period[0]) & 
            (self.analytics.df['date'] <= current_period[1])
        ]
        
        # Peak hour analysis
        hourly_activity = current_df.groupby('hour').agg({
            'transaction id': 'count',
            'revenue': 'sum'
        }).sort_values('transaction id', ascending=False)
        
        if len(hourly_activity) > 0:
            peak_hour = hourly_activity.index[0]
            peak_hour_txns = hourly_activity.iloc[0]['transaction id']
            
            # Get dominant merchant category during peak hour
            peak_hour_data = current_df[current_df['hour'] == peak_hour]
            top_category = peak_hour_data['merchant_category'].value_counts().index[0] if len(peak_hour_data) > 0 else 'various'
        
        narrative = f"## 📌 Leadership Insight\n\n"
        narrative += f"**Executive Summary** for {period_label}:\n\n"
        narrative += f"**Key Metrics:**\n"
        narrative += f"- Revenue: ₹{latest['revenue']:,.0f}\n"
        narrative += f"- Transactions: {latest['transaction id']:,.0f}\n"
        narrative += f"- Success Rate: {latest['success_rate']:.1f}%\n"
        narrative += f"- Revenue Leakage: ₹{latest['lost_revenue']:,.0f}\n\n"
        
        # 7-day trend
        last_7 = trend.tail(7)
        avg_revenue = last_7['revenue'].mean()
        avg_success = last_7['success_rate'].mean()
        
        narrative += f"**7-Day Trend:**\n"
        narrative += f"- Average Daily Revenue: ₹{avg_revenue:,.0f}\n"
        narrative += f"- Average Success Rate: {avg_success:.1f}%\n\n"
        
        # Peak hour insight
        if len(hourly_activity) > 0:
            peak_end = peak_hour + 2 if peak_hour < 22 else 23
            narrative += f"**Transaction Patterns:**\n"
            narrative += f"- Peak activity occurred between {peak_hour}:00–{peak_end}:00, "
            narrative += f"with {peak_hour_txns:,} transactions\n"
            narrative += f"- Driven primarily by {top_category} category\n"
        
        response['narrative'] = narrative
        response['metrics'] = {
            'latest_revenue': latest['revenue'],
            'latest_transactions': latest['transaction id'],
            'latest_success_rate': latest['success_rate'],
            'avg_7day_revenue': avg_revenue,
            'avg_7day_success': avg_success,
            'peak_hour': peak_hour if len(hourly_activity) > 0 else None,
            'peak_hour_volume': peak_hour_txns if len(hourly_activity) > 0 else 0
        }
        response['confidence'] = self.analytics._calculate_confidence(latest['transaction id'], latest['success_rate'])
        
        response['decision_suggestions'] = [
            f"Monitor peak hour ({peak_hour}:00–{peak_end}:00) for capacity planning" if len(hourly_activity) > 0 else "Review transaction patterns for optimization opportunities",
            "Track success rate trends to identify early warning signs"
        ]
        
        return response
    
    def _get_period_label(self, period: Tuple) -> str:
        """Generate human-readable period label"""
        if period[0] == period[1]:
            return period[0].strftime('%B %d, %Y')
        else:
            return f"{period[0].strftime('%B %d')} - {period[1].strftime('%B %d, %Y')}"


def load_data():
    """Load and cache the transaction data"""
    if 'data' not in st.session_state:
        with st.spinner('Loading transaction data...'):
            df = pd.read_csv('./data/upi_transactions_2024.csv')
            # Ensure timestamp is datetime type
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            st.session_state.data = df
            st.session_state.analytics = DataAnalytics(df)
            st.session_state.ai = ConversationalAI(st.session_state.analytics)
    
    return st.session_state.data, st.session_state.analytics, st.session_state.ai


def main():
    """Main application"""
    
    # Minimal header
    st.markdown("""
    <div style="
        padding: 2rem 0 1rem 0;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h1 style="
            font-size: 2rem;
            font-weight: 600;
            color: #111827;
            margin: 0 0 0.5rem 0;
        ">💼 Strategic CFO Assistant</h1>
        <p style="
            font-size: 0.95rem;
            color: #6b7280;
            margin: 0;
            font-weight: 400;
            line-height: 1.5;
        ">Leadership-level financial insights through natural language conversation</p>
        <p style="
            font-size: 0.85rem;
            color: #9ca3af;
            margin: 0.25rem 0 0 0;
        ">Converting digital payment data into conversational insights aligned with InsightX</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df, analytics, ai = load_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="
            padding: 1rem 0 0.5rem 0;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 1rem;
        ">
            <h2 style="color: #374151; font-size: 1.1rem; margin: 0; font-weight: 600;">📊 Dataset Overview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Total Transactions", f"{len(df):,}")
        st.metric("Date Range", f"{df['timestamp'].min().strftime('%b %d')} - {df['timestamp'].max().strftime('%b %d, %Y')}")
        
        total_revenue = df[df['transaction_status'] == 'SUCCESS']['amount (INR)'].sum()
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
        
        success_rate = (df['transaction_status'] == 'SUCCESS').mean() * 100
        st.metric("Overall Success Rate", f"{success_rate:.1f}%")
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            padding: 1rem 0 0.5rem 0;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 1rem;
        ">
            <h2 style="color: #374151; font-size: 1.1rem; margin: 0; font-weight: 600;">💡 Try These Questions</h2>
        </div>
        """, unsafe_allow_html=True)
        example_questions = [
            "Why did revenue drop last week?",
            "Which regions caused the biggest loss?",
            "What are the high-risk segments?",
            "How much money are we losing to failures?",
            "If success rate hadn't declined, what would revenue be?",
            "Show me transaction trends",
            "What's causing the revenue decline?",
            "Analyze last month's performance"
        ]
        
        for q in example_questions:
            if st.button(q, key=f"example_{hash(q)}", use_container_width=True):
                st.session_state.user_query = q
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            padding: 1rem 0 0.5rem 0;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 0.75rem;
        ">
            <h2 style="color: #374151; font-size: 1.1rem; margin: 0 0 0.25rem 0; font-weight: 600;">📉 Quick Scenarios</h2>
            <p style="font-size: 0.8rem; color: #6b7280; margin: 0;">One-click guided analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📉 Analyze Last Week Revenue Drop", key="scenario_revenue_drop", use_container_width=True):
            st.session_state.user_query = "Why did revenue drop last week? Show me the root causes and financial impact."
        
        if st.button("🎯 High-Risk Assessment", key="scenario_risk", use_container_width=True):
            st.session_state.user_query = "What are our highest risk segments and how much revenue is at stake?"
        
        if st.button("💰 Revenue Leakage Analysis", key="scenario_leakage", use_container_width=True):
            st.session_state.user_query = "How much money are we losing to transaction failures and what's the business impact?"
        
        st.divider()
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            if 'messages' in st.session_state:
                st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "data" in message:
                # Display metrics
                if "metrics" in message["data"]:
                    cols = st.columns(4)
                    metrics = message["data"]["metrics"]
                    
                    if 'revenue2' in metrics:
                        cols[0].metric("Revenue", f"₹{metrics['revenue2']:,.0f}", 
                                     delta=f"{metrics['revenue_change_pct']:+.1f}%")
                        cols[1].metric("Success Rate", f"{metrics['success_rate2']:.1f}%",
                                     delta=f"{metrics['success_rate_change']:+.1f}%")
                    
                    if 'lost_revenue' in metrics:
                        cols[2].metric("Lost Revenue", f"₹{metrics['lost_revenue']:,.0f}")
                    
                # Display confidence
                if "confidence" in message["data"]:
                    conf = message["data"]["confidence"]
                    # Handle both dict and potential missing keys
                    if isinstance(conf, dict) and 'level' in conf and 'score' in conf:
                        conf_class = f"confidence-{conf['level'].lower()}"
                        st.markdown(f"**Confidence:** <span class='{conf_class}'>{conf['level']} ({conf['score']:.0f}%)</span>", 
                                  unsafe_allow_html=True)
                        
                        if 'factors' in conf:
                            st.caption(f"Based on: Sample Size ({conf['factors']['sample_size']}), Stability ({conf['factors']['stability']})")
                        elif 'note' in conf:
                            st.caption(conf['note'])
                
                # Display assumptions
                if "assumptions" in message["data"] and message["data"]["assumptions"]:
                    with st.expander("📋 Assumptions & Limitations"):
                        for assumption in message["data"]["assumptions"]:
                            st.write(f"• {assumption}")
                
                # Display recommendations
                if "recommendations" in message["data"] and message["data"]["recommendations"]:
                    with st.expander("💡 Recommendations"):
                        for rec in message["data"]["recommendations"]:
                            st.write(f"• {rec}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your business metrics...") or st.session_state.get('user_query'):
        if st.session_state.get('user_query'):
            prompt = st.session_state.user_query
            st.session_state.user_query = None
        
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = ai.generate_response(prompt)
                
                # Show context summary if available
                if response.get('context_summary'):
                    st.info(response['context_summary'])
                
                st.markdown(response['narrative'])
                
                # Display metrics
                if response.get('metrics'):
                    cols = st.columns(4)
                    metrics = response['metrics']
                    
                    if 'revenue2' in metrics:
                        cols[0].metric("Revenue", f"₹{metrics['revenue2']:,.0f}", 
                                     delta=f"{metrics['revenue_change_pct']:+.1f}%")
                        cols[1].metric("Success Rate", f"{metrics['success_rate2']:.1f}%",
                                     delta=f"{metrics['success_rate_change']:+.1f}%")
                    
                    if 'lost_revenue' in metrics:
                        cols[2].metric("Lost Revenue", f"₹{metrics['lost_revenue']:,.0f}")
                    
                    if 'actual_revenue' in metrics:
                        cols[0].metric("Actual Revenue", f"₹{metrics['actual_revenue']:,.0f}")
                        cols[1].metric("Potential Revenue", f"₹{metrics['potential_revenue']:,.0f}")
                        cols[2].metric("Lost Revenue", f"₹{metrics['lost_revenue']:,.0f}")
                        cols[3].metric("Failure Rate", f"{metrics['failure_rate']:.2f}%")
                
                # Display confidence
                if response.get('confidence'):
                    conf = response['confidence']
                    # Handle both dict and potential missing keys
                    if isinstance(conf, dict) and 'level' in conf and 'score' in conf:
                        conf_class = f"confidence-{conf['level'].lower()}"
                        st.markdown(f"**Confidence:** <span class='{conf_class}'>{conf['level']} ({conf['score']:.0f}%)</span>", 
                                  unsafe_allow_html=True)
                        
                        if 'factors' in conf:
                            st.caption(f"Based on: Sample Size ({conf['factors']['sample_size']}), Stability ({conf['factors']['stability']})")
                        elif 'note' in conf:
                            st.caption(conf['note'])
                
                # Display decision suggestions
                if response.get('decision_suggestions'):
                    with st.expander("🎯 Decision Suggestions", expanded=False):
                        st.caption("*These are strategic suggestions, not automated actions. Final decisions remain with leadership.*")
                        for sug in response['decision_suggestions']:
                            st.write(f"• {sug}")
                
                # Display assumptions
                if response.get('assumptions'):
                    with st.expander("📋 Assumptions & Limitations"):
                        for assumption in response['assumptions']:
                            st.write(f"• {assumption}")
                
                # Display recommendations
                if response.get('recommendations'):
                    with st.expander("💡 Recommendations"):
                        for rec in response['recommendations']:
                            st.write(f"• {rec}")
                
                # Store assistant message
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response['narrative'],
                    "data": response
                })


if __name__ == "__main__":
    main()
    
    # Minimal footer
    st.markdown("""
    <div style="
        border-top: 1px solid #e5e7eb;
        padding: 2rem 0 1rem 0;
        text-align: center;
        margin-top: 3rem;
    ">
        <p style="
            color: #9ca3af;
            font-size: 0.85rem;
            margin: 0;
        ">This prototype demonstrates representative analytics on synthetic data.</p>
        <p style="
            color: #d1d5db;
            font-size: 0.75rem;
            margin: 0.5rem 0 0 0;
        ">Strategic CFO Assistant v1.0 • Built for InsightX</p>
    </div>
    """, unsafe_allow_html=True)
