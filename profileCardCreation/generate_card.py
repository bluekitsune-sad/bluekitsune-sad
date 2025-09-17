import os
import requests
import json

def get_github_stats(username, token):
    """Fetches GitHub user data using the GitHub API."""
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.loads(response.text)

def create_svg(data):
    """Generates an SVG string for the stats card."""
    # Define SVG constants
    width = 400
    height = 180
    bg_color = "#1f2937"
    text_color = "#e5e7eb"
    title_color = "#60a5fa"
    icon_color = "#9ca3af"
    border_radius = "10"
    
    # Basic SVG structure
    svg_template = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="0.5" y="0.5" rx="{border_radius}" width="{width-1}" height="{height-1}" fill="{bg_color}" stroke="#e5e7eb" stroke-opacity="0.2"/>
      <g transform="translate(25, 25)">
        <text x="0" y="0" font-family="sans-serif" font-size="20" font-weight="bold" fill="{title_color}">
          Saad Yousuf's GitHub Stats
        </text>
        
        <g transform="translate(0, 40)">
          <!-- Followers -->
          <text x="0" y="0" font-family="sans-serif" font-size="16" fill="{text_color}">
            <tspan x="0" y="0" fill="{icon_color}">⭐</tspan>
            <tspan x="25" y="0">Followers:</tspan>
            <tspan x="140" y="0" font-weight="bold">{data['followers']}</tspan>
          </text>
          
          <!-- Public Repos -->
          <text x="0" y="25" font-family="sans-serif" font-size="16" fill="{text_color}">
            <tspan x="0" y="0" fill="{icon_color}">📁</tspan>
            <tspan x="25" y="0">Public Repos:</tspan>
            <tspan x="140" y="0" font-weight="bold">{data['public_repos']}</tspan>
          </text>
          
          <!-- Following -->
          <text x="0" y="50" font-family="sans-serif" font-size="16" fill="{text_color}">
            <tspan x="0" y="0" fill="{icon_color}">👥</tspan>
            <tspan x="25" y="0">Following:</tspan>
            <tspan x="140" y="0" font-weight="bold">{data['following']}</tspan>
          </text>
        </g>
      </g>
    </svg>
    """
    return svg_template

def main():
    """Main function to fetch data and generate SVG file."""
    username = "bluekitsune-sad"
    token = os.getenv("GH_TOKEN")
    
    if not token:
        print("GH_TOKEN environment variable not set.")
        return
        
    try:
        data = get_github_stats(username, token)
        svg_content = create_svg(data)
        
        with open("github_stats_card.svg", "w") as f:
            f.write(svg_content)
        
        print("Successfully generated github_stats_card.svg")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {e}")

if __name__ == "__main__":
    main()
