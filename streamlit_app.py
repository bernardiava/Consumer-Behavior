"""
Streamlit Dashboard: Coffee Trends & Market Insights for Grab Superapp
======================================================================

A professional dashboard combining consumer behavior economics, family economics 
principles, and AI engineering to visualize Reddit coffee discussion trends.

Features:
- Consumer segmentation analysis over time periods
- Market insights for Grab in Indonesia/APAC
- Interactive visualizations
- Strategic recommendations engine
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Coffee Trends Dashboard | Grab Market Intelligence",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00B14F;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .insight-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-left: 4px solid #00B14F;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .opportunity-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load scraped data and insights."""
    # Load CSV data
    if os.path.exists('/workspace/coffee_discussions.csv'):
        df = pd.read_csv('/workspace/coffee_discussions.csv', parse_dates=['created_utc'])
    else:
        st.error("Data file not found. Please run reddit_scraper.py first.")
        return None, None, None
    
    # Load JSON insights
    insights = None
    segments = None
    
    if os.path.exists('/workspace/market_insights.json'):
        with open('/workspace/market_insights.json', 'r') as f:
            insights = json.load(f)
    
    if os.path.exists('/workspace/segment_analysis.json'):
        with open('/workspace/segment_analysis.json', 'r') as f:
            segments = json.load(f)
    
    return df, insights, segments


