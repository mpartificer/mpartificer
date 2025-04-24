# nyt_stats.py
import os
import json
import requests
from datetime import datetime
import re

def get_nyt_stats(cookie):
    """
    Fetch NYT puzzle stats using user's cookie
    """
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try to get crossword stats
    crossword_stats = {}
    try:
        crossword_response = requests.get('https://www.nytimes.com/svc/crosswords/v6/puzzle/daily/stats.json', headers=headers)
        if crossword_response.status_code == 200:
            crossword_stats = crossword_response.json()
    except Exception as e:
        print(f"Error fetching crossword stats: {e}")
    
    # Try to get Wordle stats
    wordle_stats = {}
    try:
        wordle_response = requests.get('https://www.nytimes.com/svc/wordle/v2/stats.json', headers=headers)
        if wordle_response.status_code == 200:
            wordle_stats = wordle_response.json()
    except Exception as e:
        print(f"Error fetching Wordle stats: {e}")
    
    # Try to get Spelling Bee stats
    spelling_bee_stats = {}
    try:
        spelling_bee_response = requests.get('https://www.nytimes.com/svc/spelling-bee/v1/stats.json', headers=headers)
        if spelling_bee_response.status_code == 200:
            spelling_bee_stats = spelling_bee_response.json()
    except Exception as e:
        print(f"Error fetching Spelling Bee stats: {e}")
    
    return {
        "crossword": crossword_stats,
        "wordle": wordle_stats,
        "spelling_bee": spelling_bee_stats,
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
    
    # Format Spelling Bee stats
    if stats['spelling_bee'] and 'stats' in stats['spelling_bee']:
        sb_stats = stats['spelling_bee']['stats']
        markdown += "### Spelling Bee\n\n"
        markdown += "| Statistic | Value |\n"
        markdown += "|-----------|-------|\n"
        
        if 'currentStreak' in sb_stats:
            markdown += f"| Current Streak | {sb_stats['currentStreak']} |\n"
        if 'maxStreak' in sb_stats:
            markdown += f"| Max Streak | {sb_stats['maxStreak']} |\n"
        if 'gamesPlayed' in sb_stats:
            markdown += f"| Games Played | {sb_stats['gamesPlayed']} |\n"
        if 'genius' in sb_stats:
            markdown += f"| Genius Achieved | {sb_stats['genius']} times |\n"
        if 'pangrams' in sb_stats:
            markdown += f"| Total Pangrams | {sb_stats['pangrams']} |\n"
    
    return markdown

def update_readme(stats_markdown):
    """
    Update the GitHub README.md with the new stats
    """
    # Path to your README file
    readme_path = 'README.md'
    
    # Read the current README
    with open(readme_path, 'r') as file:
        content = file.read()
    
    # Define start and end markers for the stats section
    start_marker = "<!-- NYT_STATS_START -->"
    end_marker = "<!-- NYT_STATS_END -->"
    
    # Check if markers exist, otherwise add them
    if start_marker not in content:
        content += f"\n\n{start_marker}\n{end_marker}\n"
    
    # Replace or insert stats between markers
    pattern = f"{start_marker}(.*?){end_marker}"
    replacement = f"{start_marker}\n{stats_markdown}\n{end_marker}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated README
    with open(readme_path, 'w') as file:
        file.write(updated_content)

def main():
    # Get NYT cookie from environment variable
    nyt_cookie = os.environ.get('NYT_COOKIE')
    if not nyt_cookie:
        print("Error: NYT_COOKIE environment variable not set")
        return
    
    # Fetch stats
    stats = get_nyt_stats(nyt_cookie)
    
    # Format stats as markdown
    stats_markdown = format_stats_markdown(stats)
    
    # Update README
    update_readme(stats_markdown)
    
    print("GitHub README successfully updated with NYT puzzle stats!")

if __name__ == "__main__":
    main()
