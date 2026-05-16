"""Interactive Q&A service using Alibaba Cloud Model Studio."""
import json
import logging
from typing import List, Dict, Any, Tuple, Optional
from openai import OpenAI, OpenAIError

from src.base_service import AlibabaPlatformService, ServiceInitError
from src.config import ALIBABA_CLOUD_API_KEY, QWEN_TEXT_MODEL_NAME, SWIMMING_TERMS
from src.storage import DataStore
from src.analytics import PerformanceAnalytics
from src.validation import time_to_seconds

logger = logging.getLogger(__name__)


class QAService(AlibabaPlatformService):
    """Natural language Q&A about Sunny's swimming data."""

    def __init__(self, conversation_history: Optional[List[Dict[str, str]]] = None):
        """Initialize QAService with an optional external conversation history list.

        Args:
            conversation_history: External list reference to use for storing
                conversation state (e.g., st.session_state.chat_history).
                If None, an internal list is created.
        """
        try:
            super().__init__(QWEN_TEXT_MODEL_NAME)
        except ServiceInitError:
            self.client = None
        self.conversation_history = conversation_history if conversation_history is not None else []

    def _get_data_context(self) -> str:
        """Build structured context string from all swimming and body-metrics data.

        Returns:
            Multi-line string summarizing personal bests, recent races, and
            the latest body metrics for inclusion in the LLM system prompt.
        """
        events = DataStore.load_swim_events()
        metrics = DataStore.load_body_metrics()
        pb_df = PerformanceAnalytics.get_personal_bests()
        
        context = []
        context.append("=== Sunny's Swimming Data ===\n")
        
        # Personal bests
        if not pb_df.empty:
            context.append("Personal Bests:")
            for _, row in pb_df.iterrows():
                context.append(f"- {row['stroke'].title()} {row['distance']}m ({row['course']}): {row['time']} on {row['date']}")
            context.append("")
        
        # Recent events
        if events:
            context.append(f"Total Races: {len(events)}")
            context.append(f"Meets Attended: {len(set(e.meet_name for e in events))}")
            recent = sorted(events, key=lambda x: x.date, reverse=True)[:5]
            context.append("\nRecent Races:")
            for e in recent:
                context.append(f"- {e.date}: {e.stroke.title()} {e.distance}m - {e.time} ({e.meet_name})")
            context.append("")
        
        # Body metrics
        if metrics:
            latest = sorted(metrics, key=lambda x: x.date, reverse=True)[0]
            context.append(f"\nLatest Body Metrics ({latest.date}):")
            context.append(f"- Height: {latest.height_cm}cm")
            context.append(f"- Weight: {latest.weight_kg}kg")
            context.append(f"- BMI: {latest.bmi}")
        
        return "\n".join(context)

    def _classify_query(self, question: str) -> str:
        """Classify the intent of a user question.

        Args:
            question: Raw user question string.

        Returns:
            One of 'personal_best', 'trend', 'comparison', 'advice', 'rank',
            or 'general'.
        """
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["best", "fastest", "personal best", "pb"]):
            return "personal_best"
        elif any(word in question_lower for word in ["trend", "improve", "progress", "getting better", "faster"]):
            return "trend"
        elif any(word in question_lower for word in ["compare", "versus", "vs", "better than"]):
            return "comparison"
        elif any(word in question_lower for word in ["advice", "suggest", "training", "drill", "recommend"]):
            return "advice"
        elif any(word in question_lower for word in ["rank", "placement", "place"]):
            return "rank"
        else:
            return "general"

    def answer(self, question: str) -> str:
        """Answer a question about Sunny's swimming data using the Qwen text model.

        Rejects out-of-scope questions, checks API availability, and appends
        the exchange to conversation_history on success.

        Args:
            question: User's natural-language question.

        Returns:
            The model's answer string, or an error/info message if the query
            is out of scope or the API is unavailable.
        """
        # Check if it's out of scope
        if not any(term in question.lower() for term in SWIMMING_TERMS):
            logger.info("Question out of scope, rejecting: %s", question[:80])
            return "I can only answer questions about Sunny's swimming data. Please ask about races, times, strokes, training, or body metrics."
        
        if not ALIBABA_CLOUD_API_KEY or self.client is None:
            logger.warning("Cannot answer question: API key not configured or client unavailable.")
            return "Alibaba Cloud API key not configured. Please set ALIBABA_CLOUD_API_KEY environment variable."
        
        # Get data context
        data_context = self._get_data_context()
        query_type = self._classify_query(question)
        logger.info("Processing question (type=%s): %s", query_type, question[:80])
        
        # Build prompt
        system_prompt = f"""You are a swimming data analyst assistant. Answer questions about Sunny's swimming data using ONLY the provided data context.

Rules:
1. Answer based ONLY on the data provided below
2. Include specific data citations (dates, times, meets) in your answers
3. If data is insufficient, say so clearly
4. Keep answers concise but informative
5. Use the conversation history for context on follow-up questions

Data Context:
{data_context}
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question type: {query_type}\nQuestion: {question}"}
        ]
        
        # Add conversation history for context
        for msg in self.conversation_history[-6:]:  # Last 6 messages
            messages.append(msg)
        
        try:
            logger.debug("Calling API with model '%s' for question type '%s'.", self.model, query_type)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            logger.info("Received API response for question: %s", question[:80])
            
            return answer
            
        except Exception as e:
            logger.error("Failed to answer question: %s: %s", type(e).__name__, e)
            return f"Sorry, I encountered an error: {str(e)}"

    def clear_history(self) -> None:
        """Clear conversation history in-place to keep external references in sync."""
        self.conversation_history.clear()

    @staticmethod
    def get_personal_best_answer(stroke: str, distance: int) -> str:
        """Retrieve Sunny's personal best for a specific stroke and distance.

        Args:
            stroke: Stroke name (e.g., 'freestyle').
            distance: Race distance in meters.

        Returns:
            Human-readable string with the best time and meet details,
            or a message indicating no data is available.
        """
        pb_df = PerformanceAnalytics.get_personal_bests()
        pb_row = pb_df[(pb_df["stroke"] == stroke) & (pb_df["distance"] == distance)]
        
        if pb_row.empty:
            return f"No personal best found for {stroke.title()} {distance}m yet."
        
        row = pb_row.iloc[0]
        return f"Sunny's personal best in {stroke.title()} {distance}m ({row['course']}) is {row['time']}, achieved on {row['date']} at {row['meet_name']}."

    @staticmethod
    def get_trend_answer(stroke: str) -> str:
        """Analyse improvement trend for a specific stroke.

        Args:
            stroke: Stroke name to analyse.

        Returns:
            Human-readable trend summary including percentage improvement
            or decline, or a message if insufficient data.
        """
        events = DataStore.load_swim_events()
        stroke_events = [e for e in events if e.stroke == stroke]
        
        if len(stroke_events) < 2:
            return f"Not enough {stroke.title()} races to analyze trends. Need at least 2 races."
        
        stroke_events.sort(key=lambda x: x.date)
        first = stroke_events[0]
        last = stroke_events[-1]
        first_time = time_to_seconds(first.time)
        last_time = time_to_seconds(last.time)
        improvement = ((first_time - last_time) / first_time * 100) if first_time > 0 else 0
        
        if improvement > 0:
            return f"{stroke.title()} is improving! Time dropped from {first.time} ({first.date}) to {last.time} ({last.date}), a {improvement:.1f}% improvement over {len(stroke_events)} races."
        elif improvement < 0:
            return f"{stroke.title()} times have increased from {first.time} to {last.time} ({abs(improvement):.1f}% change). Consider focusing technique work on this stroke."
        else:
            return f"{stroke.title()} times are consistent around {last.time} across {len(stroke_events)} races."
