import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        transition: width 0.3s ease;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_day" not in st.session_state:
    st.session_state.current_day = 1

# API base URL
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8001")


def main():
    # Header
    st.markdown(
        '<h1 class="main-header">🧠 AI Interview Assistant</h1>', unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.header("📊 Quick Stats")

        # Get status
        try:
            status_response = requests.get(f"{API_BASE_URL}/progress/status")
            if status_response.status_code == 200:
                status = status_response.json()

                st.metric("Overall Progress", f"{status['overall_progress']:.1f}%")
                st.metric("Days Remaining", status["days_remaining"])
                st.metric("Readiness Score", f"{status['readiness_score']:.1f}%")

                # Category progress
                st.subheader("Category Progress")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("DSA", f"{status['dsa_progress']:.1f}%")
                    st.metric("ML", f"{status['ml_progress']:.1f}%")
                with col2:
                    st.metric(
                        "System Design", f"{status['system_design_progress']:.1f}%"
                    )
                    st.metric("Behavioral", f"{status['behavioral_progress']:.1f}%")
        except:
            st.warning("Unable to fetch status")

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🎯 Daily Plan",
            "💬 AI Chat",
            "📈 Progress Analytics",
            "📅 Study Calendar",
            "⚙️ Settings",
        ]
    )

    with tab1:
        show_daily_plan()

    with tab2:
        show_ai_chat()

    with tab3:
        show_analytics()

    with tab4:
        show_calendar()

    with tab5:
        show_settings()


def show_daily_plan():
    st.header("🎯 Today's Study Plan")

    # Day selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_day = st.selectbox(
            "Select Day", range(1, 46), index=st.session_state.current_day - 1
        )

    # Get daily plan
    try:
        plan_response = requests.get(f"{API_BASE_URL}/progress/plan/{selected_day}")
        if plan_response.status_code == 200:
            plan = plan_response.json()

            # Display plan
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader(f"Day {plan['day']} - {', '.join(plan['topics'])}")

                # Topics
                st.write("**Topics to Cover:**")
                for topic in plan["topics"]:
                    st.write(f"• {topic}")

                # Learning objectives
                st.write("**Learning Objectives:**")
                for objective in plan["learning_objectives"]:
                    st.write(f"• {objective}")

                # Practice problems
                st.write("**Practice Problems:**")
                for problem in plan["practice_problems"]:
                    st.write(f"• {problem}")

            with col2:
                st.metric("Estimated Hours", f"{plan['estimated_hours']}h")

                # Resources
                st.write("**Resources:**")
                for resource in plan["resources"]:
                    st.write(f"📚 {resource}")

                # Log progress button
                if st.button("✅ Mark Day Complete", type="primary"):
                    log_progress(selected_day, plan)
                    st.success(f"Day {selected_day} marked as complete!")
        else:
            st.error("Unable to fetch daily plan")

    except Exception as e:
        st.error(f"Error loading plan: {str(e)}")


