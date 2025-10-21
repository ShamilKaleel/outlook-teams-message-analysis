# Analytics Dashboard

Professional Streamlit dashboard with 10 interactive Plotly visualizations for Outlook and Teams productivity analytics powered by AI insights.

## Features

- 📊 **10 Interactive Plotly Charts**: Donut charts, funnel charts, gauges, bar charts, radar charts, and pie charts
- 📧 **Outlook Analytics**: Email distribution donut, reply productivity funnel, response time gauges, and conversation bar chart
- 💬 **Teams Analytics**: Message volume bars, communication style donut, productivity radar, response gauges, peak activity bars, and priority pie chart
- 💾 **Smart Caching**: Results are cached locally to avoid unnecessary API calls
- 🔄 **Manual Refresh**: Fetch recent analytics on-demand with a button click
- 🎯 **Auto-fetch**: Automatically fetches analytics on first visit if no cache exists
- 🎨 **Beautiful UI**: Professional interface with custom CSS styling, color-coded metrics, and responsive grid layouts

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

### Outlook Analytics Tab

**Visualizations:**
1. **Email Distribution Donut Chart**: Visual breakdown of emails by folder (Inbox, Sent, Spam, Urgent)
2. **Reply Productivity Funnel**: Conversion flow from conversations received to replied
3. **Reply Rate Gauge**: Performance indicator with color-coded zones (0-100%)
4. **Top Conversations Bar Chart**: Shows conversations needing most attention

**Sections:**
- **Key Metrics Overview**: KPI cards for total emails, inbox, sent items, urgent
- **Email Distribution & Reply Productivity**: Side-by-side donut and funnel charts
- **Response Performance**: Gauge chart + response time metric with status indicators
- **Conversations Needing Attention**: Bar chart + detailed AI suggestions

### Teams Analytics Tab

**Visualizations:**
1. **Message Volume Bar Chart**: Grouped bars for received, sent, replied
2. **Communication Style Donut Chart**: Proactive vs reactive message breakdown
3. **Productivity Radar Chart**: 4-dimension spider chart (Overall, Responsiveness, Engagement, Quality)
4. **Response Time Gauge**: Performance indicator for avg response time (0-48 hours)
5. **Reply Rate Gauge**: Performance indicator for reply percentage (0-100%)
6. **Peak Activity Hours Bar Chart**: Shows top 3 activity hours
7. **Insights Priority Pie Chart**: Distribution of high/medium/low priority insights

**Sections:**
- **Key Communication Metrics**: KPI cards for messages and avg message length
- **Message Volume & Communication Style**: Side-by-side bar and donut charts
- **Productivity Scores & Response Metrics**: Radar chart + dual gauges
- **Peak Activity Hours**: Bar chart showing optimal communication times
- **Insights & Recommendations**: Priority pie chart + grouped detailed insights by priority level
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


### Cache Issues

If you encounter stale or corrupted cache:
1. Use "Clear All Cache" button in sidebar
2. Or manually delete files in `dashboard/cache/` directory
3. Refresh analytics to fetch new data

## Architecture

```
dashboard/
├── streamlit_app.py      # Main Streamlit application with enhanced UI
├── visualizations.py     # Plotly chart creation functions (10 chart types)
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
- `plotly>=5.18.0`: Interactive visualization library for professional charts

## Tips

- 💡 Cache analytics to avoid waiting for LLM processing on every visit
- 🔄 Use "Fetch Recent Analytics" sparingly to avoid rate limits
- 📊 Compare metrics over time by noting the timestamp on each fetch
- 🎯 Focus on high-priority insights for maximum impact
- 🖱️ Hover over charts for detailed tooltips with exact values
- 📈 Use radar chart to quickly identify productivity gaps across dimensions
- 🎨 Color-coded gauges show performance zones (green=good, yellow=moderate, red=needs attention)
