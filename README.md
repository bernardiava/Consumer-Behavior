# Coffee Trends & Market Intelligence Dashboard

## ☕ Reddit Coffee Discussion Analyzer for Grab Superapp Strategy

A professional-grade analytics platform combining **consumer behavior economics**, **family economics principles**, and **AI engineering** to extract actionable market insights from Reddit coffee discussions.

### Features

- **Reddit Data Scraping**: Automated collection of coffee-related discussions from global and APAC-specific subreddits
- **Consumer Segmentation**: AI-powered classification into 6 behavioral segments:
  - Price Sensitive (Economic Utility Theory)
  - Convenience Seekers (Time-Value Tradeoff)
  - Quality Focused (Veblen Goods Behavior)
  - Social Drinkers (Network Externalities)
  - Habitual Consumers (Behavioral Economics)
  - Brand Loyal (Marketing Psychology)
- **Market Insights**: Strategic recommendations for Grab's superapp expansion in Indonesia/APAC
- **Interactive Dashboard**: Streamlit-powered visualization with filtering by time period, region, and segment

### Files

| File | Description |
|------|-------------|
| `reddit_scraper.py` | Reddit API scraper with consumer behavior analysis engine |
| `streamlit_app.py` | Interactive dashboard for data visualization |
| `coffee_discussions.csv` | Raw scraped discussion data |
| `market_insights.json` | Generated market insights and recommendations |
| `segment_analysis.json` | Consumer segmentation results |

### Quick Start

```bash
# Install dependencies
pip install praw streamlit pandas plotly numpy

# Run the scraper to collect data
python reddit_scraper.py

# Launch the Streamlit dashboard
streamlit run streamlit_app.py
```

### Dashboard Access

Once running, access the dashboard at:
- **Local**: http://localhost:8501
- **Network**: http://[YOUR_IP]:8501

### Key Insights for Grab

Based on the analysis:

#### 🎯 Opportunities Identified
1. **High price sensitivity** (78.67%): Launch budget coffee bundle subscriptions
2. **Strong convenience preference** (36%): Optimize GrabExpress for <15min delivery
3. **Growing quality consciousness** (54.67%): Curate premium specialty marketplace

#### 📋 Strategic Recommendations
- Introduce 'Coffee Pass' - unlimited monthly coffee from partner warungs
- Partner with offices for bulk morning coffee delivery subscriptions
- Launch 'Grab Coffee Reserve' - direct trade with Indonesian farmers

#### ⚠️ Competitive Threats
- Gojek's strong presence in Indonesia F&B delivery
- Direct cafe apps offering loyalty programs
- Traditional retail expansion (Alfamart, Indomaret)

### Regional Coverage

- **Indonesia** (Jakarta, Bali)
- **Singapore**
- **Malaysia**
- **Thailand**
- **Philippines**
- **APAC Regional Analysis**

### Configuration

To use real Reddit API (instead of demo mode):

```python
# Set environment variables or pass credentials directly
export PRAW_REDDIT_CLIENT_ID="your_client_id"
export PRAW_REDDIT_CLIENT_SECRET="your_client_secret"

# Or in code:
scraper = RedditCoffeeScraper(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="your_app_name"
)
```

### Academic Framework

This tool applies principles from:
- **Consumer Behavior Economics**: Understanding purchase decision drivers
- **Family Economics**: Household spending patterns and budget allocation
- **Behavioral Economics**: Habit formation and choice architecture
- **AI/ML Engineering**: NLP-based sentiment and topic analysis

---

Built with ❤️ for Grab's market intelligence team
