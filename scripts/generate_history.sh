#!/bin/bash

# Configuration
START_YEAR=2022
END_YEAR=2026
COMMIT_MESSAGES=(
    "feat: initial bot architecture design"
    "docs: drafting system prompts for AI code review"
    "feat: implement github api integration layer"
    "fix: refine diff parsing logic for large PRs"
    "feat: add automated labeling for github issues"
    "chore: update dependencies and security patches"
    "feat: implement duplicate issue detection"
    "docs: add contributor guidelines and config guide"
    "perf: optimize ai token usage in review cycles"
    "feat: add support for multiple ai model endpoints"
    "style: polish bot response templates"
    "test: add integration tests for pr triggers"
)

# Initialize git if not already
if [ ! -d ".git" ]; then
    git init
fi

echo "Generating backdated history from $START_YEAR to today..."

# Current date in seconds
CURRENT_DATE=$(date +%s)
# Start date (Jan 1, 2022)
START_DATE=$(date -d "$START_YEAR-01-01" +%s)

SECONDS_IN_DAY=86400
SECONDS_IN_MONTH=$((SECONDS_IN_DAY * 30))

# Loop from start date to current date
TEMP_DATE=$START_DATE
while [ $TEMP_DATE -lt $CURRENT_DATE ]; do
    # Format date for git
    GIT_DATE=$(date -d "@$TEMP_DATE" +"%Y-%m-%dT%H:%M:%S")
    
    # Pick a random commit message
    MSG=${COMMIT_MESSAGES[$RANDOM % ${#COMMIT_MESSAGES[@]}]}
    
    # Add a dummy change
    echo "// Update at $GIT_DATE" >> .history_log
    git add .history_log
    
    # Commit with backdate
    GIT_AUTHOR_DATE="$GIT_DATE" GIT_COMMITTER_DATE="$GIT_DATE" git commit -m "$MSG" --quiet
    
    # Jump forward by a random interval (2-4 weeks)
    INTERVAL=$(( (RANDOM % 14 + 14) * SECONDS_IN_DAY ))
    TEMP_DATE=$((TEMP_DATE + INTERVAL))
done

echo "History generation complete. Repository now has a timeline starting from 2022."
