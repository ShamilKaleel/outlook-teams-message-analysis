"""
Analytics Dashboard for Microsoft Graph SDK

Streamlit dashboard for viewing Outlook and Teams productivity analytics
with caching support and easy refresh functionality.
"""

import streamlit as st
from datetime import datetime
from cache_manager import CacheManager
from api_client import AnalyticsAPIClient


# Page configuration
st.set_page_config(
    page_title="Productivity Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
cache_manager = CacheManager()


def get_api_client():
    """Get API client with configured base URL."""
    api_url = st.session_state.get("api_url", "http://localhost:8000")
    return AnalyticsAPIClient(base_url=api_url)


def fetch_outlook_analytics(force_refresh=False):
    """Fetch Outlook analytics with caching."""
    # Check cache first
    if not force_refresh:
        cached_data = cache_manager.load_outlook_analytics()
        if cached_data:
            return cached_data, True

    # Fetch from API
    api_client = get_api_client()

    with st.spinner("🔄 Fetching Outlook analytics from API... This may take a few minutes."):
        try:
            data = api_client.fetch_outlook_analytics()
            # Cache the result
            cache_manager.save_outlook_analytics(data)
            return {"cached_at": datetime.now().isoformat(), "data": data}, False
        except Exception as e:
            st.error(f"❌ Error fetching Outlook analytics: {str(e)}")
            return None, False


def fetch_teams_analytics(force_refresh=False):
    """Fetch Teams analytics with caching."""
    # Check cache first
    if not force_refresh:
        cached_data = cache_manager.load_teams_analytics()
        if cached_data:
            return cached_data, True

    # Fetch from API
    api_client = get_api_client()

    with st.spinner("🔄 Fetching Teams analytics from API... This may take a few minutes."):
        try:
            data = api_client.fetch_teams_analytics()
            # Cache the result
            cache_manager.save_teams_analytics(data)
            return {"cached_at": datetime.now().isoformat(), "data": data}, False
        except Exception as e:
            st.error(f"❌ Error fetching Teams analytics: {str(e)}")
            return None, False


def display_outlook_analytics(analytics_data, from_cache):
    """Display Outlook analytics in a nice format."""
    if not analytics_data:
        st.warning("⚠️ No Outlook analytics data available.")
        if st.button("🔄 Fetch Analytics Now", key="outlook_first_fetch"):
            result, _ = fetch_outlook_analytics(force_refresh=True)
            if result:
                st.rerun()
        return

    data = analytics_data["data"]
    cached_at = analytics_data["cached_at"]

    # Cache info
    if from_cache:
        st.info(f"📦 Showing cached data from: {cached_at}")
    else:
        st.success(f"✅ Fresh data fetched at: {cached_at}")

    # Refresh button
    if st.button("🔄 Fetch Recent Analytics", key="outlook_refresh"):
        result, _ = fetch_outlook_analytics(force_refresh=True)
        if result:
            st.rerun()

    st.divider()

    # Email Statistics
    st.subheader("📧 Email Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Emails", data.get("total_emails", 0))
    col2.metric("Inbox", data.get("inbox", 0))
    col3.metric("Sent Items", data.get("sent_items", 0))
    col4.metric("Spam", data.get("spam_emails", 0))

    col5, col6 = st.columns(2)
    col5.metric("Urgent (RSVP)", data.get("urgent_emails_with_rsvp", 0))
    col6.metric("Avg Response Time",
                f"{data.get('average_response_time', 0):.1f} hours" if data.get('average_response_time') else "N/A")

    st.divider()

    # Reply Productivity
    st.subheader("💬 Reply Productivity")
    reply_prod = data.get("reply_productivity", {})

    col1, col2, col3 = st.columns(3)
    col1.metric("Conversations Received", reply_prod.get("conversations_received", 0))
    col2.metric("Conversations Replied", reply_prod.get("conversations_replied", 0))
    col3.metric("Reply Rate", f"{reply_prod.get('reply_rate_conversation_level', 0):.1f}%")

    st.divider()

    # Suggestions
    st.subheader("💡 AI Suggestions for Improvement")
    suggestions = data.get("suggestions_for_replied_email", [])

    if suggestions:
        for i, suggestion in enumerate(suggestions[:5]):  # Show top 5
            with st.expander(f"💬 Conversation with {suggestion.get('counterparty', 'Unknown')}"):
                st.write(f"**Conversation ID:** `{suggestion.get('conversationId', 'N/A')}`")
                st.write("**Suggestions:**")
                for sug in suggestion.get('suggestions', []):
                    st.write(f"- {sug}")
    else:
        st.info("No suggestions available.")


def display_teams_analytics(analytics_data, from_cache):
    """Display Teams analytics in a nice format."""
    if not analytics_data:
        st.warning("⚠️ No Teams analytics data available.")
        if st.button("🔄 Fetch Analytics Now", key="teams_first_fetch"):
            result, _ = fetch_teams_analytics(force_refresh=True)
            if result:
                st.rerun()
        return

    data = analytics_data["data"]
    cached_at = analytics_data["cached_at"]

    # Cache info
    if from_cache:
        st.info(f"📦 Showing cached data from: {cached_at}")
    else:
        st.success(f"✅ Fresh data fetched at: {cached_at}")

    # Refresh button
    if st.button("🔄 Fetch Recent Analytics", key="teams_refresh"):
        result, _ = fetch_teams_analytics(force_refresh=True)
        if result:
            st.rerun()

    st.divider()

    # Metrics
    st.subheader("📊 Communication Metrics")
    metrics = data.get("metrics", {})

    col1, col2, col3 = st.columns(3)
    col1.metric("Messages Received", metrics.get("messages_received", 0))
    col2.metric("Messages Sent", metrics.get("messages_sent", 0))
    col3.metric("Messages Replied", metrics.get("messages_replied", 0))

    col4, col5, col6 = st.columns(3)
    col4.metric("Proactive Messages", metrics.get("proactive_messages", 0))
    col5.metric("Reactive Messages", metrics.get("reactive_messages", 0))
    col6.metric("Reply Rate", f"{metrics.get('reply_rate_percentage', 0):.1f}%")

    col7, col8 = st.columns(2)
    col7.metric("Avg Response Time",
                f"{metrics.get('average_response_time_hours', 0):.1f} hours" if metrics.get('average_response_time_hours') else "N/A")
    col8.metric("Avg Message Length", f"{metrics.get('average_message_length', 0):.0f} chars")

    # Peak Activity Hours
    peak_hours = metrics.get("peak_activity_hours", [])
    if peak_hours:
        st.write(f"**⏰ Peak Activity Hours:** {', '.join(f'{h}:00' for h in peak_hours)}")

    st.divider()

    # Productivity Scores
    st.subheader("🎯 Productivity Scores")
    scores = data.get("productivity_score", {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Overall Score", f"{scores.get('overall_score', 0)}/100")
        st.progress(scores.get('overall_score', 0) / 100)

    with col2:
        st.metric("Responsiveness", f"{scores.get('responsiveness_score', 0)}/100")
        st.progress(scores.get('responsiveness_score', 0) / 100)

    with col3:
        st.metric("Engagement", f"{scores.get('engagement_score', 0)}/100")
        st.progress(scores.get('engagement_score', 0) / 100)

    with col4:
        st.metric("Quality", f"{scores.get('quality_score', 0)}/100")
        st.progress(scores.get('quality_score', 0) / 100)

    st.divider()

    # Insights
    st.subheader("💡 Insights & Recommendations")
    insights = data.get("insights", [])

    if insights:
        for insight in insights:
            priority = insight.get("priority", "medium")
            emoji = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"

            with st.expander(f"{emoji} {insight.get('title', 'Insight')} ({priority.upper()})"):
                st.write(f"**Description:** {insight.get('description', 'N/A')}")
                st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")
    else:
        st.info("No insights available.")

    st.divider()

    # Summary
    st.subheader("📝 Executive Summary")
    summary = data.get("summary", "No summary available.")
    st.write(summary)


def main():
    """Main dashboard application."""
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")

        # API URL configuration
        api_url = st.text_input(
            "API Base URL",
            value=st.session_state.get("api_url", "http://localhost:8000"),
            help="FastAPI server URL"
        )
        st.session_state["api_url"] = api_url

        # Check API health
        api_client = get_api_client()
        if api_client.check_health():
            st.success("✅ API Server Connected")
        else:
            st.error("❌ API Server Offline")

        st.divider()

        # Cache management
        st.subheader("🗄️ Cache Management")
        if cache_manager.has_outlook_cache():
            if st.button("Clear Outlook Cache"):
                cache_manager.clear_outlook_cache()
                st.success("Outlook cache cleared!")
                st.rerun()

        if cache_manager.has_teams_cache():
            if st.button("Clear Teams Cache"):
                cache_manager.clear_teams_cache()
                st.success("Teams cache cleared!")
                st.rerun()

        if cache_manager.has_outlook_cache() or cache_manager.has_teams_cache():
            if st.button("Clear All Cache"):
                cache_manager.clear_all_cache()
                st.success("All cache cleared!")
                st.rerun()

    # Main content
    st.title("📊 Productivity Analytics Dashboard")
    st.markdown("### AI-Powered Communication Analytics for Outlook & Teams")

    # Tabs
    tab1, tab2 = st.tabs(["📧 Outlook Analytics", "💬 Teams Analytics"])

    with tab1:
        # Auto-fetch on first load if no cache
        if not cache_manager.has_outlook_cache():
            st.info("🎯 No cached data found. Fetching analytics for the first time...")
            outlook_data, from_cache = fetch_outlook_analytics(force_refresh=True)
        else:
            outlook_data, from_cache = fetch_outlook_analytics(force_refresh=False)

        display_outlook_analytics(outlook_data, from_cache)

    with tab2:
        # Auto-fetch on first load if no cache
        if not cache_manager.has_teams_cache():
            st.info("🎯 No cached data found. Fetching analytics for the first time...")
            teams_data, from_cache = fetch_teams_analytics(force_refresh=True)
        else:
            teams_data, from_cache = fetch_teams_analytics(force_refresh=False)

        display_teams_analytics(teams_data, from_cache)


if __name__ == "__main__":
    main()
