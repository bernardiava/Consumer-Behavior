#!/usr/bin/env python3
"""
APAC Coffee Consumer Intelligence Scraper
Sources: Hacker News (JSON API), RSS Feeds, Public News Sites
No API Keys Required - Free Tier Only

Behavioral Economics Framework:
- Price Sensitivity Index (PSI)
- Convenience Heuristics
- Social Signaling Markers
- Brand Loyalty Indicators
"""

import feedparser
import requests
import pandas as pd
import json
import re
from datetime import datetime, timedelta
from textblob import TextBlob
from bs4 import BeautifulSoup
import time
import random

class CoffeeTrendScraper:
    def __init__(self):
        self.sources = {
            'hackernews': 'https://hacker-news.firebaseio.com/v0',
            'rss_feeds': [
                'https://www.perfectdailygrind.com/feed/',
                'https://baristamagazine.com/feed/',
                'https://sprudge.com/feed/',
                'https://techcrunch.com/tag/coffee/feed/',
                'https://www.foodnavigator-asia.com/Feed/RSS/all?tags=coffee'
            ],
            'news_search': [
                'https://news.google.com/rss/search?q=coffee+price+indonesia&hl=en-ID&gl=ID&ceid=ID:en',
                'https://news.google.com/rss/search?q=grab+coffee+delivery&hl=en&gl=SG&ceid=SG:en',
                'https://news.google.com/rss/search?q=kopi+kenangan&hl=id&gl=ID&ceid=ID:id'
            ]
        }
        self.data = []
        
    def classify_consumer_segment(self, text):
        """
        Behavioral Economics Classification Engine
        Based on linguistic markers and economic signaling
        """
        text_lower = text.lower()
        scores = {
            'Price Sensitive': 0,
            'Quality Focused': 0,
            'Convenience Seekers': 0,
            'Social Drinkers': 0,
            'Habitual Consumers': 0,
            'Brand Loyal': 0
        }
        
        # Price Sensitivity Markers (Highest weight in APAC emerging markets)
        price_keywords = ['cheap', 'expensive', 'promo', 'discount', 'price', 'cost', 
                         'affordable', 'budget', 'murah', 'mahal', 'diskon', 'hemat',
                         'free delivery', 'gratis ongkir', 'bundling']
        for kw in price_keywords:
            if kw in text_lower:
                scores['Price Sensitive'] += 2.5
        
        # Quality Focused Markers
        quality_keywords = ['arabica', 'single origin', 'specialty', 'brew', 'espresso',
                           'latte art', 'beans', 'roast', 'fresh', 'premium', 'quality',
                           'manual brew', 'v60', 'chemex', 'aeropress']
        for kw in quality_keywords:
            if kw in text_lower:
                scores['Quality Focused'] += 2.0
        
        # Convenience Seekers (Critical for Grab Superapp strategy)
        convenience_keywords = ['delivery', 'grabfood', 'gojek', 'instant', 'quick', 
                               'fast', 'app', 'order online', 'drive-thru', 'near me',
                               'antar', 'pesan online', 'cepat']
        for kw in convenience_keywords:
            if kw in text_lower:
                scores['Convenience Seekers'] += 3.0
        
        # Social Drinkers
        social_keywords = ['cafe', 'hangout', 'meet', 'friends', 'instagram', 'photo',
                          'aesthetic', 'place', 'vibes', 'nongkrong', 'tempat', 'cozy',
                          'wifi', 'work from cafe', 'meeting spot']
        for kw in social_keywords:
            if kw in text_lower:
                scores['Social Drinkers'] += 1.8
        
        # Habitual Consumers
        habit_keywords = ['daily', 'every morning', 'routine', 'addict', 'need coffee',
                         'can\'t start', 'morning ritual', 'everyday', 'habit', 'rutin',
                         'tiap pagi', 'ngopi']
        for kw in habit_keywords:
            if kw in text_lower:
                scores['Habitual Consumers'] += 2.2
        
        # Brand Loyal
        brand_keywords = ['starbucks', 'kopi kenangan', 'janji jiwa', 'luckin', '% arabica',
                         'blue bottle', 'philz', 'local brand', 'support local', 'brand',
                         'loyalty', 'member', 'points', 'rewards']
        for kw in brand_keywords:
            if kw in text_lower:
                scores['Brand Loyal'] += 1.5
        
        # Determine dominant segment
        max_score = max(scores.values())
        if max_score == 0:
            return 'General Consumer'
        
        dominant = [k for k, v in scores.items() if v == max_score][0]
        return dominant
    
    def calculate_sentiment(self, text):
        """Calculate sentiment score using TextBlob"""
        try:
            blob = TextBlob(text)
            return round(blob.sentiment.polarity, 3)
        except:
            return 0.0
    
    def extract_region(self, text, source=''):
        """Detect APAC region from content"""
        text_lower = text.lower()
        region_map = {
            'Indonesia': ['indonesia', 'jakarta', 'bandung', 'surabaya', 'bali', 'medan', 'kopi indonesia'],
            'Singapore': ['singapore', 'sg', 'marina bay', 'orchard'],
            'Malaysia': ['malaysia', 'kl', 'kuala lumpur', 'penang'],
            'Thailand': ['thailand', 'bangkok', 'chiang mai'],
            'Vietnam': ['vietnam', 'hanoi', 'ho chi minh', 'saigon'],
            'Philippines': ['philippines', 'manila', 'cebu'],
            'APAC': ['apac', 'asia pacific', 'southeast asia', 'asean']
        }
        
        for region, keywords in region_map.items():
            for kw in keywords:
                if kw in text_lower:
                    return region
        
        # Default based on source URL
        if 'id' in source.lower() or '.id' in source:
            return 'Indonesia'
        elif 'sg' in source.lower():
            return 'Singapore'
        
        return 'APAC Regional'
    
    def scrape_hackernews(self, limit=50):
        """Scrape Hacker News for coffee-related discussions"""
        print("📰 Scraping Hacker News...")
        try:
            # Get top stories
            top_stories_url = f"{self.sources['hackernews']}/topstories.json"
            response = requests.get(top_stories_url, timeout=10)
            story_ids = response.json()[:limit]
            
            coffee_keywords = ['coffee', 'cafe', 'espresso', 'latte', 'caffeine', 'starbucks', 'kopitiam']
            
            for story_id in story_ids:
                story_url = f"{self.sources['hackernews']}/item/{story_id}.json"
                story_data = requests.get(story_url, timeout=5).json()
                
                title = story_data.get('title', '')
                if any(kw in title.lower() for kw in coffee_keywords):
                    text_content = f"{title} {story_data.get('selftext', '')}"
                    
                    self.data.append({
                        'date': datetime.fromtimestamp(story_data.get('time', 0)).strftime('%Y-%m-%d'),
                        'source': 'Hacker News',
                        'title': title,
                        'url': f"https://news.ycombinator.com/item?id={story_id}",
                        'region': self.extract_region(text_content, 'hackernews'),
                        'consumer_segment': self.classify_consumer_segment(text_content),
                        'sentiment_score': self.calculate_sentiment(text_content),
                        'engagement_score': story_data.get('score', 0) + story_data.get('descendants', 0),
                        'topic': self._extract_topic(title)
                    })
            print(f"   ✓ Found {len([d for d in self.data if d['source']=='Hacker News'])} coffee discussions")
        except Exception as e:
            print(f"   ⚠️  Hacker News error: {e}")
    
    def scrape_rss_feeds(self):
        """Scrape RSS feeds from coffee industry publications"""
        print("📡 Scraping RSS Feeds...")
        total_found = 0
        
        for feed_url in self.sources['rss_feeds']:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:  # Limit per feed
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    published = entry.get('published_parsed', datetime.now().timetuple())
                    
                    text_content = f"{title} {summary}"
                    
                    # Filter for relevant content
                    if any(kw in text_content.lower() for kw in ['coffee', 'cafe', 'espresso', 'barista']):
                        try:
                            pub_date = datetime(*published[:6])
                        except:
                            pub_date = datetime.now()
                        
                        self.data.append({
                            'date': pub_date.strftime('%Y-%m-%d'),
                            'source': feed.feed.get('title', 'RSS Feed'),
                            'title': title,
                            'url': entry.get('link', ''),
                            'region': self.extract_region(text_content, feed_url),
                            'consumer_segment': self.classify_consumer_segment(text_content),
                            'sentiment_score': self.calculate_sentiment(text_content),
                            'engagement_score': len(summary) // 10,  # Proxy metric
                            'topic': self._extract_topic(title)
                        })
                        total_found += 1
                
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"   ⚠️  RSS feed {feed_url} error: {e}")
        
        print(f"   ✓ Found {total_found} articles from RSS feeds")
    
    def scrape_google_news(self):
        """Scrape Google News RSS for regional coffee news"""
        print("🌐 Scraping Google News...")
        total_found = 0
        
        for news_url in self.sources['news_search']:
            try:
                feed = feedparser.parse(news_url)
                for entry in feed.entries[:15]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    published = entry.get('published_parsed', datetime.now().timetuple())
                    
                    text_content = f"{title} {summary}"
                    
                    try:
                        pub_date = datetime(*published[:6])
                    except:
                        pub_date = datetime.now()
                    
                    self.data.append({
                        'date': pub_date.strftime('%Y-%m-%d'),
                        'source': 'Google News',
                        'title': title,
                        'url': entry.get('link', ''),
                        'region': self.extract_region(text_content, news_url),
                        'consumer_segment': self.classify_consumer_segment(text_content),
                        'sentiment_score': self.calculate_sentiment(text_content),
                        'engagement_score': 50,  # Default for news
                        'topic': self._extract_topic(title)
                    })
                    total_found += 1
                
                time.sleep(0.3)
            except Exception as e:
                print(f"   ⚠️  Google News {news_url} error: {e}")
        
        print(f"   ✓ Found {total_found} news articles")
    
    def _extract_topic(self, title):
        """Extract main topic from title"""
        title_lower = title.lower()
        topics = {
            'Pricing & Promotions': ['price', 'cost', 'promo', 'discount', 'cheap', 'expensive'],
            'Delivery & Apps': ['delivery', 'grabfood', 'gojek', 'app', 'online order'],
            'New Openings': ['opens', 'new', 'launch', 'debut', 'first store'],
            'Product Innovation': ['new product', 'launches', 'introduces', 'innovation'],
            'Market Trends': ['trend', 'market', 'growth', 'industry', 'report'],
            'Local Competition': ['local', 'vs', 'competition', 'rival'],
            'Sustainability': ['sustainable', 'eco', 'fair trade', 'organic'],
            'Consumer Behavior': ['consumer', 'preference', 'habit', 'trend']
        }
        
        for topic, keywords in topics.items():
            if any(kw in title_lower for kw in keywords):
                return topic
        
        return 'General Discussion'
    
    def run(self):
        """Execute all scrapers"""
        print("🚀 Starting APAC Coffee Intelligence Scraper")
        print("=" * 50)
        
        self.scrape_hackernews()
        self.scrape_rss_feeds()
        self.scrape_google_news()
        
        # Convert to DataFrame
        df = pd.DataFrame(self.data)
        
        if len(df) > 0:
            # Remove duplicates
            df = df.drop_duplicates(subset=['title', 'url'])
            
            # Sort by date
            df = df.sort_values('date', ascending=False)
            
            # Save to CSV
            df.to_csv('coffee_discussions.csv', index=False)
            print(f"\n✅ Successfully scraped {len(df)} discussions")
            print(f"📁 Data saved to: coffee_discussions.csv")
            
            # Generate insights
            self.generate_insights(df)
            
            return df
        else:
            print("\n❌ No data collected. Check network connection.")
            return None
    
    def generate_insights(self, df):
        """Generate strategic insights for Grab"""
        print("\n🧠 Generating Market Insights...")
        
        # Segment distribution
        segment_dist = df['consumer_segment'].value_counts(normalize=True).to_dict()
        
        # Regional analysis
        regional_sentiment = df.groupby('region')['sentiment_score'].mean().to_dict()
        
        # Topic trends
        topic_trends = df['topic'].value_counts().head(5).to_dict()
        
        insights = {
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(df),
            "target_market": "Grab (Indonesia/APAC)",
            "segment_distribution": {k: round(v * 100, 2) for k, v in segment_dist.items()},
            "regional_sentiment": {k: round(v, 3) for k, v in regional_sentiment.items()},
            "top_topics": topic_trends,
            "key_findings": {
                "price_sensitivity": f"{segment_dist.get('Price Sensitive', 0)*100:.1f}% of discussions focus on pricing",
                "convenience_demand": f"{segment_dist.get('Convenience Seekers', 0)*100:.1f}% prioritize delivery/apps",
                "strongest_market": max(regional_sentiment, key=regional_sentiment.get) if regional_sentiment else "N/A"
            },
            "strategic_recommendations": [
                "Launch 'Coffee Subscription Pass' targeting Price Sensitive segment",
                "Bundle coffee with GrabExpress for Convenience Seekers",
                "Partner with local specialty cafes for Quality Focused users",
                "Create 'Work-from-Cafe' packages for Social Drinkers"
            ]
        }
        
        with open('market_insights.json', 'w') as f:
            json.dump(insights, f, indent=2)
        
        print("✅ Insights saved to: market_insights.json")


if __name__ == "__main__":
    scraper = CoffeeTrendScraper()
    scraper.run()