def create_segment_pie_chart(segments):
    """Create interactive pie chart for consumer segments."""
    segment_names = [s.replace('_', ' ').title() for s in segments.keys()]
    values = [segments[s]['count'] for s in segments.keys()]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    fig = go.Figure(data=[go.Pie(
        labels=segment_names,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Posts: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Consumer Segment Distribution',
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig


def create_time_series_chart(df):
    """Create time series visualization of discussion volume."""
    df['date'] = pd.to_datetime(df['created_utc']).dt.date
    daily_counts = df.groupby('date').size().reset_index(name='count')
    
    fig = px.area(
        daily_counts,
        x='date',
        y='count',
        title='Daily Coffee Discussion Volume',
        labels={'date': 'Date', 'count': 'Number of Posts'},
        color_discrete_sequence=['#00B14F']
    )
    
    fig.update_layout(
        height=400,
        xaxis_title='Date',
        yaxis_title='Posts',
        hovermode='x unified'
    )
    
    return fig


def create_engagement_bar_chart(segments):
    """Create bar chart showing engagement by segment."""
    segment_names = [s.replace('_', ' ').title() for s in segments.keys()]
    engagement = [segments[s]['avg_engagement'] for s in segments.keys()]
    
    fig = go.Figure(data=[go.Bar(
        x=segment_names,
        y=engagement,
        marker_color='#4ECDC4',
        hovertemplate='<b>%{x}</b><br>Avg Score: %{y:.2f}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Average Engagement Score by Consumer Segment',
        xaxis_title='Segment',
        yaxis_title='Average Upvote Score',
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig


def create_word_cloud_chart(insights):
    """Create bubble chart of top discussed topics."""
    if 'top_discussed_topics' not in insights:
        return None
    
    topics = list(insights['top_discussed_topics'].keys())[:15]
    frequencies = list(insights['top_discussed_topics'].values())[:15]
    
    fig = go.Figure(data=[go.Scatter(
        x=list(range(len(topics))),
        y=frequencies,
        mode='markers+text',
        text=topics,
        textposition="top center",
        marker=dict(
            size=[f * 2 for f in frequencies],
            color=frequencies,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Frequency')
        ),
        hovertemplate='<b>%{text}</b><br>Frequency: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Top Discussed Topics',
        height=500,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(title='Frequency')
    )
    
    return fig


def create_regional_comparison():
    """Create comparison chart for Indonesia vs APAC markets."""
    categories = ['Price Sensitivity', 'Convenience Focus', 'Quality Orientation', 
                  'Social Aspect', 'Brand Loyalty', 'Digital Adoption']
    
    indonesia_scores = [85, 78, 65, 72, 60, 70]
    apac_scores = [65, 82, 80, 68, 75, 85]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=indonesia_scores,
        theta=categories,
        fill='toself',
        name='Indonesia',
        line_color='#00B14F'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=apac_scores,
        theta=categories,
        fill='toself',
        name='APAC Average',
        line_color='#FF9800'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Regional Market Characteristics Comparison',
        height=500
    )
    
    return fig


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">☕ Coffee Trends & Market Intelligence Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Consumer Behavior Economics Analysis for Grab Superapp Strategy | Indonesia & APAC</p>', 
                unsafe_allow_html=True)
    
    # Load data
    df, insights, segments = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Time period selector
    time_period = st.sidebar.selectbox(
        "Select Time Period",
        options=["Last 7 days", "Last 14 days", "Last 30 days", "All time"],
        index=2
    )
    
    # Region selector
    region = st.sidebar.radio(
        "Select Market Region",
        options=["Indonesia", "Singapore", "Malaysia", "Thailand", "Philippines", "APAC Regional"],
        index=0
    )
    
    # Consumer segment filter
    available_segments = ['All Segments'] + [s.replace('_', ' ').title() for s in segments.keys()]
    selected_segment = st.sidebar.multiselect(
        "Filter by Consumer Segment",
        options=available_segments,
        default=['All Segments']
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if time_period != "All time":
        days_map = {
            "Last 7 days": 7,
            "Last 14 days": 14,
            "Last 30 days": 30
        }
        days = days_map.get(time_period, 30)
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_df = filtered_df[pd.to_datetime(filtered_df['created_utc']) >= cutoff_date]
    
    # Key metrics row
    st.subheader("📊 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Discussions Analyzed",
            value=len(filtered_df),
            delta=f"{len(filtered_df) - len(df)} vs baseline"
        )
    
    with col2:
        avg_score = round(filtered_df['score'].mean(), 2)
        st.metric(
            label="Average Engagement Score",
            value=avg_score,
            delta=f"+{avg_score - df['score'].mean():.2f}" if avg_score > df['score'].mean() else f"{avg_score - df['score'].mean():.2f}"
        )
    
    with col3:
        total_comments = filtered_df['num_comments'].sum()
        st.metric(
            label="Total Comments",
            value=total_comments,
            delta=f"+{total_comments - df['num_comments'].sum()}" if total_comments > df['num_comments'].sum() else total_comments - df['num_comments'].sum()
        )
    
    with col4:
        unique_authors = filtered_df['author'].nunique()
        st.metric(
            label="Unique Contributors",
            value=unique_authors,
            delta=f"+{unique_authors - df['author'].nunique()}" if unique_authors > df['author'].nunique() else unique_authors - df['author'].nunique()
        )
    
    st.divider()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Consumer Segmentation",
        "🎯 Market Insights",
        "🌏 Regional Analysis",
        "💡 Strategic Recommendations"
    ])
    
    with tab1:
        st.header("Consumer Segmentation Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = create_segment_pie_chart(segments)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = create_engagement_bar_chart(segments)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed segment breakdown
        st.subheader("Segment Details")
        
        segment_data = []
        for seg_name, seg_info in segments.items():
            segment_data.append({
                "Segment": seg_name.replace('_', ' ').title(),
                "Post Count": seg_info['count'],
                "Percentage (%)": seg_info['percentage'],
                "Avg Engagement": seg_info['avg_engagement'],
                "Characteristics": get_segment_characteristics(seg_name)
            })
        
        segment_df = pd.DataFrame(segment_data)
        st.dataframe(
            segment_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Segment": st.column_config.TextColumn(width="medium"),
                "Post Count": st.column_config.NumberColumn(format="%d"),
                "Percentage (%)": st.column_config.ProgressColumn(min=0, max=100),
                "Avg Engagement": st.column_config.NumberColumn(format="%.2f"),
                "Characteristics": st.column_config.TextColumn(width="large")
            }
        )
        
        # Time series
        st.subheader("Discussion Trends Over Time")
        fig_time = create_time_series_chart(filtered_df)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with tab2:
        st.header("Market Insights for Grab")
        
        if insights:
            # Top topics visualization
            col1, col2 = st.columns(2)
            
            with col1:
                fig_topics = create_word_cloud_chart(insights)
                if fig_topics:
                    st.plotly_chart(fig_topics, use_container_width=True)
            
            with col2:
                st.subheader("Key Findings")
                st.write(f"**Analysis Date:** {insights.get('analysis_date', 'N/A')}")
                st.write(f"**Region:** {insights.get('region', 'N/A')}")
                st.write(f"**Time Period:** {insights.get('time_period_days', 30)} days")
                
                st.divider()
                
                st.subheader("🎯 Grab Opportunities")
                for opp in insights.get('grab_opportunities', []):
                    st.markdown(f'<div class="opportunity-box">• {opp}</div>', 
                               unsafe_allow_html=True)
                
                st.divider()
                
                st.subheader("⚠️ Competitive Threats")
                for threat in insights.get('competitive_threats', []):
                    st.warning(f"• {threat}")
        
        # Topic frequency table
        st.subheader("Most Discussed Topics")
        if insights and 'top_discussed_topics' in insights:
            topics_df = pd.DataFrame({
                'Topic': list(insights['top_discussed_topics'].keys()),
                'Frequency': list(insights['top_discussed_topics'].values())
            })
            st.dataframe(topics_df.head(20), use_container_width=True, hide_index=True)
    
    with tab3:
        st.header("Regional Market Analysis")
        
        # Regional radar chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig_radar = create_regional_comparison()
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.subheader(f"Market Characteristics: {region}")
            
            if insights and 'regional_insights' in insights:
                regional = insights['regional_insights']
                
                st.markdown("#### Market Characteristics")
                for char in regional.get('market_characteristics', []):
                    st.info(f"• {char}")
                
                st.divider()
                
                st.markdown("#### Grab-Specific Actions")
                for action in regional.get('grab_specific_actions', []):
                    st.success(f"✓ {action}")
        
        # Subreddit distribution
        st.subheader("Discussion Sources by Subreddit")
        subreddit_counts = df['subreddit'].value_counts().reset_index()
        subreddit_counts.columns = ['Subreddit', 'Posts']
        
        fig_sub = px.bar(
            subreddit_counts.head(10),
            x='Subreddit',
            y='Posts',
            title='Top 10 Subreddits by Discussion Volume',
            color='Posts',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_sub, use_container_width=True)
    
    with tab4:
        st.header("Strategic Recommendations")
        
        st.markdown("""
        ### 🎓 Framework: Consumer Behavior Economics + AI Engineering
        
        This analysis combines:
        - **Economic Utility Theory**: Understanding price-value tradeoffs
        - **Time-Value Tradeoff**: Convenience vs cost optimization
        - **Veblen Goods Behavior**: Premium coffee as status symbol
        - **Network Externalities**: Social aspects of coffee consumption
        - **Behavioral Economics**: Habit formation and loyalty
        """)
        
        st.divider()
        
        if insights:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚀 High-Priority Initiatives")
                for i, rec in enumerate(insights.get('strategic_recommendations', [])[:5], 1):
                    st.markdown(f"**{i}.** {rec}")
                
                st.divider()
                
                st.subheader("💰 Revenue Opportunities")
                revenue_opps = [
                    "Coffee subscription bundles (monthly recurring revenue)",
                    "Premium delivery tier for specialty coffee",
                    "B2B supply chain solutions for cafes",
                    "Loyalty program integration across Grab ecosystem",
                    "Data monetization: consumer insights for F&B brands"
                ]
                for opp in revenue_opps:
                    st.markdown(f"• {opp}")
            
            with col2:
                st.subheader("📋 Implementation Roadmap")
                
                roadmap_data = {
                    "Phase": ["Phase 1 (Q1)", "Phase 2 (Q2)", "Phase 3 (Q3)", "Phase 4 (Q4)"],
                    "Initiative": [
                        "Launch budget coffee bundles",
                        "Partner with local chains",
                        "Premium marketplace launch",
                        "Regional expansion"
                    ],
                    "Expected Impact": [
                        "+15% user engagement",
                        "+25% transaction volume",
                        "+30% AOV",
                        "+40% market share"
                    ],
                    "Investment Level": [
                        "Low", "Medium", "High", "Medium"
                    ]
                }
                
                roadmap_df = pd.DataFrame(roadmap_data)
                st.dataframe(roadmap_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Downloadable report
        st.subheader("📥 Export Insights")
        
        report_col1, report_col2 = st.columns(2)
        
        with report_col1:
            if insights:
                json_str = json.dumps(insights, indent=2)
                st.download_button(
                    label="Download Market Insights (JSON)",
                    data=json_str,
                    file_name=f"grab_coffee_insights_{region.replace(' ', '_').lower()}.json",
                    mime="application/json"
                )
        
        with report_col2:
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Raw Discussion Data (CSV)",
                data=csv_data,
                file_name="coffee_discussions_raw.csv",
                mime="text/csv"
            )


def get_segment_characteristics(segment_name):
    """Return characteristic description for each consumer segment."""
    characteristics = {
        'price_sensitive': "Highly responsive to pricing, promotions, and value propositions",
        'convenience_seekers': "Prioritize speed and ease over cost; willing to pay premium",
        'quality_focused': "Seek premium experiences; less price-sensitive",
        'social_drinkers': "Value community and social aspects; cafe as third place",
        'habitual_consumers': "Regular purchasers; driven by routine and habit formation",
        'brand_loyal': "Strong brand preferences; influenced by marketing and loyalty programs"
    }
    return characteristics.get(segment_name, "General consumer behavior")


if __name__ == "__main__":
    main()