def show_ai_chat():
    st.header("💬 AI Interview Coach")

    # Topic selection
    col1, col2 = st.columns([1, 2])
    with col1:
        topic_category = st.selectbox(
            "Select Topic Category",
            ["General", "DSA", "Machine Learning", "System Design", "Behavioral"],
            help="Choose a specific topic for more targeted assistance",
        )

    # Chat interface
    chat_container = st.container()

    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI Coach:** {message['content']}")

        # Chat input
        user_input = st.text_area("Ask your question:", height=100)

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Send", type="primary"):
                if user_input.strip():
                    send_chat_message(user_input, topic_category)
                    st.rerun()
        with col2:
            if st.button("Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()


def show_analytics():
    st.header("📈 Progress Analytics")

    try:
        # Get analytics
        analytics_response = requests.get(f"{API_BASE_URL}/progress/analytics")
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()

            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Total Hours Studied", f"{analytics['total_hours_studied']:.1f}h"
                )
            with col2:
                st.metric("Problems Solved", analytics["problems_solved"])
            with col3:
                st.metric("Topics Covered", len(analytics["topics_covered"]))
            with col4:
                st.metric("Study Sessions", len(analytics["confidence_trend"]))

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                # Confidence trend
                if analytics["confidence_trend"]:
                    df = pd.DataFrame(analytics["confidence_trend"])
                    fig = px.line(
                        df,
                        x="day",
                        y="confidence",
                        title="Confidence Level Trend",
                        labels={"confidence": "Confidence Level", "day": "Day"},
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Topics covered
                if analytics["topics_covered"]:
                    topic_counts = (
                        pd.Series(analytics["topics_covered"]).value_counts().head(10)
                    )
                    fig = px.bar(
                        x=topic_counts.values,
                        y=topic_counts.index,
                        title="Most Studied Topics",
                        orientation="h",
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

            # Weak and strong areas
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🎯 Focus Areas (Weak)")
                if analytics["weak_areas"]:
                    for area in analytics["weak_areas"]:
                        st.write(f"• {area}")
                else:
                    st.write("No weak areas identified!")

            with col2:
                st.subheader("✅ Strong Areas")
                if analytics["strong_areas"]:
                    for area in analytics["strong_areas"]:
                        st.write(f"• {area}")
                else:
                    st.write("Keep building strength in all areas!")

            # Recommendations
            st.subheader("💡 AI Recommendations")
            for rec in analytics["next_recommendations"]:
                st.write(f"• {rec}")

        else:
            st.warning(
                "No progress data available yet. Start studying to see analytics!"
            )

    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")


def show_calendar():
    st.header("📅 45-Day Study Calendar")

    try:
        # Get full plan
        plan_response = requests.get(f"{API_BASE_URL}/progress/plan")
        if plan_response.status_code == 200:
            plans = plan_response.json()

            # Create calendar view
            weeks = []
            current_week = []

            for plan in plans:
                current_week.append(plan)
                if len(current_week) == 7:
                    weeks.append(current_week)
                    current_week = []

            if current_week:
                weeks.append(current_week)

            # Display calendar
            for week_num, week in enumerate(weeks, 1):
                st.subheader(f"Week {week_num}")

                cols = st.columns(7)
                for i, day_plan in enumerate(week):
                    with cols[i]:
                        day_num = day_plan["day"]
                        topics = day_plan["topics"]

                        # Day card
                        st.markdown(
                            f"""
                        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin: 5px;">
                            <h4>Day {day_num}</h4>
                            <p><strong>{topics[0]}</strong></p>
                            <p>{day_plan['estimated_hours']}h</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

        else:
            st.error("Unable to load study plan")

    except Exception as e:
        st.error(f"Error loading calendar: {str(e)}")


def show_settings():
    st.header("⚙️ Settings")

    st.subheader("Study Preferences")

    # Daily study hours
    daily_hours = st.slider("Daily Study Hours", 1, 8, 4)

    # Focus areas
    focus_areas = st.multiselect(
        "Primary Focus Areas",
        ["DSA", "Machine Learning", "System Design", "Behavioral"],
        default=["DSA", "Machine Learning"],
    )

    # Notification preferences
    st.subheader("Notifications")
    enable_notifications = st.checkbox("Enable daily reminders", value=True)
    reminder_time = st.time_input("Reminder time", value=datetime.now().time())

    if st.button("Save Settings"):
        st.success("Settings saved!")


def send_chat_message(message: str, topic_category: str):
    """Send message to AI and update chat history"""

    try:
        # Map topic category to API format
        category_map = {
            "DSA": "dsa",
            "Machine Learning": "ml",
            "System Design": "system_design",
            "Behavioral": "behavioral",
            "General": None,
        }

        payload = {
            "message": message,
            "topic_category": category_map.get(topic_category),
        }

        response = requests.post(f"{API_BASE_URL}/chat", json=payload)

        if response.status_code == 200:
            result = response.json()

            # Add to chat history
            st.session_state.chat_history.append({"role": "user", "content": message})

            st.session_state.chat_history.append(
                {"role": "assistant", "content": result["response"]}
            )

        else:
            st.error("Failed to get AI response")

    except Exception as e:
        st.error(f"Error sending message: {str(e)}")


def log_progress(day: int, plan: dict):
    """Log daily progress"""

    try:
        payload = {
            "day": day,
            "topics": plan["topics"],
            "notes": f"Completed day {day} study plan",
            "hours_studied": plan["estimated_hours"],
            "problems_solved": len(plan["practice_problems"]),
            "confidence_level": 8,  # Default confidence
        }

        response = requests.post(f"{API_BASE_URL}/progress/daily", json=payload)

        if response.status_code == 200:
            st.session_state.current_day = day + 1
        else:
            st.error("Failed to log progress")

    except Exception as e:
        st.error(f"Error logging progress: {str(e)}")


if __name__ == "__main__":
    main()
