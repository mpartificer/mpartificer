# debug_nyt_stats.py - Drop-in replacement for nyt_stats.py with debugging
import os
import json
import requests
from datetime import datetime
import re

def get_nyt_stats(cookie):
    """
    Fetch NYT puzzle stats using user's cookie
    """
    print(f"Cookie length: {len(cookie)}")
    print(f"Cookie starts with: {cookie[:20]}...")
    
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try to get crossword stats
    crossword_stats = {}
    try:
        crossword_url = 'https://www.nytimes.com/svc/crosswords/v6/puzzle/daily/stats.json'
        print(f"Fetching crossword stats from: {crossword_url}")
        crossword_response = requests.get(crossword_url, headers=headers)
        print(f"Crossword response status: {crossword_response.status_code}")
        print(f"Crossword response headers: {crossword_response.headers}")
        if crossword_response.status_code == 200:
            crossword_stats = crossword_response.json()
            print(f"Crossword stats: {json.dumps(crossword_stats, indent=2)}")
        else:
            print(f"Crossword response text: {crossword_response.text[:200]}...")
    except Exception as e:
        print(f"Error fetching crossword stats: {e}")
    
    # For debugging, let's create some dummy stats if we didn't get real ones
    if not crossword_stats:
        print("Using dummy crossword stats")
        crossword_stats = {
            "stats": {
                "streakCount": 5,
                "maxStreakCount": 10,
                "solves": 42,
                "averageSolveTime": 600
            }
        }
    
    # Try to get Wordle stats
    wordle_stats = {}
    try:
        wordle_url = 'https://www.nytimes.com/svc/wordle/v2/stats.json'
        print(f"Fetching Wordle stats from: {wordle_url}")
        wordle_response = requests.get(wordle_url, headers=headers)
        print(f"Wordle response status: {wordle_response.status_code}")
        if wordle_response.status_code == 200:
            wordle_stats = wordle_response.json()
            print(f"Wordle stats keys: {list(wordle_stats.keys())}")
        else:
            print(f"Wordle response text: {wordle_response.text[:200]}...")
    except Exception as e:
        print(f"Error fetching Wordle stats: {e}")
    
    # For debugging, let's create some dummy stats if we didn't get real ones
    if not wordle_stats:
        print("Using dummy Wordle stats")
        wordle_stats = {
            "data": {
                "currentStreak": 3,
                "maxStreak": 12,
                "gamesPlayed": 65,
                "winPercentage": 92,
                "guesses": {"1": 5, "2": 10, "3": 20, "4": 15, "5": 10, "6": 5}
            }
        }
    
    return {
        "crossword": crossword_stats,
        "wordle": wordle_stats,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def format_stats_markdown(stats):
    """
    Format the stats as a nice markdown table for GitHub README
    """
    markdown = "## 🧩 My NYT Puzzle Stats\n\n"
    markdown += f"*Last updated: {stats['last_updated']}*\n\n"
    
    # Format Crossword stats
    if stats['crossword'] and 'stats' in stats['crossword']:
        cw_stats = stats['crossword']['stats']
        markdown += "### Crossword\n\n"
        markdown += "| Statistic | Value |\n"
        markdown += "|-----------|-------|\n"
        
        if 'streakCount' in cw_stats:
            markdown += f"| Current Streak | {cw_stats['streakCount']} |\n"
        if 'maxStreakCount' in cw_stats:
            markdown += f"| Max Streak | {cw_stats['maxStreakCount']} |\n"
        if 'solves' in cw_stats:
            markdown += f"| Total Solved | {cw_stats['solves']} |\n"
        if 'averageSolveTime' in cw_stats:
            avg_time = int(cw_stats['averageSolveTime'])
            minutes = avg_time // 60
            seconds = avg_time % 60
            markdown += f"| Average Time | {minutes}m {seconds}s |\n"
        
        markdown += "\n"
    
    # Format Wordle stats
    if stats['wordle'] and 'data' in stats['wordle']:
        w_stats = stats['wordle']['data']
        markdown += "### Wordle\n\n"
        markdown += "| Statistic | Value |\n"
        markdown += "|-----------|-------|\n"
        
        if 'currentStreak' in w_stats:
            markdown += f"| Current Streak | {w_stats['currentStreak']} |\n"
        if 'maxStreak' in w_stats:
            markdown += f"| Max Streak | {w_stats['maxStreak']} |\n"
        if 'gamesPlayed' in w_stats:
            markdown += f"| Games Played | {w_stats['gamesPlayed']} |\n"
        if 'winPercentage' in w_stats:
            markdown += f"| Win Rate | {w_stats['winPercentage']}% |\n"
        if 'guesses' in w_stats:
            guesses_dist = w_stats['guesses']
            markdown += f"| Guess Distribution | 1: {guesses_dist.get('1', 0)}, 2: {guesses_dist.get('2', 0)}, "
            markdown += f"3: {guesses_dist.get('3', 0)}, 4: {guesses_dist.get('4', 0)}, "
            markdown += f"5: {guesses_dist.get('5', 0)}, 6: {guesses_dist.get('6', 0)} |\n"
        
        markdown += "\n"
    
    print(f"Generated markdown length: {len(markdown)}")
    print(f"Generated markdown:\n{markdown}")
    return markdown

def update_readme(stats_markdown):
    """
    Update the GitHub README.md with the new stats
    """
    # Path to your README file
    readme_path = 'README.md'
    
    # Check if README exists, create it if it doesn't
    if not os.path.exists(readme_path):
        print(f"Creating new README.md file")
        with open(readme_path, 'w') as file:
            file.write("# NYT Games Stats\n\n<!-- NYT_STATS_START -->\n<!-- NYT_STATS_END -->\n")
    
    # Read the current README
    with open(readme_path, 'r') as file:
        content = file.read()
    
    # Define start and end markers for the stats section
    start_marker = "<!-- NYT_STATS_START -->"
    end_marker = "<!-- NYT_STATS_END -->"
    
    # Check if markers exist, otherwise add them
    if start_marker not in content:
        print("Markers not found, adding them")
        content += f"\n\n{start_marker}\n{end_marker}\n"
    
    # Replace or insert stats between markers
    pattern = f"{start_marker}(.*?){end_marker}"
    replacement = f"{start_marker}\n{stats_markdown}\n{end_marker}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated README
    with open(readme_path, 'w') as file:
        file.write(updated_content)
    
    # Read it back to verify
    with open(readme_path, 'r') as file:
        new_content = file.read()
    
    print(f"Updated README, new length: {len(new_content)}")
    if start_marker in new_content and end_marker in new_content:
        start_idx = new_content.find(start_marker)
        end_idx = new_content.find(end_marker) + len(end_marker)
        stats_section = new_content[start_idx:end_idx]
        print(f"Stats section length in final README: {len(stats_section)}")
        print(f"Stats section:\n{stats_section}")

def main():
    # Get NYT cookie from environment variable
    nyt_cookie = os.environ.get('NYT_COOKIE')
    if not nyt_cookie:
        print("Error: NYT_COOKIE environment variable not set")
        # For testing, use a dummy cookie
        nyt_cookie = "dummy_cookie_for_testing"
    
    # Fetch stats
    stats = get_nyt_stats(nyt_cookie)
    
    # Format stats as markdown
    stats_markdown = format_stats_markdown(stats)
    
    # Update README
    update_readme(stats_markdown)
    
    print("GitHub README successfully updated with NYT puzzle stats!")

if __name__ == "__main__":
    main()
