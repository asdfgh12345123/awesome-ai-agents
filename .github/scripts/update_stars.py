import os
import re
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def get_stars(repo_name):
    try:
        r = requests.get(f"https://api.github.com/repos/{repo_name}", headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("stargazers_count", 0)
    except:
        pass
    return None

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all GitHub repo links and update star counts
    pattern = r'\[([^\]]+)\]\(https://github\.com/([^/]+)/([^)]+)\)'
    matches = re.findall(pattern, content)
    
    updated = 0
    for name, owner, repo in matches:
        repo_path = f"{owner}/{repo}"
        stars = get_stars(repo_path)
        if stars is not None and stars > 0:
            # Format stars
            if stars >= 1000:
                star_str = f"{stars/1000:.0f}k+"
            else:
                star_str = str(stars)
            
            # Update in content
            old_pattern = rf'\| {re.escape(name)} \|.*?\|'
            new_line = f"| {name} | {star_str} |"
            
            # Simple replacement for star column
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if name in line and "github.com" in line:
                    # Update the stars column
                    parts = line.split("|")
                    if len(parts) >= 4:
                        parts[2] = f" {star_str} "
                        lines[i] = "|".join(parts)
                        updated += 1
            content = "\n".join(lines)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Updated {updated} star counts")

if __name__ == "__main__":
    update_readme()
