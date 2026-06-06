"""
STEP 1: GENERATING MOCK SOCIAL MEDIA DATA
==========================================
In a real project, this data would come from:
  - Meta Graph API  → Instagram + Facebook
  - LinkedIn API    → LinkedIn

Since we don't have API credentials, we're generating data
that EXACTLY mirrors what those APIs return — same fields,
same data types, same structure.

This is standard practice in data projects when:
  - APIs require paid access / approval
  - You're prototyping before getting real data
  - You're building a demo / portfolio piece
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# ── NUMPY SEED ───────────────────────────────────────────────────────────────
# np.random generates random numbers. seed(42) means every time you run this,
# you get the SAME random numbers. Important for reproducibility.
np.random.seed(42)


# ── DATE RANGE ───────────────────────────────────────────────────────────────
# pd.date_range is like Python's range() but for dates.
# We're generating 90 days of posts (roughly 3 months of data).
start_date = datetime(2024, 1, 1)
end_date   = datetime(2024, 3, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
# freq='D' means daily. Could be 'W' for weekly, 'H' for hourly, etc.


# ── PLATFORM CONFIG ──────────────────────────────────────────────────────────
# Each platform has different typical engagement numbers.
# Instagram skews visual/high-like, LinkedIn skews professional/low-reach,
# Facebook sits in between. These multipliers reflect that.

platforms = {
    'Instagram': {
        'post_types':      ['image', 'video', 'reel', 'carousel'],
        'reach_range':     (800, 3500),    # min/max reach per post
        'like_rate':       (0.05, 0.15),   # likes as % of reach
        'comment_rate':    (0.01, 0.04),
        'share_rate':      (0.005, 0.02),
        'posts_per_month': 20,
    },
    'LinkedIn': {
        'post_types':      ['article', 'image', 'video', 'text'],
        'reach_range':     (300, 1800),
        'like_rate':       (0.03, 0.10),
        'comment_rate':    (0.01, 0.05),
        'share_rate':      (0.01, 0.04),
        'posts_per_month': 12,
    },
    'Facebook': {
        'post_types':      ['image', 'video', 'link', 'text'],
        'reach_range':     (500, 2500),
        'like_rate':       (0.03, 0.08),
        'comment_rate':    (0.005, 0.025),
        'share_rate':      (0.01, 0.05),
        'posts_per_month': 16,
    },
}

# ── INTERNEE.PK SPECIFIC CONTENT TOPICS ──────────────────────────────────────
# Making this realistic for an internship platform
topics = [
    'internship_opportunity', 'success_story', 'tips_and_advice',
    'company_spotlight', 'career_guide', 'motivational', 'announcement'
]


# ── DATA GENERATION FUNCTION ─────────────────────────────────────────────────
def generate_posts(platform_name, config, date_range):
    """
    For each platform, we pick random dates from date_range,
    then generate realistic metrics using the config above.
    
    np.random.choice  → picks random items from a list
    np.random.randint → picks a random integer in a range
    np.random.uniform → picks a random float in a range
    int(x * y)        → multiply reach by rate to get count
    """
    posts = []
    
    # How many posts total? posts_per_month × 3 months
    num_posts = config['posts_per_month'] * 3
    
    # Pick random dates (sorted so data looks chronological)
    post_dates = np.random.choice(date_range, size=num_posts, replace=False)
    post_dates = sorted(post_dates)
    
    for i, date in enumerate(post_dates):
        reach    = np.random.randint(*config['reach_range'])
        likes    = int(reach * np.random.uniform(*config['like_rate']))
        comments = int(reach * np.random.uniform(*config['comment_rate']))
        shares   = int(reach * np.random.uniform(*config['share_rate']))
        
        # Engagement rate formula — industry standard metric
        # (total interactions / reach) × 100 = engagement %
        engagement_rate = round(((likes + comments + shares) / reach) * 100, 2)
        
        # Simulate a small upward trend over time (realistic — accounts grow)
        # i/num_posts goes from 0 to 1 as we move through time
        # multiplying by 1.3 means last posts get up to 30% more reach
        growth_factor = 1 + (i / num_posts) * 0.3
        reach    = int(reach * growth_factor)
        likes    = int(likes * growth_factor)
        
        posts.append({
            'post_id':        f"{platform_name[:2].upper()}-{i+1:03d}",
            'date':           pd.Timestamp(date),
            'platform':       platform_name,
            'post_type':      np.random.choice(config['post_types']),
            'topic':          np.random.choice(topics),
            'reach':          reach,
            'likes':          likes,
            'comments':       comments,
            'shares':         shares,
            'engagement_rate': engagement_rate,
        })
    
    return posts


# ── GENERATE ALL DATA ─────────────────────────────────────────────────────────
all_posts = []
for platform_name, config in platforms.items():
    all_posts.extend(generate_posts(platform_name, config, date_range))

# pd.DataFrame() converts a list of dicts into a table (like a SQL table)
# Each dict key becomes a column, each dict becomes a row
df = pd.DataFrame(all_posts)

# Sort by date so data is chronological
df = df.sort_values('date').reset_index(drop=True)
# reset_index(drop=True) just resets row numbers to 0,1,2,3...
# without it, row numbers would be shuffled after sorting


# ── SAVE TO CSV ───────────────────────────────────────────────────────────────
# CSV = Comma Separated Values. Universal format — opens in Excel, pandas, etc.
df.to_csv('data/social_media_data.csv', index=False)
# index=False means don't write the row numbers as a column

# Also save as JSON to show what the "API response" would look like
json_data = df.to_dict(orient='records')
# orient='records' = list of dicts format [{col: val, ...}, ...]
with open('data/social_media_data.json', 'w') as f:
    json.dump(json_data, f, indent=2, default=str)
# default=str handles dates (which aren't JSON-serializable by default)

print(f"✅ Generated {len(df)} posts across {df['platform'].nunique()} platforms")
print(f"   Date range: {df['date'].min().date()} → {df['date'].max().date()}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nData types:")
print(df.dtypes)
print(f"\nBasic stats:")
print(df[['likes', 'comments', 'shares', 'reach', 'engagement_rate']].describe().round(2))
