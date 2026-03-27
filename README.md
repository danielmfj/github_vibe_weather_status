# GitHub Weather Status Updater

This Python application updates your GitHub profile status using GitHub API based on current weather in the configured city (default: Copenhagen).

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get API Keys:**
   - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
   - Note: Free tier allows 1000 calls/day

3. **Create GitHub Token:**
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Create a new token with the broadest available scopes (e.g., full `repo` and `user` scopes if available)
   - **Note:** The `/user/status` endpoint requires specific permissions that may not be available on all accounts or token types
   - If you get a 404 error, your account or organization may have restrictions on status updates via API
   - Copy the token and save it securely

4. **Configure Environment:**
   - Edit `.env` with:
     - `OPENWEATHER_API_KEY`
     - `CITY` (optional, default: `Copenhagen`)
     - `GH_TOKEN` (your personal access token)

## Usage

Run:
```bash
python main.py
```

The app will:
1. Fetch current weather in the configured city (`CITY` from .env, defaults to Copenhagen)
2. Map weather to emoji + message
3. Update your GitHub profile status via GraphQL API

## Important Notes
- **API usage:** This app uses the OpenWeatherMap API for weather data and GitHub API `/user/status` for status updates. This is the supported approach for personal status updates (no browser automation needed).
- **Security:** Store `GH_TOKEN` in `.env`, not in source control.
- **API Limitation:** The `/user/status` endpoint may not be available on all GitHub accounts or token types. If you receive a 404 error, the endpoint may be restricted by GitHub or your organization's policies.
- **Rate limits:** Be mindful of API limits for OpenWeatherMap and GitHub (core rate limit for authenticated user).
- **Avatar policy:** GitHub does not support personal avatar updates via public API, so this script uses a status message instead.

## Troubleshooting

- If the banner doesn't update, check the browser window that opens to see if login succeeded
- Verify your LinkedIn profile URL and update the `driver.get()` call in `main.py`
- Ensure images are in the correct format and location