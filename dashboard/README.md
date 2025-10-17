# Analytics Dashboard

Streamlit-based dashboard for viewing Outlook and Teams productivity analytics with AI-powered insights.

## Features

- 📧 **Outlook Analytics**: Email statistics, reply productivity, response times, and AI suggestions
- 💬 **Teams Analytics**: Message metrics, engagement scores, productivity scoring, and recommendations
- 💾 **Smart Caching**: Results are cached locally to avoid unnecessary API calls
- 🔄 **Manual Refresh**: Fetch recent analytics on-demand with a button click
- 🎯 **Auto-fetch**: Automatically fetches analytics on first visit if no cache exists
- 🎨 **Beautiful UI**: Clean, intuitive interface with tabs and visual components

## Setup

### 1. Install Dependencies (using uv)

```bash
cd dashboard
uv pip install -r requirements.txt
```

### 2. Ensure FastAPI Server is Running

The dashboard connects to the FastAPI backend. Make sure the server is running:

```bash
# From the project root
uv run python main.py
```

The server should be running at `http://localhost:8000`

### 3. Run the Dashboard

```bash
cd dashboard
uv run streamlit run streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Usage

### First Time Use

1. **Launch Dashboard**: The dashboard will automatically detect if no cached data exists
2. **Auto-fetch**: On first visit, analytics will be fetched automatically for both Outlook and Teams
3. **Wait**: The LLM analysis may take a few minutes to complete
4. **View Results**: Once complete, results are displayed and cached locally

### Subsequent Visits

1. **Instant Load**: Dashboard loads instantly from cache
2. **View Cached Data**: See the timestamp of when data was last fetched
3. **Refresh Option**: Click "🔄 Fetch Recent Analytics" button to get updated insights

### Navigation

- **Tabs**: Switch between "📧 Outlook Analytics" and "💬 Teams Analytics"
- **Sidebar**: Configure API URL and manage cache
- **Refresh Buttons**: Available in each tab to fetch recent data

## Dashboard Sections

### Outlook Analytics

- **Email Statistics**: Total emails, inbox, sent, spam, urgent counts
- **Reply Productivity**: Conversation metrics and reply rates
- **Response Time**: Average time to respond to emails
- **AI Suggestions**: Personalized recommendations for each conversation

### Teams Analytics

- **Communication Metrics**: Messages received, sent, replied, proactive vs reactive
- **Response Metrics**: Average response time and reply rate
- **Engagement Metrics**: Peak activity hours, message length patterns
- **Productivity Scores**: Overall, responsiveness, engagement, and quality scores (0-100)
- **Insights**: AI-generated recommendations with priority levels
- **Executive Summary**: AI-generated summary of communication patterns

## Cache Management

### Automatic Caching

- Analytics results are automatically cached after each fetch
- Cache files are stored in `dashboard/cache/` directory
- Cached data includes timestamp for tracking freshness

### Manual Cache Control

Use the sidebar to:
- **Clear Outlook Cache**: Remove only Outlook analytics cache
- **Clear Teams Cache**: Remove only Teams analytics cache
- **Clear All Cache**: Remove all cached analytics

### Cache Files

- `cache/outlook_analytics.json`: Cached Outlook analytics
- `cache/teams_analytics.json`: Cached Teams analytics

## Configuration

### API URL

Default: `http://localhost:8000`

To change:
1. Use the sidebar "API Base URL" input field
2. The dashboard will use the new URL for all API requests

## Troubleshooting

### "API Server Offline" Error

- Ensure FastAPI server is running at the configured URL
- Check that the server is accessible at `http://localhost:8000/health`

### "Request timed out" Error

- LLM analysis can take 2-5 minutes depending on data size
- Wait for the request to complete
- Timeout is set to 5 minutes (300 seconds)

### Missing Dependencies

```bash
cd dashboard
uv pip install -r requirements.txt
```

### Cache Issues

If you encounter stale or corrupted cache:
1. Use "Clear All Cache" button in sidebar
2. Or manually delete files in `dashboard/cache/` directory
3. Refresh analytics to fetch new data

## Architecture

```
dashboard/
├── streamlit_app.py      # Main Streamlit application
├── api_client.py         # FastAPI client for fetching analytics
├── cache_manager.py      # JSON-based cache management
├── cache/                # Cache storage (auto-created)
│   ├── outlook_analytics.json
│   └── teams_analytics.json
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Development

### Adding New Features

1. **New Metrics**: Add to the respective Pydantic models in `app/schemas/`
2. **UI Components**: Modify display functions in `streamlit_app.py`
3. **Caching**: Extend `cache_manager.py` for additional cache types

### Dependencies

- `streamlit>=1.31.0`: Dashboard framework
- `requests>=2.31.0`: HTTP client for API calls

## Tips

- 💡 Cache analytics to avoid waiting for LLM processing on every visit
- 🔄 Use "Fetch Recent Analytics" sparingly to avoid rate limits
- 📊 Compare metrics over time by noting the timestamp on each fetch
- 🎯 Focus on high-priority insights for maximum impact
