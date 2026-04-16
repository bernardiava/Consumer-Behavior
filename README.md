# ☕ APAC Coffee Consumer Intelligence Dashboard

**Strategic Market Insights for Grab Superapp** - Powered by FREE data sources (No API keys required)

## 📋 Overview

This tool scrapes **free, publicly available data** from:
- **Hacker News** (JSON API - no auth needed)
- **RSS Feeds** from coffee industry publications
- **Google News RSS** for regional APAC news

It applies a **behavioral economics framework** to classify consumers and generate strategic insights for Grab's coffee market strategy in Indonesia/APAC.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install streamlit pandas plotly feedparser requests textblob beautifulsoup4
```

### 2. Run the Scraper (Collect Live Data)

```bash
python scraper.py
```

This will:
- Scrape Hacker News top stories for coffee discussions
- Fetch articles from 5+ coffee industry RSS feeds
- Pull regional news from Google News RSS (Indonesia, Singapore, APAC)
- Classify each article by consumer segment using behavioral markers
- Generate sentiment scores and engagement metrics
- Save results to `coffee_discussions.csv` and `market_insights.json`

### 3. Launch the Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard will open at `http://localhost:8501`

## 🎯 Features

### Consumer Segmentation (Behavioral Economics Framework)
- **Price Sensitive**: Detects promo/discount language (critical in Indonesia)
- **Quality Focused**: Identifies specialty coffee enthusiasts
- **Convenience Seekers**: Flags delivery/app-related discussions (GrabFood opportunity)
- **Social Drinkers**: Finds cafe hangout/work-from-cafe mentions
- **Habitual Consumers**: Recognizes daily routine/addiction patterns
- **Brand Loyal**: Tracks brand-specific loyalty signals

### Market Insights for Grab
- Regional sentiment analysis (Indonesia, Singapore, Malaysia, Thailand, Vietnam, Philippines)
- Topic trend detection (pricing, delivery, new openings, innovation)
- Strategic recommendations auto-generated based on segment distribution
- Competitive intelligence on local chains (Kopi Kenangan, Janji Jiwa, etc.)

### Interactive Dashboard
- Filter by time period, region, consumer segment, and data source
- Visualize trends with Plotly charts (time series, treemaps, pie charts)
- Download filtered datasets as CSV
- Real-time strategic insights panel

## 📁 Files

| File | Description |
|------|-------------|
| `scraper.py` | Main scraping engine (Hacker News + RSS + Google News) |
| `streamlit_app.py` | Interactive dashboard for market analysis |
| `coffee_discussions.csv` | Scraped data output |
| `market_insights.json` | Auto-generated strategic insights |

## 🔍 Data Sources (All Free, No API Keys)

### Hacker News
- Endpoint: `https://hacker-news.firebaseio.com/v0/topstories.json`
- Searches for coffee-related discussions in tech community

### RSS Feeds
- Perfect Daily Grind (specialty coffee news)
- Barista Magazine
- Sprudge (global coffee culture)
- TechCrunch (coffee tech/startups)
- Food Navigator Asia (F&B industry trends)

### Google News RSS
- Custom queries for: "coffee price Indonesia", "Grab coffee delivery", "Kopi Kenangan"
- Region-specific feeds (ID, SG, MY, TH, VN, PH)

## 💡 Strategic Use Cases for Grab

1. **Product Development**: Identify unmet needs in Price Sensitive segment → Launch subscription bundles
2. **Marketing Campaigns**: Target Convenience Seekers with time-sensitive promotions
3. **Partnership Strategy**: Partner with cafes popular among Social Drinkers
4. **Regional Expansion**: Prioritize markets with high positive sentiment
5. **Competitive Intelligence**: Monitor local brand mentions vs international chains

## ⚠️ Notes

- **Rate Limiting**: Built-in delays prevent blocking (0.3-0.5s between requests)
- **Data Freshness**: Re-run scraper daily for latest insights
- **Network Required**: Active internet connection needed for scraping
- **No Storage**: Data is not persisted beyond CSV/JSON files (run scraper each session)

## 🛠 Troubleshooting

**"No data collected"**
- Check internet connection
- Some RSS feeds may be temporarily unavailable (normal)
- Try running again after a few minutes

**"Module not found"**
```bash
pip install -U streamlit pandas plotly feedparser requests textblob beautifulsoup4
```

## 📊 Sample Output

After running the scraper, you'll see:
```
🚀 Starting APAC Coffee Intelligence Scraper
==================================================
📰 Scraping Hacker News...
   ✓ Found 3 coffee discussions
📡 Scraping RSS Feeds...
   ✓ Found 27 articles from RSS feeds
🌐 Scraping Google News...
   ✓ Found 42 news articles

✅ Successfully scraped 72 discussions
📁 Data saved to: coffee_discussions.csv

🧠 Generating Market Insights...
✅ Insights saved to: market_insights.json
```

---

**Built for Grab Product & Strategy Teams** | *No API keys • Free data sources • Behavioral economics framework*
