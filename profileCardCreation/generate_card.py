import os
import requests
import json
import sys

def get_github_stats(username, token):
    """Fetches GitHub user data using the GitHub API."""
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_svg(data):
    """Generates an SVG string dynamically from GitHub API data."""

    width = 500
    height = 220
    border_radius = 15

    # Use real name if available, otherwise fallback to username
    display_name = data.get("name") or data.get("login")

    # Dynamic stats (label, API key, icon, color)
    stats_config = [
        ("Followers", "followers", "⭐", "#facc15"),
        ("Following", "following", "👥", "#34d399"),
        ("Public Repos", "public_repos", "📁", "#60a5fa"),
        ("Public Gists", "public_gists", "📝", "#f472b6"),
        ("Hireable", "hireable", "💼", "#f87171"),
    ]

    # Build SVG rows dynamically
    stats_svg_elements = []
    y_position = 0
    for label, key, icon, color in stats_config:
        value = data.get(key, "N/A")
        stats_svg_elements.append(f"""
          <text x="0" y="{y_position}" class="stats-line">
            <tspan fill="{color}">{icon}</tspan>
            <tspan dx="10" fill="{color}" font-weight="bold">{label}:</tspan>
            <tspan dx="5" fill="#e5e7eb">{value}</tspan>
          </text>
        """)
        y_position += 28

    stats_svg_content = "\n".join(stats_svg_elements)

    # SVG template with gradient + avatar + badge
    svg_template = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#1e3a8a"/>
          <stop offset="100%" stop-color="#9333ea"/>
        </linearGradient>
      </defs>
      
      <!-- Card background -->
      <rect rx="{border_radius}" width="{width}" height="{height}" fill="url(#grad)" />

      <!-- User avatar -->
      <image href="{data['avatar_url']}" x="20" y="20" height="60" width="60" clip-path="circle(30px at 30px 30px)" />

      <!-- Title -->
      <text x="100" y="55" font-size="20" font-weight="bold" fill="#ffffff">{display_name}'s GitHub Stats</text>

      <!-- Stats -->
      <g transform="translate(100, 90)" font-size="16" font-family="sans-serif">
        {stats_svg_content}
      </g>

      <!-- Circular badge -->
      <g transform="translate({width-120}, {height//2 - 20})">
        <circle cx="40" cy="40" r="35" stroke="url(#grad)" stroke-width="6" fill="none"/>
        <text x="40" y="48" text-anchor="middle" font-size="20" font-weight="bold" fill="#ffffff">A++</text>
      </g>
    </svg>
    """
    return svg_template

def main():
    username = "bluekitsune-sad"
    token = os.getenv("GH_TOKEN")

    if not token:
        print("GH_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    try:
        data = get_github_stats(username, token)
        svg_content = create_svg(data)

        with open("dynamic_github_stats_card.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)

        print("Successfully generated dynamic_github_stats_card.svg")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
