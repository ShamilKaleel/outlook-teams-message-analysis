"""
Pydantic schemas for Outlook API responses.

These models define the structure of Outlook email data
returned by the Microsoft Graph API endpoints.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class EmailRecipient(BaseModel):
    """
    Represents an email recipient (used in to, cc, bcc, reply_to fields).

    Attributes:
        email: Email address of the recipient
        name: Display name of the recipient
    """
    email: str = Field(..., description="Email address of the recipient")
    name: str = Field(..., description="Display name of the recipient")


class OutlookMetadata(BaseModel):
    """
    Metadata about the Outlook email fetch operation.

    Attributes:
        total_count: Total number of emails retrieved
        fetched_at: ISO 8601 timestamp of when the data was fetched
        user_email: Email address of the user whose data was fetched
    """
    total_count: int = Field(..., description="Total number of emails retrieved")
    fetched_at: str = Field(..., description="ISO 8601 timestamp of fetch time")
    user_email: str = Field(..., description="Target user's email address")


class OutlookEmail(BaseModel):
    """
    Represents a single Outlook email message.

    This model includes all analytics-relevant fields extracted from
    Microsoft Graph API email message objects.

    Attributes:
        message_id: Unique identifier for the message
        conversation_id: ID of the conversation thread this message belongs to
        folder_id: ID of the parent folder containing this message
        internet_message_id: Internet standard message ID
        created_at: ISO 8601 timestamp of message creation
        sent_at: ISO 8601 timestamp of when message was sent
        received_at: ISO 8601 timestamp of when message was received
        last_modified_at: ISO 8601 timestamp of last modification
        sender_email: Email address of the sender
        sender_name: Display name of the sender
        to_recipients: List of To recipients
        cc_recipients: List of CC recipients
        bcc_recipients: List of BCC recipients
        reply_to: List of Reply-To addresses
        subject: Email subject line
        body_preview: Preview/snippet of the email body
        importance: Message importance level (normal, high, low)
        is_draft: Whether this message is a draft
        is_read: Whether this message has been read
        has_attachments: Whether this message has attachments
        flag_status: Status of the message flag (flagged, complete, notFlagged)
        is_reply: Boolean indicating if this message is a reply
        recipient_count: Total number of recipients (to + cc + bcc)
    """
    # Identifiers
    message_id: str = Field(..., description="Unique message identifier")
    conversation_id: Optional[str] = Field(None, description="Conversation thread identifier")
    folder_id: Optional[str] = Field(None, description="Parent folder identifier")
    internet_message_id: Optional[str] = Field(None, description="Internet standard message ID")

    # Timestamps
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    sent_at: Optional[str] = Field(None, description="ISO 8601 sent timestamp")
    received_at: Optional[str] = Field(None, description="ISO 8601 received timestamp")
    last_modified_at: Optional[str] = Field(None, description="ISO 8601 last modified timestamp")

    # Sender information
    sender_email: Optional[str] = Field(None, description="Sender's email address")
    sender_name: Optional[str] = Field(None, description="Sender's display name")

    # Recipients
    to_recipients: list[EmailRecipient] = Field(default_factory=list, description="List of To recipients")
    cc_recipients: list[EmailRecipient] = Field(default_factory=list, description="List of CC recipients")
    bcc_recipients: list[EmailRecipient] = Field(default_factory=list, description="List of BCC recipients")
    reply_to: list[EmailRecipient] = Field(default_factory=list, description="List of Reply-To addresses")

    # Content
    subject: Optional[str] = Field(None, description="Email subject line")
    body_preview: Optional[str] = Field(None, description="Preview/snippet of email body")

    # Metadata
    importance: Optional[str] = Field(None, description="Message importance (normal, high, low)")
    is_draft: Optional[bool] = Field(None, description="Whether message is a draft")
    is_read: Optional[bool] = Field(None, description="Whether message has been read")
    has_attachments: Optional[bool] = Field(None, description="Whether message has attachments")
    flag_status: Optional[str] = Field(None, description="Flag status (flagged, complete, notFlagged)")

    # Derived fields
    is_reply: bool = Field(False, description="Whether this message is a reply")
    recipient_count: int = Field(0, description="Total number of recipients")


class OutlookEmailsResponse(BaseModel):
    """
    Complete response model for Outlook emails endpoint.

    Contains metadata about the operation and list of email messages.

    Attributes:
        metadata: Metadata about the fetch operation
        emails: List of all email messages retrieved
    """
    metadata: OutlookMetadata = Field(..., description="Fetch operation metadata")
    emails: list[OutlookEmail] = Field(..., description="List of all emails")


class OutlookVolumeMetrics(BaseModel):
    """
    Volume metrics for Outlook email analysis.

    Tracks email counts across different categories for comprehensive volume analysis.

    Attributes:
        emails_received: Total number of emails received
        emails_sent: Total number of emails sent (from sent items)
        emails_replied: Total number of emails that were replied to
        inbox_count: Current count of emails in inbox folder
        spam_count: Number of spam/junk emails identified
        urgent_count: Number of urgent emails requiring RSVP or immediate action
        unread_count: Number of unread emails (backlog tracking)
    """
    emails_received: int = Field(..., description="Total number of emails received")
    emails_sent: int = Field(..., description="Total number of emails sent")
    emails_replied: int = Field(..., description="Total number of emails replied to")
    inbox_count: int = Field(..., description="Current inbox email count")
    spam_count: int = Field(..., description="Number of spam/junk emails")
    urgent_count: int = Field(..., description="Number of urgent emails requiring action")
    unread_count: int = Field(..., description="Number of unread emails (backlog)")


class OutlookResponseMetrics(BaseModel):
    """
    Response performance metrics for Outlook email analysis.

    Measures how quickly and consistently emails are responded to.

    Attributes:
        average_response_time_hours: Average time to respond in hours
        median_response_time_hours: Median response time in hours
        reply_rate_percentage: Percentage of received emails that were replied to
        conversations_received: Total number of unique conversation threads received
        conversations_replied: Number of conversations that received at least one reply
    """
    average_response_time_hours: Optional[float] = Field(None, description="Average response time in hours")
    median_response_time_hours: Optional[float] = Field(None, description="Median response time in hours")
    reply_rate_percentage: float = Field(..., description="Percentage of emails replied to")
    conversations_received: int = Field(..., description="Total unique conversations received")
    conversations_replied: int = Field(..., description="Conversations with at least one reply")


class OutlookEngagementMetrics(BaseModel):
    """
    Engagement metrics for Outlook email communication patterns.

    Analyzes proactive vs reactive behavior and activity timing patterns.

    Attributes:
        proactive_emails: Number of emails initiated (not replies)
        reactive_emails: Number of emails that are replies
        proactive_vs_reactive_ratio: Ratio of proactive to reactive emails
        peak_activity_hours: Top 3 hours of email activity (0-23 hour format)
        emails_by_time_of_day: Distribution of emails by time period
        most_active_day_of_week: Most active day for email communication
    """
    proactive_emails: int = Field(..., description="Emails initiated (not replies)")
    reactive_emails: int = Field(..., description="Reply emails")
    proactive_vs_reactive_ratio: float = Field(..., description="Ratio of proactive to reactive")
    peak_activity_hours: List[int] = Field(default_factory=list, description="Top 3 activity hours (0-23)")
    emails_by_time_of_day: dict = Field(default_factory=dict, description="Email distribution by time period (morning/afternoon/evening/night)")
    most_active_day_of_week: Optional[str] = Field(None, description="Most active day of the week")


class OutlookQualityIndicators(BaseModel):
    """
    Quality assessment indicators for Outlook email communication.

    Evaluates email quality based on length, tone, sentiment, and clarity.

    Attributes:
        average_email_length: Average character length of emails
        median_email_length: Median character length of emails
        clarity_score: Email clarity rating (0-100, higher is better)
        tone_assessment: Overall tone classification (professional/casual/mixed)
        sentiment_distribution: Distribution of sentiment (positive/neutral/negative counts)
        conciseness_score: Conciseness rating (0-100, higher means more concise)
    """
    average_email_length: float = Field(..., description="Average email character length")
    median_email_length: float = Field(..., description="Median email character length")
    clarity_score: int = Field(..., ge=0, le=100, description="Clarity score (0-100)")
    tone_assessment: str = Field(..., description="Tone classification: professional/casual/mixed")
    sentiment_distribution: dict = Field(default_factory=dict, description="Sentiment counts (positive/neutral/negative)")
    conciseness_score: int = Field(..., ge=0, le=100, description="Conciseness score (0-100)")


class OutlookProductivityScore(BaseModel):
    """
    Productivity scoring system for Outlook email management.

    Generates comprehensive scores reflecting responsiveness, engagement, and quality.

    Attributes:
        overall_score: Overall productivity score (0-100)
        responsiveness_score: Response speed and reply rate score (0-100)
        engagement_score: Communication engagement score (0-100)
        quality_score: Email quality and clarity score (0-100)
        trend: Performance trend indicator
        benchmark_comparison: Comparison to personal benchmark
    """
    overall_score: int = Field(..., ge=0, le=100, description="Overall productivity score (0-100)")
    responsiveness_score: int = Field(..., ge=0, le=100, description="Responsiveness score (0-100)")
    engagement_score: int = Field(..., ge=0, le=100, description="Engagement score (0-100)")
    quality_score: int = Field(..., ge=0, le=100, description="Quality score (0-100)")
    trend: Optional[str] = Field(None, description="Trend: improving/stable/declining")
    benchmark_comparison: Optional[str] = Field(None, description="Comparison: above/at/below benchmark")


class OutlookInsight(BaseModel):
    """
    Structured insight or recommendation for Outlook email management.

    Provides actionable recommendations with priority levels and categories.

    Attributes:
        title: Short insight title
        description: Detailed explanation of the insight
        suggestion: Actionable recommendation
        priority: Priority level (high/medium/low)
        category: Insight category (delay/bottleneck/optimal_timing/follow_up/style/workload)
    """
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Detailed description")
    suggestion: str = Field(..., description="Actionable suggestion")
    priority: str = Field(..., description="Priority level: high, medium, or low")
    category: str = Field(..., description="Category: delay/bottleneck/optimal_timing/follow_up/style/workload")


class OutlookAnalysisResult(BaseModel):
    """
    Comprehensive analytics result for Outlook email analysis.

    Organized structure containing volume metrics, response metrics, engagement patterns,
    quality indicators, productivity scoring, insights, and executive summary.

    Attributes:
        volume_metrics: Email volume tracking across categories
        response_metrics: Response performance and reply rates
        engagement_metrics: Proactive vs reactive patterns and timing trends
        quality_indicators: Email quality assessment (clarity, tone, sentiment)
        productivity_score: Multi-dimensional productivity scores (0-100)
        insights: Prioritized actionable recommendations
        summary: AI-generated executive summary of email communication patterns
    """
    volume_metrics: OutlookVolumeMetrics = Field(..., description="Email volume metrics")
    response_metrics: OutlookResponseMetrics = Field(..., description="Response performance metrics")
    engagement_metrics: OutlookEngagementMetrics = Field(..., description="Engagement patterns and timing")
    quality_indicators: OutlookQualityIndicators = Field(..., description="Email quality assessment")
    productivity_score: OutlookProductivityScore = Field(..., description="Productivity scores (0-100)")
    insights: List[OutlookInsight] = Field(..., description="Prioritized insights and recommendations")
    summary: str = Field(..., description="AI-generated executive summary")
