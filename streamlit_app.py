import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Grab Coffee Intelligence Dashboard",
    page_icon="☕",
    layout="wide"
)

# Load Data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    try:
        df = pd.read_csv('coffee_discussions.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("🚨 Data file not found. Please run `python scraper.py` first to collect live data.")
        return None

@st.cache_data(ttl=3600)
def load_insights():
    try:
        with open('market_insights.json', 'r') as f:
            return json.load(f)
    except:
        return {}

df = load_data()
insights = load_insights()

if df is not None:
    # Header
    st.title("☕ APAC Coffee Consumer Intelligence")
    st.markdown("**Strategic Dashboard for Grab Superapp** | *Live Data from Hacker News, RSS Feeds & Google News*")
    st.caption(f"Last updated: {df['date'].max().strftime('%Y-%m-%d')} | Total articles: {len(df):,}")
    st.divider()

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    
    # Time Period
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = st.sidebar.date_input(
        "Select Period",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    # Region Filter
    regions = ['All'] + sorted(df['region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Market Region", regions)
    
    # Segment Filter
    segments = ['All'] + sorted(df['consumer_segment'].unique().tolist())
    selected_segment = st.sidebar.selectbox("Consumer Segment", segments)
    
    # Source Filter
    sources = ['All'] + sorted(df['source'].unique().tolist())
    selected_source = st.sidebar.selectbox("Data Source", sources)

    # Apply Filters
    mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
    if selected_region != 'All':
        mask &= (df['region'] == selected_region)
    if selected_segment != 'All':
        mask &= (df['consumer_segment'] == selected_segment)
    if selected_source != 'All':
        mask &= (df['source'] == selected_source)
    
    filtered_df = df[mask].copy()

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Articles", f"{len(filtered_df):,}")
    with col2:
        avg_sentiment = filtered_df['sentiment_score'].mean()
        delta = "Positive ↑" if avg_sentiment > 0 else "Negative ↓"
        st.metric("Avg Sentiment", f"{avg_sentiment:.3f}", delta=delta)
    with col3:
        total_engagement = filtered_df['engagement_score'].sum()
        st.metric("Total Engagement", f"{total_engagement:,}")
    with col4:
        top_topic = filtered_df['topic'].mode()[0] if not filtered_df.empty else "N/A"
        st.metric("Trending Topic", top_topic[:25])

    st.divider()

    # Main Charts Row 1
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📈 Discussion Volume & Sentiment Trend")
        if len(filtered_df) > 0:
            trend_df = filtered_df.groupby(filtered_df['date'].dt.to_period('D').astype(str)).agg({
                'sentiment_score': 'mean',
                'engagement_score': 'sum'
            }).reset_index()
            trend_df['date'] = pd.to_datetime(trend_df['date'])
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(
                x=trend_df['date'], 
                y=trend_df['engagement_score'], 
                name='Engagement', 
                marker_color='#00B14F', 
                opacity=0.4
            ))
            fig_trend.add_trace(go.Scatter(
                x=trend_df['date'], 
                y=trend_df['sentiment_score'], 
                name='Sentiment Score', 
                line=dict(color='#FF5A5F', width=3),
                yaxis='y2'
            ))
            fig_trend.update_layout(
                height=400, 
                margin=dict(l=20, r=20, t=20, b=20), 
                hovermode='x unified',
                yaxis=dict(title='Engagement'),
                yaxis2=dict(title='Sentiment', overlaying='y', side='right', range=[-1, 1])
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No data for selected filters")

    with c2:
        st.subheader("👥 Consumer Segmentation")
        if len(filtered_df) > 0:
            seg_counts = filtered_df['consumer_segment'].value_counts()
            fig_pie = px.pie(
                values=seg_counts.values, 
                names=seg_counts.index, 
                hole=0.4, 
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

    # Main Charts Row 2
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("🌏 Regional Distribution & Topics")
        if len(filtered_df) > 0:
            if selected_region == 'All':
                heat_df = filtered_df.groupby(['region', 'topic']).size().reset_index(name='count')
                fig_heat = px.treemap(
                    heat_df, 
                    path=['region', 'topic'], 
                    values='count', 
                    color='count', 
                    color_continuous_scale='RdBu',
                    title='Regional Topic Intensity'
                )
                fig_heat.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_heat, use_container_width=True)
            else:
                bar_df = filtered_df['topic'].value_counts().head(10).reset_index()
                bar_df.columns = ['Topic', 'Count']
                fig_bar = px.bar(
                    bar_df, 
                    x='Count', 
                    y='Topic', 
                    orientation='h', 
                    color='Count', 
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_bar, use_container_width=True)

    with c4:
        st.subheader("💡 Strategic Insights for Grab")
        if insights:
            st.success(f"**Key Finding:** {insights['key_findings']['price_sensitivity']}")
            st.info(f"**Opportunity:** {insights['key_findings']['convenience_demand']}")
            
            st.markdown("### 🚀 Recommended Actions")
            for i, rec in enumerate(insights['strategic_recommendations'], 1):
                st.markdown(f"{i}. {rec}")
            
            st.markdown("---")
            st.markdown("**Top Topics:**")
            for topic, count in list(insights.get('top_topics', {}).items())[:3]:
                st.write(f"• {topic}: {count} articles")
        else:
            st.warning("Insights data missing. Re-run scraper.")

    # Source Breakdown
    st.divider()
    st.subheader("📊 Data Sources Breakdown")
    source_df = filtered_df['source'].value_counts().reset_index()
    source_df.columns = ['Source', 'Articles']
    fig_source = px.bar(source_df, x='Source', y='Articles', color='Articles', color_continuous_scale='Viridis')
    fig_source.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_source, use_container_width=True)

    # Raw Data Expander
    with st.expander("📄 View Raw Article Data"):
        display_cols = ['date', 'source', 'region', 'topic', 'consumer_segment', 'sentiment_score', 'engagement_score', 'title']
        st.dataframe(
            filtered_df[display_cols].sort_values('date', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f'grab_coffee_intelligence_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )

else:
    st.warning("⏳ Waiting for data... Run the scraper first:")
    st.code("python scraper.py", language="bash")
    st.info("This scraper uses FREE sources: Hacker News API, RSS feeds, and Google News RSS - No API keys required!")
