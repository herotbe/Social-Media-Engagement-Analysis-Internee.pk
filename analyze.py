"""
STEP 2: ANALYSIS + VISUALIZATION
==================================
This is where pandas really shines.
Core operations we'll use:

  df.groupby()     → like SQL GROUP BY
  df.agg()         → like SQL SUM(), AVG(), COUNT()
  df.sort_values() → like SQL ORDER BY
  df[condition]    → like SQL WHERE
  df.resample()    → group by time period (week, month, etc.)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import os

# ── SETUP ─────────────────────────────────────────────────────────────────────
os.makedirs('charts', exist_ok=True)

# Load our data
df = pd.read_csv('data/social_media_data.csv', parse_dates=['date'])
# parse_dates=['date'] tells pandas to convert that column to datetime
# Without this, dates load as plain strings and you can't do time operations

# Color palette — consistent colors per platform throughout all charts
COLORS = {
    'Instagram': '#E1306C',
    'LinkedIn':  '#0077B5',
    'Facebook':  '#1877F2',
}
PLATFORM_COLORS = [COLORS[p] for p in ['Instagram', 'LinkedIn', 'Facebook']]

# Global chart style
sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams['figure.dpi'] = 150


print("=" * 60)
print("INTERNEE.PK — SOCIAL MEDIA ENGAGEMENT ANALYSIS")
print("=" * 60)


# ════════════════════════════════════════════════════════════════
# ANALYSIS 1: PLATFORM PERFORMANCE OVERVIEW
# ════════════════════════════════════════════════════════════════
"""
groupby('platform') → splits df into 3 groups (one per platform)
.agg({...})         → for each group, calculate these aggregations
  'sum'             → add up all values (total likes across all posts)
  'mean'            → average (avg engagement rate per post)
  'count'           → how many posts
"""
platform_stats = df.groupby('platform').agg(
    total_posts      = ('post_id',        'count'),
    total_reach      = ('reach',          'sum'),
    total_likes      = ('likes',          'sum'),
    total_comments   = ('comments',       'sum'),
    total_shares     = ('shares',         'sum'),
    avg_engagement   = ('engagement_rate','mean'),
    avg_reach        = ('reach',          'mean'),
).round(2)

print("\n📊 PLATFORM OVERVIEW:")
print(platform_stats.to_string())

# ── CHART 1: Side-by-side bar chart ──────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Internee.pk — Platform Performance Overview", fontsize=14, fontweight='bold', y=1.02)

metrics = ['total_reach', 'total_likes', 'avg_engagement']
labels  = ['Total Reach', 'Total Likes', 'Avg Engagement Rate (%)']

for ax, metric, label in zip(axes, metrics, labels):
    bars = ax.bar(
        platform_stats.index,
        platform_stats[metric],
        color=PLATFORM_COLORS,
        edgecolor='white',
        linewidth=0.5,
        width=0.5
    )
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height * 1.01,
            f'{height:,.0f}' if height > 100 else f'{height:.1f}%',
            ha='center', va='bottom', fontsize=9, fontweight='bold'
        )
    ax.set_title(label, fontweight='bold', fontsize=11)
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=0)
    sns.despine(ax=ax)

plt.tight_layout()
plt.savefig('charts/01_platform_overview.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ Chart 1 saved")


# ════════════════════════════════════════════════════════════════
# ANALYSIS 2: ENGAGEMENT TREND OVER TIME
# ════════════════════════════════════════════════════════════════
"""
resample('W') → groups rows by week (like groupby but for time)
  You need date as the index for this to work, hence set_index()
  
This answers: "Is our engagement growing, shrinking, or flat?"
"""
df_indexed = df.set_index('date')
# set_index makes 'date' the row label instead of 0,1,2,3...

weekly = (
    df_indexed
    .groupby('platform')
    .resample('W')['engagement_rate']
    .mean()
    .reset_index()
)
# This is chaining:
# 1. group by platform
# 2. within each platform, resample by week
# 3. take the mean engagement_rate for that week
# 4. reset_index() flattens the result back to a normal table

# ── CHART 2: Line chart — engagement trend ───────────────────────
fig, ax = plt.subplots(figsize=(14, 5))

for platform, color in COLORS.items():
    subset = weekly[weekly['platform'] == platform]
    # weekly[weekly['platform'] == platform] is filtering — like SQL WHERE
    # It returns only rows where platform equals this value
    
    ax.plot(
        subset['date'],
        subset['engagement_rate'],
        color=color,
        label=platform,
        linewidth=2.5,
        marker='o',
        markersize=4,
        alpha=0.9
    )
    # Add a trend line using numpy polyfit (linear regression)
    # This shows the overall direction regardless of weekly noise
    x_num = mdates.date2num(subset['date'])
    z = np.polyfit(x_num, subset['engagement_rate'], 1)
    p = np.poly1d(z)
    ax.plot(subset['date'], p(x_num), '--', color=color, alpha=0.4, linewidth=1.5)

ax.set_title("Weekly Engagement Rate Trend by Platform\n(dashed = trend line)", fontsize=13, fontweight='bold')
ax.set_xlabel("Date")
ax.set_ylabel("Avg Engagement Rate (%)")
ax.legend(loc='upper left')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
plt.xticks(rotation=30)
sns.despine()
plt.tight_layout()
plt.savefig('charts/02_engagement_trend.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ Chart 2 saved")


# ════════════════════════════════════════════════════════════════
# ANALYSIS 3: POST TYPE PERFORMANCE
# ════════════════════════════════════════════════════════════════
"""
Which content format (video, image, reel...) drives most engagement?
This is actionable — it tells you what to post more of.

