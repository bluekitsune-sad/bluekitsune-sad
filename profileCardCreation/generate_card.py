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

    # Text content and formatting
    title = "Saad Yousuf's GitHub Stats"
    stats = [
        ("⭐", "Followers", data['followers']),
        ("📁", "Public Repos", data['public_repos']),
        ("👥", "Following", data['following'])
    ]
    
    # Dynamically generate the stats text elements
    stats_svg_elements = []
    y_position = 0
    for icon, label, value in stats:
        # Use relative positioning and tspans for better control
        stats_svg_elements.append(f"""
          <text x="0" y="{y_position}" class="stats-line">
            <tspan class="icon">{icon}</tspan>
            <tspan class="label">{label}:</tspan>
            <tspan class="value">{value}</tspan>
          </text>
        """)
        y_position += 25 # Increase vertical spacing for next line

    stats_svg_content = "\n".join(stats_svg_elements)

    # Basic SVG structure
    svg_template = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
      <style>
        .card-bg {{ fill: {bg_color}; stroke: #e5e7eb; stroke-opacity: 0.2; }}
        .title {{ font-family: sans-serif; font-size: 20px; font-weight: bold; fill: {title_color}; }}
        .stats-group {{ transform: translate(25px, 25px); }}
        .stats-line {{ font-family: sans-serif; font-size: 16px; fill: {text_color}; }}
        .icon {{ fill: {icon_color}; }}
        .label {{ font-weight: normal; }}
        .value {{ font-weight: bold; fill: {text_color}; }}
      </style>
      <rect x="0.5" y="0.5" rx="{border_radius}" width="{width-1}" height="{height-1}" class="card-bg"/>
      <g class="stats-group">
        <text x="0" y="0" class="title">{title}</text>
        <g transform="translate(0, 40)">
          {stats_svg_content}
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
        # Exit with a non-zero code to fail the workflow
        print("GH_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)
        
    try:
        data = get_github_stats(username, token)
        svg_content = create_svg(data)
        
        with open("github_stats_card.svg", "w") as f:
            f.write(svg_content)
        
        print("Successfully generated github_stats_card.svg")
        
    except requests.exceptions.RequestException as e:
        # Exit with a non-zero code to fail the workflow and log the error
        print(f"Error fetching GitHub data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
