import os
from typing import List
import dspy
from dotenv import load_dotenv
import logging
from app.schemas.teams import TeamMessage, TeamsMetadata, TeamsAnalysisResult

from config.llm_config import LLMConfig

# Set up logger
logger = logging.getLogger("teams_analyzer")

# Load environment variables
load_dotenv()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

llm_config = LLMConfig(provider=LLM_PROVIDER)
logger.info(f"Using LLM provider: {llm_config.provider } ({llm_config.model_name})")

# Configure DSPy with the selected LLM
lm = llm_config.create_dspy_lm()
dspy.settings.configure(lm=lm, track_usage=True)


class TeamsChatsAnalysis(dspy.Signature):
    """
    Comprehensive Teams Communication Analysis and Productivity Insights Generator.

    This DSPy signature analyzes a user's complete Teams messages dataset to provide actionable
    insights for improving communication efficiency, responsiveness, and productivity. The
    analysis includes volume metrics, response patterns, engagement analysis, quality assessment,
    productivity scoring, and personalized recommendations.

    Key Analysis Features:
    - Volume metrics: Messages received, sent, and replied across chats
    - Response metrics: Average response times and reply rates
    - Engagement metrics: Proactive vs. reactive communication, peak activity hours
    - Quality indicators: Message length patterns and communication quality
    - Productivity scoring: Responsiveness, engagement, and quality scores
    - Insights & recommendations: Actionable suggestions for improvement

    Input Requirements:
    - all_messages: Complete list of Teams messages with analytics-relevant fields (15 fields)
    - metadata: Metadata about the fetch operation (total_chats, total_messages, fetched_at, user_email)

    Output:
    - TeamsAnalysisResult: Simple structured analysis with metrics, scores, insights, and summary
    """

    # Input Fields with Comprehensive Descriptions
    all_messages: List[TeamMessage] = dspy.InputField(
        desc="Complete set of Teams messages retrieved from the user's chats for analysis. Each message includes 15 analytics-relevant fields such as message_id, chat_id, chat_type, timestamps (created_at, last_modified_at, last_edited_at, deleted_at), sender information (sender_id, sender_name), content details (content, content_type, message_length), message metadata (message_type, importance), and reply tracking (reply_to_id, is_reply). This rich dataset enables thorough examination of communication patterns, responsiveness, engagement levels, and quality for generating actionable insights and recommendations."
    )

    metadata: TeamsMetadata = dspy.InputField(
        desc="Metadata about the Teams data fetch operation including total_chats count, total_messages count, fetched_at timestamp (ISO 8601 format), and user_email address of the Teams account owner whose messages are being analyzed."
    )

    # Output Field
    analysis_result: TeamsAnalysisResult = dspy.OutputField(
        desc="Comprehensive Teams communication analysis results including: (1) metrics - volume metrics (messages received/sent/replied), response metrics (average response time, reply rate), engagement metrics (proactive/reactive messages, peak activity hours), and quality indicators (average message length); (2) productivity_score - overall score, responsiveness score, engagement score, quality score (all 0-100); (3) insights - list of actionable recommendations with title, description, suggestion, and priority; (4) summary - AI-generated executive summary of communication patterns and key findings."
    )


class TeamsChatsAnalyzer(dspy.Module):
    def __init__(self):
        self.analysis_result = dspy.ChainOfThought(TeamsChatsAnalysis)

    def forward(self, all_messages, metadata):
        return self.analysis_result(all_messages=all_messages, metadata=metadata)
