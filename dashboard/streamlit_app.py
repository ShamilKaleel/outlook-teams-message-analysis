"""
Analytics Dashboard for Microsoft Graph SDK

Streamlit dashboard for viewing Outlook and Teams productivity analytics
with caching support and easy refresh functionality.
"""

import streamlit as st
from datetime import datetime
from cache_manager import CacheManager
from api_client import AnalyticsAPIClient
import visualizations as viz


# Page configuration
st.set_page_config(
    page_title="Productivity Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling - Theme aware
st.markdown("""
    <style>
    /* Main container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Subheader styling - Theme aware */
    h2, h3 {
        padding-top: 1rem;
        opacity: 0.9;
    }

    /* Metric styling - Theme aware */
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Enhanced metric styling for dark theme */
    @media (prefers-color-scheme: dark) {
        [data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05);
        }
    }

    /* Button styling */
    .stButton button {
        border-radius: 0.5rem;
        font-weight: 600;
    }

    /* Expander styling - Theme aware */
    .streamlit-expanderHeader {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 0.5rem;
        font-weight: 500;
    }

    /* Enhanced expander for dark theme */
    @media (prefers-color-scheme: dark) {
        .streamlit-expanderHeader {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    }

    /* Divider styling - Theme aware */
    hr {
        margin: 2rem 0;
        opacity: 0.2;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Info/Success/Warning box styling */
    .stAlert {
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

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
    """Display Outlook analytics with comprehensive visualizations."""
    if not analytics_data:
        st.warning("⚠️ No Outlook analytics data available.")
        if st.button("🔄 Fetch Analytics Now", key="outlook_first_fetch"):
            result, _ = fetch_outlook_analytics(force_refresh=True)
            if result:
                st.rerun()
        return

    data = analytics_data["data"]
    cached_at = analytics_data["cached_at"]

    volume = data.get("volume_metrics", {})
    response = data.get("response_metrics", {})
    engagement = data.get("engagement_metrics", {})
    quality = data.get("quality_indicators", {})
    scores = data.get("productivity_score", {})
    insights = data.get("insights", [])

    # Cache info and refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        if from_cache:
            st.info(f"📦 Showing cached data from: {cached_at}")
        else:
            st.success(f"✅ Fresh data fetched at: {cached_at}")
    with col2:
        if st.button("🔄 Fetch Recent Analytics", key="outlook_refresh", use_container_width=True):
            result, _ = fetch_outlook_analytics(force_refresh=True)
            if result:
                st.rerun()

    st.divider()

    # KPI Cards at Top
    st.subheader("📊 Key Volume Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Received", volume.get("emails_received", 0))
    col2.metric("Sent", volume.get("emails_sent", 0))
    col3.metric("Inbox", volume.get("inbox_count", 0))
    col4.metric("Unread", volume.get("unread_count", 0))
    col5.metric("Urgent", volume.get("urgent_count", 0))

    st.divider()

    # Email Distribution and Reply Productivity
    st.subheader("📧 Email Distribution & Reply Productivity")
    col1, col2 = st.columns(2)

    with col1:
        # Email distribution donut chart
        fig_distribution = viz.create_email_distribution_donut(data)
        st.plotly_chart(fig_distribution, use_container_width=True)

    with col2:
        # Reply productivity funnel
        fig_funnel = viz.create_reply_funnel(data)
        st.plotly_chart(fig_funnel, use_container_width=True)

    st.divider()

    # Response Performance
    st.subheader("⚡ Response Performance")
    col1, col2 = st.columns(2)

    with col1:
        # Reply rate gauge
        fig_gauge = viz.create_reply_rate_gauge(data)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Response time metrics
        avg_response = response.get('average_response_time_hours')
        median_response = response.get('median_response_time_hours')

        if avg_response:
            st.metric(
                "Average Response Time",
                f"{avg_response:.1f} hours",
                help="Average time to respond to emails"
            )
            if avg_response < 4:
                st.success("🟢 Excellent response time!")
            elif avg_response < 24:
                st.info("🟡 Good response time")
            else:
                st.warning("🔴 Consider improving response time")
        else:
            st.metric("Average Response Time", "N/A")

        if median_response:
            st.metric("Median Response Time", f"{median_response:.1f} hours")

    st.divider()

    # Productivity Scores
    st.subheader("🎯 Productivity Scores")
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

    # Trend and benchmark
    if scores.get('trend'):
        st.write(f"**📈 Trend:** {scores.get('trend').title()}")
    if scores.get('benchmark_comparison'):
        st.write(f"**📊 Benchmark:** {scores.get('benchmark_comparison').title()}")

    st.divider()

    # Engagement Metrics
    st.subheader("💬 Engagement Patterns")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Proactive Emails", engagement.get("proactive_emails", 0))
        st.metric("Reactive Emails", engagement.get("reactive_emails", 0))
        ratio = engagement.get("proactive_vs_reactive_ratio", 0)
        st.metric("Proactive/Reactive Ratio", f"{ratio:.2f}")

    with col2:
        peak_hours = engagement.get("peak_activity_hours", [])
        if peak_hours:
            st.write(f"**⏰ Peak Activity Hours:** {', '.join(f'{h}:00' for h in peak_hours)}")

        most_active_day = engagement.get("most_active_day_of_week")
        if most_active_day:
            st.write(f"**📅 Most Active Day:** {most_active_day}")

    st.divider()

    # Quality Indicators
    st.subheader("✨ Quality Assessment")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Avg Email Length", f"{quality.get('average_email_length', 0):.0f} chars")
        st.metric("Clarity Score", f"{quality.get('clarity_score', 0)}/100")

    with col2:
        st.metric("Tone", quality.get('tone_assessment', 'N/A').title())
        st.metric("Conciseness Score", f"{quality.get('conciseness_score', 0)}/100")

    with col3:
        sentiment = quality.get('sentiment_distribution', {})
        if sentiment:
            st.write("**Sentiment Distribution:**")
            for sent_type, count in sentiment.items():
                st.write(f"- {sent_type.title()}: {count}")

    st.divider()

    # Insights & Recommendations
    st.subheader("💡 Insights & Recommendations")

    if insights:
        # Bar chart by category
        fig_insights = viz.create_outlook_insights_by_category_bar(insights)
        st.plotly_chart(fig_insights, use_container_width=True)

        # Detailed insights grouped by priority
        st.write("**Detailed Recommendations:**")

        # Group by priority
        high_priority = [i for i in insights if i.get("priority", "").lower() == "high"]
        medium_priority = [i for i in insights if i.get("priority", "").lower() == "medium"]
        low_priority = [i for i in insights if i.get("priority", "").lower() == "low"]

        # Display by priority
        if high_priority:
            st.write("🔴 **High Priority:**")
            for insight in high_priority[:3]:  # Show top 3
                with st.expander(f"{insight.get('title', 'Insight')} [{insight.get('category', 'general')}]"):
                    st.write(f"**Description:** {insight.get('description', 'N/A')}")
                    st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")

        if medium_priority:
            st.write("🟡 **Medium Priority:**")
            for insight in medium_priority[:2]:  # Show top 2
                with st.expander(f"{insight.get('title', 'Insight')} [{insight.get('category', 'general')}]"):
                    st.write(f"**Description:** {insight.get('description', 'N/A')}")
                    st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")

        if low_priority:
            st.write("🟢 **Low Priority:**")
            for insight in low_priority[:2]:  # Show top 2
                with st.expander(f"{insight.get('title', 'Insight')} [{insight.get('category', 'general')}]"):
                    st.write(f"**Description:** {insight.get('description', 'N/A')}")
                    st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")
    else:
        st.info("No insights available.")

    st.divider()

    # Executive Summary
    st.subheader("📝 Executive Summary")
    summary = data.get("summary", "No summary available.")
    st.markdown(f"_{summary}_")


def display_teams_analytics(analytics_data, from_cache):
    """Display Teams analytics with enhanced visualizations."""
    if not analytics_data:
        st.warning("⚠️ No Teams analytics data available.")
        if st.button("🔄 Fetch Analytics Now", key="teams_first_fetch"):
            result, _ = fetch_teams_analytics(force_refresh=True)
            if result:
                st.rerun()
        return

    data = analytics_data["data"]
    cached_at = analytics_data["cached_at"]
    metrics = data.get("metrics", {})
    scores = data.get("productivity_score", {})
    insights = data.get("insights", [])

    # Cache info and refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        if from_cache:
            st.info(f"📦 Showing cached data from: {cached_at}")
        else:
            st.success(f"✅ Fresh data fetched at: {cached_at}")
    with col2:
        if st.button("🔄 Fetch Recent Analytics", key="teams_refresh", use_container_width=True):
            result, _ = fetch_teams_analytics(force_refresh=True)
            if result:
                st.rerun()

    st.divider()

    # KPI Cards at Top
    st.subheader("📊 Key Communication Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Messages Received", metrics.get("messages_received", 0))
    col2.metric("Messages Sent", metrics.get("messages_sent", 0))
    col3.metric("Messages Replied", metrics.get("messages_replied", 0))
    col4.metric("Avg Message Length", f"{metrics.get('average_message_length', 0):.0f} chars")

    st.divider()

    # Message Volume and Communication Style
    st.subheader("📈 Message Volume & Communication Style")
    col1, col2 = st.columns(2)

    with col1:
        # Message volume bar chart
        fig_volume = viz.create_message_volume_bar(metrics)
        st.plotly_chart(fig_volume, use_container_width=True)

    with col2:
        # Proactive vs Reactive donut chart
        fig_proactive = viz.create_proactive_reactive_donut(metrics)
        st.plotly_chart(fig_proactive, use_container_width=True)

    st.divider()

    # Productivity Scores and Response Metrics
    st.subheader("🎯 Productivity Scores & Response Metrics")
    col1, col2 = st.columns([3, 2])

    with col1:
        # Productivity radar chart
        fig_radar = viz.create_productivity_radar(scores)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        # Response time and reply rate gauges
        fig_response, fig_reply = viz.create_response_gauges(metrics)
        st.plotly_chart(fig_response, use_container_width=True)
        st.plotly_chart(fig_reply, use_container_width=True)

    st.divider()

    # Peak Activity Hours
    st.subheader("⏰ Peak Activity Hours")
    fig_peak = viz.create_peak_hours_bar(metrics)
    st.plotly_chart(fig_peak, use_container_width=True)

    st.divider()

    # Insights Priority Breakdown
    st.subheader("💡 Insights & Recommendations")

    if insights:
        col1, col2 = st.columns([1, 2])

        with col1:
            # Priority pie chart
            fig_priority = viz.create_insights_priority_pie(insights)
            st.plotly_chart(fig_priority, use_container_width=True)

        with col2:
            # Detailed insights grouped by priority
            st.write("**Detailed Recommendations:**")

            # Group by priority
            high_priority = [i for i in insights if i.get("priority", "").lower() == "high"]
            medium_priority = [i for i in insights if i.get("priority", "").lower() == "medium"]
            low_priority = [i for i in insights if i.get("priority", "").lower() == "low"]

            # Display by priority
            if high_priority:
                st.write("🔴 **High Priority:**")
                for insight in high_priority[:3]:  # Show top 3
                    with st.expander(f"{insight.get('title', 'Insight')}"):
                        st.write(f"**Description:** {insight.get('description', 'N/A')}")
                        st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")

            if medium_priority:
                st.write("🟡 **Medium Priority:**")
                for insight in medium_priority[:2]:  # Show top 2
                    with st.expander(f"{insight.get('title', 'Insight')}"):
                        st.write(f"**Description:** {insight.get('description', 'N/A')}")
                        st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")

            if low_priority:
                st.write("🟢 **Low Priority:**")
                for insight in low_priority[:2]:  # Show top 2
                    with st.expander(f"{insight.get('title', 'Insight')}"):
                        st.write(f"**Description:** {insight.get('description', 'N/A')}")
                        st.write(f"**💡 Suggestion:** {insight.get('suggestion', 'N/A')}")
    else:
        st.info("No insights available.")

    st.divider()

    # Executive Summary
    st.subheader("📝 Executive Summary")
    summary = data.get("summary", "No summary available.")
    st.markdown(f"_{summary}_")


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
