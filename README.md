# 📊 Social Media Engagement Analysis — Internee.pk

> **Task 1 of 6** | Virtual Data Science Internship @ [Internee.pk](https://internee.pk)

Analyzing engagement trends across Instagram, LinkedIn, and Facebook to identify what content drives the most reach and interaction — and translate that into actionable content strategy recommendations.

---

## 📌 Objective

Measure and compare engagement performance across Internee.pk's three main social media channels, identify high-performing content types and topics, and provide data-backed recommendations for optimizing future content strategy.

---

## 🗂️ Project Structure

```
social-media-analysis/
│
├── data/
│   ├── social_media_data.csv       # Structured dataset (144 posts, 3 platforms)
│   └── social_media_data.json      # JSON format — mirrors real API response shape
│
├── charts/
│   ├── 01_platform_overview.png    # Reach, likes, engagement by platform
│   ├── 02_engagement_trend.png     # Weekly engagement trend + trend lines
│   ├── 03_post_type_heatmap.png    # Engagement rate by post type × platform
│   ├── 04_topic_performance.png    # Content topic ranking by engagement
│   └── 05_monthly_growth.png       # Month-over-month reach by platform
│
├── generate_data.py                # Mock data generation (mirrors Meta/LinkedIn API schema)
├── analyze.py                      # Full analysis + chart generation pipeline
└── README.md
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| pandas | Data manipulation and aggregation |
| matplotlib | Chart rendering |
| seaborn | Statistical visualizations |
| numpy | Numerical operations + trend line fitting |

---

## 📡 Data Source

**Note on API access:** Production social media analytics require platform-approved developer credentials (Meta Graph API, LinkedIn Organization API). Since this project does not have admin access to Internee.pk's accounts, the dataset was synthetically generated to mirror the exact schema returned by those APIs — same fields, same data types, same structural relationships.

The analysis logic, aggregation methods, and visualization pipeline are identical to what would run against live API data. To connect to real data, replace `generate_data.py` with authenticated API calls and point `analyze.py` at the live CSV/JSON output.

**Dataset:** 144 posts across 3 platforms over a 90-day period (Jan–Mar 2024)

| Platform | Posts | Fields |
|----------|-------|--------|
| Instagram | 60 | post_id, date, platform, post_type, topic, reach, likes, comments, shares, engagement_rate |
| Facebook | 48 | ↑ same schema |
| LinkedIn | 36 | ↑ same schema |

---

## 📈 Key Findings

### Platform Performance
| Platform | Avg Engagement Rate | Total Reach | Total Posts |
|----------|-------------------|-------------|-------------|
| **Instagram** | **13.47%** | 152,965 | 60 |
| LinkedIn | 12.40% | 41,283 | 36 |
| Facebook | 10.32% | 83,245 | 48 |

- Instagram leads on both reach and engagement rate
- LinkedIn punches above its weight — smaller audience but high interaction quality
- Facebook has the largest gap between reach and engagement

### Best Performing Content Types
- **Instagram:** Video (13.71%) > Carousel (13.60%) > Reel (13.22%)
- **LinkedIn:** Text posts (14.29%) > Article (13.10%) > Video (11.96%)
- **Facebook:** Text posts (10.79%) > Link posts (10.62%) > Video (10.29%)

### Best Performing Topics
1. Tips & Advice — 13.25% avg engagement
2. Internship Opportunities — 13.13%
3. Announcements — 12.61%
4. Success Stories — 12.32%

Motivational content ranked last (10.95%) — utility beats inspiration.

---

## 💡 Content Strategy Recommendations

**1. Double down on Instagram video and carousels**
These consistently outperform static images. Reels in particular benefit from algorithmic amplification.

**2. LinkedIn text posts > articles**
Counter-intuitive but clear in the data — native text posts get higher engagement than long-form articles on LinkedIn. Keep copy concise and insight-driven.

**3. Lead with utility, not motivation**
Tips & Advice and Internship Opportunity posts outperform Motivational content by ~2pp. Audiences engage when they get something actionable.

**4. Facebook strategy needs revision**
Lowest engagement rate across all post types. Consider reducing posting frequency and concentrating effort on higher-ROI platforms, or A/B testing paid reach to identify whether organic strategy or audience fit is the bottleneck.

**5. Post timing**
Trend analysis shows engagement variance week-over-week. Recommend A/B testing morning vs evening posting times to isolate timing effects in the next analysis cycle.

---

## ▶️ How to Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/internee-social-media-analysis
cd internee-social-media-analysis

# Install dependencies
pip install pandas matplotlib seaborn numpy

# Generate the dataset
python generate_data.py

# Run the full analysis (outputs charts to /charts/)
python analyze.py
```

---

## 🧠 What I Learned

- Structuring a data analysis pipeline from ingestion → transformation → visualization
- Using `pandas groupby`, `resample`, and `pivot_table` for multi-dimensional aggregation
- Fitting linear trend lines with `numpy.polyfit` over time-series data
- Translating raw numbers into strategic, decision-ready recommendations

---

## 👤 Author

**Abdullah** — Data Science Student @ NIT Lahore (Powered by ASU)
Virtual Intern @ Internee.pk | Task 1/6

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/YOUR_USERNAME)
