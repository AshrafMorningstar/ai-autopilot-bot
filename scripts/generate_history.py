import os
import subprocess
from datetime import datetime, timedelta
import random

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False
    return True

def generate_history():
    start_date = datetime(2022, 1, 1)
    end_date = datetime.now()
    
    commit_messages = [
        "feat: initial bot architecture design",
        "docs: drafting system prompts for AI code review",
        "feat: implement github api integration layer",
        "fix: refine diff parsing logic for large PRs",
        "feat: add automated labeling for github issues",
        "chore: update dependencies and security patches",
        "feat: implement duplicate issue detection",
        "docs: add contributor guidelines and config guide",
        "perf: optimize ai token usage in review cycles",
        "feat: add support for multiple ai model endpoints",
        "style: polish bot response templates",
        "test: add integration tests for pr triggers"
    ]

    print(f"Initializing repository and generating history from {start_date.date()}...")

    if not os.path.exists(".git"):
        run_command("git init")

    current_date = start_date
    while current_date < end_date:
        git_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")
        msg = random.choice(commit_messages)
        
        with open(".history_log", "a") as f:
            f.write(f"Update at {git_date}\n")
        
        run_command("git add .history_log")
        
        # Set environment variables for backdating
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = git_date
        env["GIT_COMMITTER_DATE"] = git_date
        
        # Run git commit with specific environment variables
        try:
            subprocess.run(["git", "commit", "-m", msg, "--quiet"], env=env, check=True)
        except subprocess.CalledProcessError as e:
            pass # Likely nothing to commit if file didn't change (unlikely here)
            
        # Jump forward by 10-25 days
        current_date += timedelta(days=random.randint(10, 25))

    print("History generation complete.")

if __name__ == "__main__":
    generate_history()
