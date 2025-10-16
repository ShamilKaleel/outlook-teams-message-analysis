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
    analysis includes email distribution across folders, conversation-level reply patterns,
    average response times, and personalized suggestions for better email practices.

    Key Analysis Features:
    - Email categorization by folder (inbox, sent items, spam, urgent with RSVP)
    - Conversation-level reply productivity metrics (received vs. replied conversations)
    - Average response time calculation from received to sent timestamps
    - Actionable suggestions for each replied conversation to improve communication
    - Identification of urgent emails requiring immediate attention

    Input Requirements:
    - all_email: Complete list of Outlook email messages with analytics-relevant fields (24 fields)
    - metadata: Metadata about the fetch operation (total_count, fetched_at, user_email)

    Output:
    - OutlookAnalysisResult: Structured analysis with counts, metrics, response times, and suggestions
    """

    # Input Fields with Comprehensive Descriptions
    all_email: List[OutlookEmail] = dspy.InputField(
        desc="Complete set of email messages retrieved from the user's Outlook account for analysis. Each email includes 24 analytics-relevant fields such as message_id, conversation_id, timestamps (created_at, sent_at, received_at), sender information, recipients (to, cc, bcc, reply_to), subject, body_preview, importance, read status, attachments indicator, flag status, and derived fields (is_reply, recipient_count). This rich dataset enables thorough examination of communication patterns, content quality, and contextual relevance for generating actionable insights and recommendations."
    )

    metadata: OutlookMetadata = dspy.InputField(
        desc="Metadata about the email fetch operation including total_count of emails, fetched_at timestamp (ISO 8601 format), and user_email address of the Outlook account owner whose emails are being analyzed."
    )

    # Output Field
    analysis_result: OutlookAnalysisResult = dspy.OutputField(
        desc="Comprehensive email analysis results including email counts by folder (total, inbox, sent items, spam, urgent with RSVP), reply productivity metrics (conversations received, conversations replied, reply rate at conversation level), average response time in hours calculated from received to sent timestamps for replied emails, and actionable suggestions for each replied conversation to improve email management and communication efficiency."
    )


class OutlookEmailAnalyzer(dspy.Module):
    def __init__(self):
        self.analysis_result = dspy.ChainOfThought(OutlookEmailAnalysis)

    def forward(self, all_email, metadata):
        return self.analysis_result(all_email=all_email, metadata=metadata)