pivot_table is like a spreadsheet pivot — 
rows = post_type, columns = platform, values = avg engagement
"""
post_type_perf = df.groupby(['platform', 'post_type'])['engagement_rate'].mean().round(2).reset_index()

pivot = post_type_perf.pivot(index='post_type', columns='platform', values='engagement_rate')
# pivot restructures the table:
# Before: platform | post_type | engagement_rate  (long format)
# After:  post_type | Instagram | LinkedIn | Facebook  (wide format)

print("\n📊 ENGAGEMENT BY POST TYPE:")
print(pivot.to_string())

# ── CHART 3: Heatmap ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(
    pivot,
    annot=True,       # show values inside cells
    fmt='.1f',        # format: 1 decimal place
    cmap='YlOrRd',    # color scale: yellow → orange → red (higher = darker)
    linewidths=0.5,
    ax=ax,
    cbar_kws={'label': 'Avg Engagement Rate (%)'}
)
ax.set_title("Avg Engagement Rate by Post Type & Platform", fontsize=13, fontweight='bold')
ax.set_xlabel("")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig('charts/03_post_type_heatmap.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ Chart 3 saved")


# ════════════════════════════════════════════════════════════════
# ANALYSIS 4: TOPIC PERFORMANCE
# ════════════════════════════════════════════════════════════════
topic_perf = (
    df.groupby('topic')
    .agg(
        avg_engagement = ('engagement_rate', 'mean'),
        total_reach    = ('reach',           'sum'),
        post_count     = ('post_id',         'count')
    )
    .sort_values('avg_engagement', ascending=False)
    .round(2)
)

print("\n📊 ENGAGEMENT BY TOPIC:")
print(topic_perf.to_string())

# ── CHART 4: Horizontal bar — topics ranked ──────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
colors_topic = sns.color_palette("viridis", len(topic_perf))
bars = ax.barh(
    topic_perf.index,
    topic_perf['avg_engagement'],
    color=colors_topic,
    edgecolor='white'
)
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
            f'{width:.1f}%', va='center', ha='left', fontsize=9)
ax.set_title("Avg Engagement Rate by Content Topic", fontsize=13, fontweight='bold')
ax.set_xlabel("Avg Engagement Rate (%)")
ax.invert_yaxis()
sns.despine()
plt.tight_layout()
plt.savefig('charts/04_topic_performance.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ Chart 4 saved")


# ════════════════════════════════════════════════════════════════
# ANALYSIS 5: MONTHLY GROWTH
# ════════════════════════════════════════════════════════════════
df['month'] = df['date'].dt.to_period('M')
# dt.to_period('M') extracts just the year-month: 2024-01, 2024-02, etc.

monthly_growth = df.groupby(['platform', 'month']).agg(
    total_reach = ('reach', 'sum'),
    avg_engagement = ('engagement_rate', 'mean')
).reset_index()
monthly_growth['month_str'] = monthly_growth['month'].astype(str)

# ── CHART 5: Grouped bar — monthly reach ────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
months = monthly_growth['month_str'].unique()
x = np.arange(len(months))
width = 0.25

for i, (platform, color) in enumerate(COLORS.items()):
    subset = monthly_growth[monthly_growth['platform'] == platform]
    ax.bar(x + i*width, subset['total_reach'], width, label=platform, color=color, alpha=0.85)

ax.set_title("Monthly Total Reach by Platform", fontsize=13, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(['January', 'February', 'March'])
ax.set_ylabel("Total Reach")
ax.legend()
sns.despine()
plt.tight_layout()
plt.savefig('charts/05_monthly_growth.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ Chart 5 saved")


# ════════════════════════════════════════════════════════════════
# SUMMARY STATS FOR REPORT
# ════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("KEY FINDINGS SUMMARY")
print("=" * 60)

best_platform = platform_stats['avg_engagement'].idxmax()
# idxmax() returns the INDEX (row label) of the maximum value
# So this gives us the platform name with highest avg engagement

best_post_type = df.groupby('post_type')['engagement_rate'].mean().idxmax()
best_topic     = topic_perf['avg_engagement'].idxmax()

print(f"  Best performing platform:  {best_platform} ({platform_stats.loc[best_platform, 'avg_engagement']:.1f}% avg engagement)")
print(f"  Best performing post type: {best_post_type}")
print(f"  Best performing topic:     {best_topic}")
print(f"  Total posts analyzed:      {len(df)}")
print(f"  Total reach generated:     {df['reach'].sum():,}")
print(f"  Overall avg engagement:    {df['engagement_rate'].mean():.2f}%")

# Month-over-month growth
jan_eng = df[df['month'] == '2024-01']['engagement_rate'].mean()
mar_eng = df[df['month'] == '2024-03']['engagement_rate'].mean()
growth  = ((mar_eng - jan_eng) / jan_eng) * 100
print(f"  Engagement growth Jan→Mar: {growth:+.1f}%")

print("\n✅ All 5 charts saved to /charts/")
print("✅ Analysis complete — ready for report writing")
