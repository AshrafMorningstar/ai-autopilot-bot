import os
import sys
import json
import requests
from github import Github

import google.generativeai as genai

# Constants
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")

def get_ai_response(prompt, context):
    """
    Sends a request to the Gemini model.
    """
    if not AI_API_KEY:
        return {
            "status": "error",
            "feedback": "AI_API_KEY not set. Please add it to your repo secrets."
        }
    
    try:
        genai.configure(api_key=AI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        full_prompt = f"{prompt}\n\nCONTENT TO ANALYZE:\n{context}"
        response = model.generate_content(full_prompt)
        
        return {
            "status": "success",
            "feedback": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "feedback": f"AI Error: {str(e)}"
        }

def handle_pull_request(repo, pr_number):
    """
    Fetches PR diffs and requests AI review.
    """
    pr = repo.get_pull(pr_number)
    commits = pr.get_commits()
    files = pr.get_files()
    
    diff_text = ""
    for file in files:
        diff_text += f"\nFile: {file.filename}\n{file.patch}\n"

    system_prompt = open("prompts/system_prompt.md", "r").read()
    
    ai_feedback = get_ai_response(system_prompt, diff_text)
    
    # Post comments to GitHub (simplified)
    pr.create_issue_comment(f"### AI Code Review\n\n{ai_feedback['feedback']}")
    print(f"Posted review to PR #{pr_number}")

def handle_issue(repo, issue_number):
    """
    Categorizes and responds to issues.
    """
    issue = repo.get_issue(issue_number)
    content = f"Title: {issue.title}\nBody: {issue.body}"
    
    system_prompt = open("prompts/system_prompt.md", "r").read()
    
    ai_feedback = get_ai_response(system_prompt, content)
    
    # Auto-labeling logic
    issue.add_to_labels("ai-triaged")
    issue.create_comment(f"### AI Triage\n\n{ai_feedback['feedback']}")
    print(f"Processed Issue #{issue_number}")

def main():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not set.")
        sys.exit(1)

    g = Github(GITHUB_TOKEN)
    repo_name = os.getenv("GITHUB_REPOSITORY")
    repo = g.get_repo(repo_name)
    
    event_name = os.getenv("GITHUB_EVENT_NAME")
    event_path = os.getenv("GITHUB_EVENT_PATH")
    
    with open(event_path, 'r') as f:
        event_data = json.load(f)

    if event_name == "pull_request":
        pr_number = event_data["number"]
        handle_pull_request(repo, pr_number)
    elif event_name == "issues":
        issue_number = event_data["issue"]["number"]
        handle_issue(repo, issue_number)
    else:
        print(f"Event {event_name} not handled.")

if __name__ == "__main__":
    main()
