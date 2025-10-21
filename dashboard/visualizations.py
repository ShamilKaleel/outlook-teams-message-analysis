"""
Visualization Functions for Analytics Dashboard

Creates professional Plotly charts for Outlook and Teams analytics.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List


# Color Scheme
COLORS = {
    "primary": "#1f77b4",      # Blue
    "success": "#2ca02c",      # Green
    "warning": "#ff7f0e",      # Orange
    "alert": "#d62728",        # Red
    "neutral": "#7f7f7f",      # Gray
    "purple": "#9467bd",       # Purple
    "pink": "#e377c2",         # Pink
    "teal": "#17becf",         # Teal
}


def create_email_distribution_donut(data: Dict[str, Any]) -> go.Figure:
    """
    Create donut chart showing email distribution by folder.

    Args:
        data: Outlook analytics data with volume_metrics

    Returns:
        Plotly figure
    """
    volume = data.get("volume_metrics", {})

    labels = ["Inbox", "Sent", "Spam", "Urgent"]
    values = [
        volume.get("inbox_count", 0),
        volume.get("emails_sent", 0),
        volume.get("spam_count", 0),
        volume.get("urgent_count", 0),
    ]

    colors = [COLORS["primary"], COLORS["success"], COLORS["alert"], COLORS["warning"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='percent',
        textposition='inside',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])

    total_emails = volume.get("emails_received", 0) + volume.get("emails_sent", 0)

    fig.update_layout(
        title=dict(
            text=f"Email Distribution<br><sub>Total: {total_emails} emails</sub>",
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        height=450,
        margin=dict(t=120, b=60, l=40, r=40)
    )

    return fig


def create_reply_funnel(data: Dict[str, Any]) -> go.Figure:
    """
    Create funnel chart showing reply productivity flow.

    Args:
        data: Outlook analytics data with response_metrics

    Returns:
        Plotly figure
    """
    response = data.get("response_metrics", {})

    conversations_received = response.get("conversations_received", 0)
    conversations_replied = response.get("conversations_replied", 0)

    fig = go.Figure(go.Funnel(
        y=["Conversations Received", "Conversations Replied"],
        x=[conversations_received, conversations_replied],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=[COLORS["primary"], COLORS["success"]]),
        connector={"line": {"color": COLORS["neutral"], "dash": "dot", "width": 2}}
    ))

    fig.update_layout(
        title="Reply Productivity Funnel",
        height=300,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig


def create_reply_rate_gauge(data: Dict[str, Any]) -> go.Figure:
    """
    Create gauge chart for reply rate percentage.

    Args:
        data: Outlook analytics data with response_metrics

    Returns:
        Plotly figure
    """
    response = data.get("response_metrics", {})
    reply_rate = response.get("reply_rate_percentage", 0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=reply_rate,
        title={'text': "Reply Rate"},
        delta={'reference': 70, 'suffix': "%"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': COLORS["primary"]},
            'steps': [
                {'range': [0, 40], 'color': "rgba(214, 39, 40, 0.2)"},    # Red zone
                {'range': [40, 70], 'color': "rgba(255, 127, 14, 0.2)"},  # Yellow zone
                {'range': [70, 100], 'color': "rgba(44, 160, 44, 0.2)"},  # Green zone
            ],
            'threshold': {
                'line': {'color': COLORS["alert"], 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        },
        number={'suffix': "%"}
    ))

    fig.update_layout(
        height=300,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig


def create_message_volume_bar(metrics: Dict[str, Any]) -> go.Figure:
    """
    Create grouped bar chart for Teams message volumes.

    Args:
        metrics: Teams metrics data

    Returns:
        Plotly figure
    """
    categories = ["Received", "Sent", "Replied"]
    values = [
        metrics.get("messages_received", 0),
        metrics.get("messages_sent", 0),
        metrics.get("messages_replied", 0),
    ]

    colors = [COLORS["primary"], COLORS["success"], COLORS["teal"]]

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Message Volume",
        yaxis_title="Count",
        height=350,
        margin=dict(t=60, b=60, l=60, r=40),
        showlegend=False
    )

    return fig


def create_proactive_reactive_donut(metrics: Dict[str, Any]) -> go.Figure:
    """
    Create donut chart showing proactive vs reactive messages.

    Args:
        metrics: Teams metrics data

    Returns:
        Plotly figure
    """
    labels = ["Proactive", "Reactive"]
    values = [
        metrics.get("proactive_messages", 0),
        metrics.get("reactive_messages", 0),
    ]

    colors = [COLORS["success"], COLORS["primary"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        title="Communication Style",
        showlegend=True,
        height=350,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig


def create_productivity_radar(scores: Dict[str, Any]) -> go.Figure:
    """
    Create radar/spider chart for productivity scores.

    Args:
        scores: Teams productivity scores

    Returns:
        Plotly figure
    """
    categories = ["Responsiveness", "Engagement", "Quality", "Overall"]
    values = [
        scores.get("responsiveness_score", 0),
        scores.get("engagement_score", 0),
        scores.get("quality_score", 0),
        scores.get("overall_score", 0),
    ]

    # Close the loop
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor=f'rgba(31, 119, 180, 0.3)',  # Blue with transparency
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=8, color=COLORS["primary"]),
        name='Scores',
        hovertemplate='<b>%{theta}</b><br>Score: %{r}/100<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=25,
                showline=True,
                gridcolor=COLORS["neutral"],
                gridwidth=0.5
            ),
            angularaxis=dict(
                gridcolor=COLORS["neutral"],
                gridwidth=0.5
            )
        ),
        title="Productivity Scores",
        showlegend=False,
        height=400,
        margin=dict(t=80, b=40, l=80, r=80)
    )

    return fig


def create_response_gauges(metrics: Dict[str, Any]) -> tuple:
    """
    Create two gauge charts for response metrics.

    Args:
        metrics: Teams metrics data

    Returns:
        Tuple of (response_time_fig, reply_rate_fig)
    """
    # Response Time Gauge
    avg_response = metrics.get("average_response_time_hours", 0) or 0

    response_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_response,
        title={'text': "Avg Response Time"},
        gauge={
            'axis': {'range': [None, 48]},
            'bar': {'color': COLORS["primary"]},
            'steps': [
                {'range': [0, 4], 'color': "rgba(44, 160, 44, 0.2)"},     # Green
                {'range': [4, 24], 'color': "rgba(255, 127, 14, 0.2)"},   # Yellow
                {'range': [24, 48], 'color': "rgba(214, 39, 40, 0.2)"},   # Red
            ],
        },
        number={'suffix': " hrs"}
    ))

    response_fig.update_layout(
        height=250,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    # Reply Rate Gauge
    reply_rate = metrics.get("reply_rate_percentage", 0)

    reply_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=reply_rate,
        title={'text': "Reply Rate"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': COLORS["success"]},
            'steps': [
                {'range': [0, 40], 'color': "rgba(214, 39, 40, 0.2)"},
                {'range': [40, 70], 'color': "rgba(255, 127, 14, 0.2)"},
                {'range': [70, 100], 'color': "rgba(44, 160, 44, 0.2)"},
            ],
        },
        number={'suffix': "%"}
    ))

    reply_fig.update_layout(
        height=250,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return response_fig, reply_fig


def create_peak_hours_bar(metrics: Dict[str, Any]) -> go.Figure:
    """
    Create bar chart for peak activity hours.

    Args:
        metrics: Teams metrics data with peak_activity_hours

    Returns:
        Plotly figure
    """
    peak_hours = metrics.get("peak_activity_hours", [])

    if not peak_hours:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No peak activity data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=COLORS["neutral"])
        )
        fig.update_layout(height=300, margin=dict(t=40, b=40, l=40, r=40))
        return fig

    # Sort hours and format labels
    peak_hours_sorted = sorted(peak_hours)
    labels = [f"{hour:02d}:00" for hour in peak_hours_sorted]
    # Use dummy values since we don't have actual counts
    values = [100 - (i * 20) for i in range(len(peak_hours_sorted))]  # Descending values

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=COLORS["teal"],
            text=[f"Peak #{i+1}" for i in range(len(values))],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Activity Rank: %{text}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Peak Activity Hours",
        xaxis_title="Time",
        yaxis_title="Activity Level",
        height=300,
        margin=dict(t=60, b=60, l=60, r=40),
        showlegend=False,
        yaxis=dict(showticklabels=False)  # Hide y-axis labels since they're relative
    )

    return fig


def create_insights_priority_pie(insights: List[Dict[str, Any]]) -> go.Figure:
    """
    Create pie chart showing insights breakdown by priority.

    Args:
        insights: List of Teams insights

    Returns:
        Plotly figure
    """
    if not insights:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No insights available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=COLORS["neutral"])
        )
        fig.update_layout(height=300, margin=dict(t=40, b=40, l=40, r=40))
        return fig

    # Count insights by priority
    priority_counts = {"high": 0, "medium": 0, "low": 0}
    for insight in insights:
        priority = insight.get("priority", "medium").lower()
        if priority in priority_counts:
            priority_counts[priority] += 1

    labels = ["🔴 High Priority", "🟡 Medium Priority", "🟢 Low Priority"]
    values = [priority_counts["high"], priority_counts["medium"], priority_counts["low"]]
    colors = [COLORS["alert"], COLORS["warning"], COLORS["success"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+value',
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
    )])

    fig.update_layout(
        title=f"Insights by Priority<br><sub>Total: {sum(values)} insights</sub>",
        showlegend=False,
        height=350,
        margin=dict(t=80, b=40, l=40, r=40)
    )

    return fig


def create_outlook_insights_by_category_bar(insights: List[Dict[str, Any]]) -> go.Figure:
    """
    Create bar chart showing Outlook insights grouped by category.

    Args:
        insights: List of Outlook insights

    Returns:
        Plotly figure
    """
    if not insights:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No insights available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=COLORS["neutral"])
        )
        fig.update_layout(height=300, margin=dict(t=40, b=40, l=40, r=40))
        return fig

    # Count insights by category
    category_counts = {}
    for insight in insights:
        category = insight.get("category", "other")
        category_counts[category] = category_counts.get(category, 0) + 1

    # Sort by count
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    categories = [c[0].replace("_", " ").title() for c in sorted_categories]
    counts = [c[1] for c in sorted_categories]

    # Color code by priority
    colors_map = {
        "delay": COLORS["alert"],
        "bottleneck": COLORS["alert"],
        "optimal_timing": COLORS["success"],
        "follow_up": COLORS["warning"],
        "style": COLORS["primary"],
        "workload": COLORS["purple"]
    }
    bar_colors = [colors_map.get(c[0], COLORS["neutral"]) for c in sorted_categories]

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker_color=bar_colors,
            text=counts,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Insights by Category",
        xaxis_title="Category",
        yaxis_title="Number of Insights",
        height=350,
        margin=dict(t=60, b=80, l=60, r=40),
        showlegend=False
    )

    return fig
