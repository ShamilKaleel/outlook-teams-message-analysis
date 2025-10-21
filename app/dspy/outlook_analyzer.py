import os
from typing import List
import dspy
from dotenv import load_dotenv
import logging
from app.schemas.outlook import OutlookEmail, OutlookMetadata, OutlookAnalysisResult

from config.llm_config import LLMConfig

# Set up logger
logger = logging.getLogger("outlook_analyzer")

# Load environment variables
load_dotenv()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

llm_config = LLMConfig(provider=LLM_PROVIDER)
logger.info(f"Using LLM provider: {llm_config.provider } ({llm_config.model_name})")

# Configure DSPy with the selected LLM
lm = llm_config.create_dspy_lm()
dspy.settings.configure(lm=lm, track_usage=True)


class OutlookEmailAnalysis(dspy.Signature):
    """
    Comprehensive Outlook Email Analysis and Productivity Insights Generator.

    This DSPy signature analyzes a user's complete Outlook email dataset to provide actionable
    insights for improving email management, communication efficiency, and productivity. The
    analysis provides multi-dimensional metrics, productivity scoring, quality assessment, and
    prioritized recommendations.

    Key Analysis Features:
    - Volume Metrics: Emails received, sent, replied, inbox count, spam, urgent, unread backlog
    - Response Metrics: Average/median response times, reply rates, conversation tracking
    - Engagement Metrics: Proactive vs reactive communication, time-of-day trends, activity patterns
    - Quality Indicators: Email length, clarity score, tone assessment, sentiment, conciseness
    - Productivity Scoring: Overall, responsiveness, engagement, and quality scores (0-100)
    - Insights & Recommendations: Prioritized suggestions (high/medium/low) with categories
      (delay/bottleneck/optimal_timing/follow_up/style/workload)

    Input Requirements:
    - all_email: Complete list of Outlook email messages with analytics-relevant fields (24 fields)
    - metadata: Metadata about the fetch operation (total_count, fetched_at, user_email)

    Output:
    - OutlookAnalysisResult: Comprehensive structured analysis organized by metric categories
    """

    # Input Fields with Comprehensive Descriptions
    all_email: List[OutlookEmail] = dspy.InputField(
        desc="Complete set of email messages retrieved from the user's Outlook account for analysis. Each email includes 24 analytics-relevant fields such as message_id, conversation_id, timestamps (created_at, sent_at, received_at), sender information, recipients (to, cc, bcc, reply_to), subject, body_preview, importance, read status, attachments indicator, flag status, and derived fields (is_reply, recipient_count). This rich dataset enables thorough examination of communication patterns, engagement levels, response behaviors, content quality, and contextual relevance for generating comprehensive analytics and actionable insights."
    )

    metadata: OutlookMetadata = dspy.InputField(
        desc="Metadata about the email fetch operation including total_count of emails, fetched_at timestamp (ISO 8601 format), and user_email address of the Outlook account owner whose emails are being analyzed."
    )

    # Output Field
    analysis_result: OutlookAnalysisResult = dspy.OutputField(
        desc="Comprehensive email analysis results organized into structured categories: (1) volume_metrics - emails received/sent/replied, inbox/spam/urgent counts, unread backlog; (2) response_metrics - average/median response time, reply rate %, conversations received/replied; (3) engagement_metrics - proactive vs reactive emails, ratio, peak activity hours (top 3), time-of-day distribution, most active day; (4) quality_indicators - average/median email length, clarity score (0-100), tone (professional/casual/mixed), sentiment distribution, conciseness score (0-100); (5) productivity_score - overall/responsiveness/engagement/quality scores (0-100), trend (improving/stable/declining), benchmark comparison; (6) insights - prioritized list of recommendations with title, description, suggestion, priority (high/medium/low), category (delay/bottleneck/optimal_timing/follow_up/style/workload); (7) summary - AI-generated executive summary highlighting key patterns and areas for improvement."
    )


class OutlookEmailAnalyzer(dspy.Module):
    def __init__(self):
        self.analysis_result = dspy.ChainOfThought(OutlookEmailAnalysis)

    def forward(self, all_email, metadata):
        return self.analysis_result(all_email=all_email, metadata=metadata)
