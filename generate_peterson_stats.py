#!/usr/bin/env python3
"""
Generate Peterson Podcast Statistics HTML
"""

import json
from collections import Counter


def parse_views(views_str):
    """Convert '123,970 views' to 123970"""
    if views_str:
        return int(views_str.replace(',', '').replace(' views', ''))
    return 0


def parse_duration(duration_str):
    """Convert '1:38:16' to total seconds"""
    parts = duration_str.split(':')
    if len(parts) == 3:  # H:M:S
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:  # M:S
        return int(parts[0]) * 60 + int(parts[1])
    return 0


def generate_html():
    # Load data
    with open('flask_data/peterson-podcasts.json', 'r') as f:
        episodes = json.load(f)

    # Calculate total views
    total_views = sum(parse_views(ep.get('views', '0')) for ep in episodes)
    avg_views = total_views // len(episodes)

    # Calculate total duration
    total_seconds = sum(parse_duration(ep.get('duration', '0:0')) for ep in episodes)
    total_hours = total_seconds / 3600
    total_days = total_hours / 24
    avg_minutes = total_seconds / len(episodes) / 60

    # Extract guests
    guests = []
    for ep in episodes:
        guest = ep.get('guest')
        if guest and not guest.startswith('EP ') and guest not in ['Answer the Call', 'Lecture One (Official)']:
            guests.append(guest)

    guest_counts = Counter(guests)
    top_10_guests = guest_counts.most_common(10)

    # Top viewed episodes
    episodes_with_views = [(ep, parse_views(ep.get('views', '0'))) for ep in episodes]
    top_viewed = sorted(episodes_with_views, key=lambda x: x[1], reverse=True)[:10]

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Gorgon: Peterson Podcast Statistics</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #0a0a0a;
            color: #e0e0e0;
            line-height: 1.6;
        }}
        h1 {{
            color: #00ff88;
            border-bottom: 3px solid #00ff88;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #00ccff;
            margin-top: 40px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: #1a1a1a;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #333;
        }}
        .stat-label {{
            color: #888;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stat-value {{
            color: #00ff88;
            font-size: 2em;
            font-weight: bold;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #1a1a1a;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #333;
        }}
        th {{
            background: #252525;
            color: #00ccff;
            font-weight: 600;
        }}
        tr:hover {{
            background: #222;
        }}
        .rank {{
            color: #00ff88;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 60px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>🎙️ Project Gorgon: Peterson Podcast Statistics</h1>
    <p>Comprehensive analysis of Jordan Peterson's YouTube podcast episodes</p>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Total Episodes</div>
            <div class="stat-value">{len(episodes):,}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Views</div>
            <div class="stat-value">{total_views:,}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Avg Views/Episode</div>
            <div class="stat-value">{avg_views:,}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Hours</div>
            <div class="stat-value">{total_hours:,.1f}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Days</div>
            <div class="stat-value">{total_days:,.1f}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Avg Length (min)</div>
            <div class="stat-value">{avg_minutes:.1f}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Unique Guests</div>
            <div class="stat-value">{len(guest_counts)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Episodes with Guests</div>
            <div class="stat-value">{len(guests)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Solo Episodes</div>
            <div class="stat-value">{len(episodes) - len(guests)}</div>
        </div>
    </div>

    <h2>Top 10 Most Frequent Guests</h2>
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Guest</th>
                <th>Episodes</th>
            </tr>
        </thead>
        <tbody>
"""

    for i, (guest, count) in enumerate(top_10_guests, 1):
        html += f"""            <tr>
                <td class="rank">{i}</td>
                <td>{guest}</td>
                <td>{count}</td>
            </tr>
"""

    html += """        </tbody>
    </table>

    <h2>Top 10 Most Viewed Episodes</h2>
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Views</th>
                <th>Guest</th>
                <th>Title</th>
            </tr>
        </thead>
        <tbody>
"""

    for i, (ep, views) in enumerate(top_viewed, 1):
        title = ep['title']
        guest = ep.get('guest') or 'Solo'
        url = ep.get('url', '')
        html += f"""            <tr>
                <td class="rank">{i}</td>
                <td>{views:,}</td>
                <td>{guest}</td>
                <td><a href="{url}" target="_blank" style="color: #00ccff; text-decoration: none;">{title}</a></td>
            </tr>
"""

    html += f"""        </tbody>
    </table>

    <div class="footer">
        <p>Project Gorgon | Generated from {len(episodes)} episodes</p>
    </div>
</body>
</html>
"""

    return html


if __name__ == '__main__':
    html_content = generate_html()
    
    # Save to file
    with open('flask_data/peterson-stats.html', 'w') as f:
        f.write(html_content)
    
    print("✓ Generated peterson-stats.html")
