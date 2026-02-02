# AI Autopilot Configuration

Store your secrets in GitHub Repository Settings -> Secrets and Variables -> Actions.

## Required Secrets
- `AI_API_KEY`: Your API key for the frontier AI model (Gemini, OpenAI, etc.).
- `GITHUB_TOKEN`: This is automatically provided by GitHub Actions, but ensure the "Read and write permissions" are enabled in Repository Settings -> Actions -> General -> Workflow permissions.

## Customization
- **System Prompt**: Edit [system_prompt.md](file:///c:/Users/Admin/Desktop/New%20folder/prompts/system_prompt.md) to change the bot's behavior, tone, or specific coding standards.
- **Model Endpoint**: Change the `AI_MODEL_ENDPOINT` in [.github/workflows/ai-autopilot.yml](file:///c:/Users/Admin/Desktop/New%20folder/.github/workflows/ai-autopilot.yml) to use a different AI provider.
