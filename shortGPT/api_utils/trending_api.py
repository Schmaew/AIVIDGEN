"""
Trending Topics API - Fetches current trending topics for viral content generation
"""
import requests
import random
from datetime import datetime

def get_trending_topics():
    """
    Get trending topics from multiple sources.
    Returns a list of trending topic strings.
    """
    topics = []
    
    # Try Google Trends RSS
    try:
        topics.extend(_get_google_trends())
    except Exception as e:
        print(f"Google Trends fetch failed: {e}")
    
    # Add curated viral topics as fallback
    topics.extend(_get_viral_fact_categories())
    
    # Remove duplicates and shuffle
    topics = list(set(topics))
    random.shuffle(topics)
    
    return topics[:20]  # Return top 20

def _get_google_trends():
    """Fetch trending searches from Google Trends RSS"""
    trends = []
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if response.status_code == 200:
            import re
            titles = re.findall(r'<title>([^<]+)</title>', response.text)
            # Skip the first title (feed title)
            trends = [t.strip() for t in titles[1:15] if t.strip()]
    except:
        pass
    return trends

def _get_viral_fact_categories():
    """
    Curated list of viral fact categories that consistently perform well.
    These are rotated based on day/time for variety.
    """
    categories = [
        # Science & Nature
        "Mind-blowing space facts",
        "Crazy animal facts",
        "Weird ocean creatures facts",
        "Insane human body facts",
        "Unbelievable science discoveries",
        "Bizarre plant facts",
        "Terrifying deep sea facts",
        
        # Psychology & Human Behavior
        "Dark psychology facts",
        "Manipulation tactics facts",
        "Dreams and sleep facts",
        "Memory and brain facts",
        "Creepy psychology facts",
        
        # History & World
        "Disturbing history facts",
        "Ancient civilization secrets",
        "Unsolved mysteries facts",
        "Weird laws around the world",
        "Creepy places on earth",
        "Abandoned places facts",
        
        # Technology & Future
        "AI and technology facts",
        "Future predictions facts",
        "Internet dark secrets",
        
        # Money & Success
        "Rich people secrets",
        "Money psychology facts",
        "Billionaire habits facts",
        
        # Relationships & Social
        "Dating psychology facts",
        "Body language secrets",
        "Social manipulation facts",
        
        # Food & Health
        "Disgusting food industry facts",
        "Scary health facts",
        "Food you should never eat facts",
        
        # Entertainment
        "Movie industry dark secrets",
        "Celebrity conspiracy facts",
        "Disney dark secrets",
    ]
    
    # Rotate based on current hour for variety
    hour = datetime.now().hour
    day = datetime.now().day
    seed = hour + day * 24
    random.seed(seed)
    random.shuffle(categories)
    random.seed()  # Reset seed
    
    return categories

def get_trending_fact_topic():
    """
    Get a single trending topic optimized for facts videos.
    Combines trending searches with viral categories.
    """
    topics = get_trending_topics()
    
    if topics:
        # 70% chance viral category, 30% chance actual trending
        if random.random() < 0.7:
            return random.choice([t for t in topics if "facts" in t.lower() or len(t.split()) > 2])
        return random.choice(topics) + " facts"
    
    return "Mind-blowing facts you need to know"
