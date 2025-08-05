import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from config import PAGE_CONFIG, CUSTOM_CSS, TOPIC_CATEGORIES, STUDY_PLAN_DAYS
from api_client import api_client
from session_state import SessionStateManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def render_header():
    """Render the main header"""
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Main header
    st.markdown(
        '<h1 class="main-header">🧠 AI Interview Assistant</h1>',
        unsafe_allow_html=True
    )

    # Subtitle
    st.markdown(
        "**Your AI-powered companion for FAANG interview preparation**",
        help="45-day structured study plan with daily guidance"
    )

def render_sidebar():
    """Render the sidebar with quick stats"""
    with st.sidebar:
        st.header("📊 Quick Stats")

        # Get status from API
        status = api_client.get_progress_status()

        if status:
            # Overall metrics
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
                st.metric("System Design", f"{status['system_design_progress']:.1f}%")
                st.metric("Behavioral", f"{status['behavioral_progress']:.1f}%")
        else:
            st.warning("Unable to fetch status")

def render_daily_plan():
    """Render the daily plan page with AI-generated content"""
    st.header("🎯 Today's Study Plan")

    # Day selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_day = SessionStateManager.get_current_day()
        selected_day = st.selectbox(
            "Select Day",
            range(1, STUDY_PLAN_DAYS + 1),
            index=current_day - 1
        )

    # Get daily plan from API
    plan = api_client.get_daily_plan(selected_day)

    if plan:
        # Display plan with enhanced UI
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"Day {selected_day} - {', '.join(plan['topics'])}")
            
            # Difficulty indicator
            difficulty = plan.get('difficulty_level', 'Medium')
            difficulty_color = {
                'Easy': '🟢',
                'Medium': '🟡', 
                'Hard': '🔴'
            }.get(difficulty, '🟡')
            st.write(f"**Difficulty:** {difficulty_color} {difficulty}")

            # Topics
            st.write("**Topics to Cover:**")
            for topic in plan["topics"]:
                st.write(f"• {topic}")

            # Learning objectives
            st.write("**Learning Objectives:**")
            for objective in plan["learning_objectives"]:
                st.write(f"• {objective}")

            # Practice problems with difficulty indicators
            st.write("**Practice Problems:**")
            for problem in plan["practice_problems"]:
                if "(Easy)" in problem:
                    st.write(f"🟢 {problem}")
                elif "(Medium)" in problem:
                    st.write(f"🟡 {problem}")
                elif "(Hard)" in problem:
                    st.write(f"🔴 {problem}")
                else:
                    st.write(f"• {problem}")

        with col2:
            st.metric("Estimated Hours", f"{plan['estimated_hours']}h")

            # Focus areas
            if 'focus_areas' in plan:
                st.write("**Focus Areas:**")
                for area in plan['focus_areas']:
                    st.write(f"🎯 {area}")

            # Resources
            st.write("**Resources:**")
            for resource in plan["resources"]:
                st.write(f"📚 {resource}")

            # Log progress button
            if st.button("✅ Mark Day Complete", type="primary"):
                result = api_client.log_progress(selected_day, plan)
                if result:
                    SessionStateManager.increment_current_day()
                    st.success(f"Day {selected_day} marked as complete!")
                    st.balloons()
                else:
                    st.error("Failed to log progress")
    else:
        st.error("Unable to fetch daily plan")

def render_ai_chat():
    """Render the AI chat page with enhanced features"""
    st.header("💬 AI Interview Coach")

    # Topic selection with descriptions
    col1, col2 = st.columns([1, 2])
    with col1:
        topic_descriptions = {
            "general": "General interview preparation",
            "dsa": "Data Structures & Algorithms",
            "ml": "Machine Learning & AI",
            "system_design": "System Design",
            "behavioral": "Behavioral Questions"
        }
        
        topic_category = st.selectbox(
            "Select Topic Category",
            TOPIC_CATEGORIES,
            help="Choose a specific topic for more targeted assistance",
            format_func=lambda x: f"{x.upper()} - {topic_descriptions.get(x, '')}"
        )

    # Chat interface with enhanced features
    chat_container = st.container()

    with chat_container:
        # Display chat history with better formatting
        chat_history = SessionStateManager.get_chat_history()
        
        if chat_history:
            st.subheader("💬 Chat History")
            for i, message in enumerate(chat_history):
                if message["role"] == "user":
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI Coach:** {message['content']}")
                st.divider()

        # Chat input with suggestions
        st.subheader("Ask Your Question")
        
        # Quick suggestions based on topic
        suggestions = {
            "dsa": [
                "How do I approach dynamic programming problems?",
                "What's the best way to practice binary search?",
                "How do I analyze time complexity?"
            ],
            "ml": [
                "How do I choose between different ML algorithms?",
                "What's the bias-variance tradeoff?",
                "How do I handle overfitting?"
            ],
            "system_design": [
                "How do I design a scalable system?",
                "What's the CAP theorem?",
                "How do I choose between SQL and NoSQL?"
            ],
            "behavioral": [
                "How do I answer 'Tell me about yourself'?",
                "How do I handle conflict resolution questions?",
                "How do I prepare STAR method answers?"
            ],
            "general": [
                "How do I prepare for technical interviews?",
                "What should I focus on for FAANG interviews?",
                "How do I manage interview anxiety?"
            ]
        }
        
        topic_suggestions = suggestions.get(topic_category, [])
        if topic_suggestions:
            st.write("💡 **Quick Suggestions:**")
            for suggestion in topic_suggestions:
                if st.button(suggestion, key=f"suggestion_{suggestion[:20]}"):
                    user_input = suggestion
                    break
            else:
                user_input = st.text_area("Ask your question:", height=100)
        else:
            user_input = st.text_area("Ask your question:", height=100)

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Send", type="primary"):
                if user_input.strip():
                    send_chat_message(user_input, topic_category)
                    st.rerun()
        with col2:
            if st.button("Clear Chat"):
                SessionStateManager.clear_chat_history()
                st.rerun()

def send_chat_message(message: str, topic_category: str):
    """Send message to AI and get response"""
    # Add user message to history
    SessionStateManager.add_chat_message("user", message)

    # Show loading spinner
    with st.spinner("AI Coach is thinking..."):
        # Get AI response
        result = api_client.send_chat_message(message, topic_category)

        if result:
            # Add AI response to history
            SessionStateManager.add_chat_message("assistant", result["response"])
        else:
            st.error("Failed to get AI response")

def render_analytics():
    """Render the analytics page with enhanced visualizations"""
    st.header("📈 Progress Analytics")

    # Get analytics from API
    analytics = api_client.get_analytics()

    if analytics:
        # Enhanced metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Hours Studied", f"{analytics['total_study_hours']:.1f}h"
            )
        with col2:
            st.metric("Problems Solved", analytics["problems_solved"])
        with col3:
            st.metric("Topics Completed", analytics["topics_completed"])
        with col4:
            st.metric("Confidence Level", f"{analytics['confidence_level']}%")

        # Progress chart with enhanced styling
        st.subheader("📊 Study Progress by Category")

        # Create a more detailed progress chart
        progress_data = {
            "Category": ["DSA", "ML", "System Design", "Behavioral"],
            "Progress": [75, 60, 45, 80],
            "Target": [100, 100, 100, 100]
        }

        fig = go.Figure()

        # Add progress bars
        fig.add_trace(go.Bar(
            name='Current Progress',
            x=progress_data["Category"],
            y=progress_data["Progress"],
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        ))

        fig.add_trace(go.Bar(
            name='Target',
            x=progress_data["Category"],
            y=progress_data["Target"],
            marker_color='rgba(0,0,0,0.1)',
            showlegend=False
        ))

        fig.update_layout(
            title="Progress by Category",
            barmode='overlay',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Additional metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Days Remaining", analytics["days_remaining"])
        with col2:
            st.metric("Streak Days", analytics["streak_days"])

        # Study streak visualization
        st.subheader("🔥 Study Streak")
        streak_days = analytics["streak_days"]
        if streak_days > 0:
            st.write(f"You're on a {streak_days}-day study streak! Keep it up! 🔥")
            
            # Create streak visualization
            streak_fig = go.Figure()
            streak_fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=streak_days,
                title={'text': "Current Streak"},
                gauge={'axis': {'range': [None, 30]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 7], 'color': "lightgray"},
                           {'range': [7, 14], 'color': "yellow"},
                           {'range': [14, 21], 'color': "orange"},
                           {'range': [21, 30], 'color': "red"}
                       ],
                       'threshold': {
                           'line': {'color': "red", 'width': 4},
                           'thickness': 0.75,
                           'value': 21
                       }}))
            st.plotly_chart(streak_fig, use_container_width=True)
        else:
            st.write("Start your study streak today! 📚")

        # Completion rate
        completion_rate = analytics.get("completion_rate", 0)
        st.subheader("📋 Overall Completion")
        st.progress(completion_rate / 100)
        st.write(f"**{completion_rate:.1f}%** of the 45-day plan completed")

    else:
        st.warning("No progress data available yet. Start studying to see analytics!")

def render_calendar():
    """Render the calendar page with enhanced features"""
    st.header("📅 Study Calendar")

    st.write("**45-Day Study Plan Overview**")

    # Create an enhanced calendar view
    st.subheader("📅 45-Day Study Plan")

    # Create a calendar grid with better styling
    days = list(range(1, STUDY_PLAN_DAYS + 1))
    cols = st.columns(7)

    current_day = SessionStateManager.get_current_day()

    for i, day in enumerate(days):
        col_idx = i % 7
        with cols[col_idx]:
            if day == current_day:
                st.markdown(f"**{day}** 🎯")
            elif day < current_day:
                st.markdown(f"~~{day}~~ ✅")
            else:
                st.markdown(f"{day}")

    st.write("**Legend:**")
    st.write("• 🎯 = Current Day")
    st.write("• ✅ = Completed")
    st.write("• Number = Future Day")

    # Progress summary with enhanced metrics
    st.subheader("📊 Progress Summary")

    completed_days = current_day - 1
    remaining_days = STUDY_PLAN_DAYS - current_day + 1
    progress_percentage = (completed_days / STUDY_PLAN_DAYS) * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completed Days", completed_days)
    with col2:
        st.metric("Remaining Days", remaining_days)
    with col3:
        st.metric("Overall Progress", f"{progress_percentage:.1f}%")

    # Enhanced progress bar
    st.progress(progress_percentage / 100)

    # Study timeline visualization
    st.subheader("📈 Study Timeline")
    
    # Create a timeline chart
    timeline_data = {
        "Week": [f"Week {i+1}" for i in range(7)],
        "Days": [7, 7, 7, 7, 7, 7, 3],
        "Completed": [min(completed_days, 7), max(0, min(completed_days-7, 7)), 
                     max(0, min(completed_days-14, 7)), max(0, min(completed_days-21, 7)),
                     max(0, min(completed_days-28, 7)), max(0, min(completed_days-35, 7)),
                     max(0, min(completed_days-42, 3))]
    }

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Completed Days',
        x=timeline_data["Week"],
        y=timeline_data["Completed"],
        marker_color='#1f77b4'
    ))
    fig.add_trace(go.Bar(
        name='Remaining Days',
        x=timeline_data["Week"],
        y=[max(0, total - completed) for total, completed in zip(timeline_data["Days"], timeline_data["Completed"])],
        marker_color='lightgray'
    ))

    fig.update_layout(
        title="Weekly Progress",
        barmode='stack',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def render_settings():
    """Render the settings page with enhanced features"""
    st.header("⚙️ Settings")

    # Backend configuration
    st.subheader("🔧 Backend Configuration")
    from config import API_BASE_URL
    st.write(f"**Backend URL:** {API_BASE_URL}")

    # Test connection
    if st.button("🔗 Test Connection"):
        health = api_client.get_health()
        if health:
            st.success("✅ Backend connection successful!")
        else:
            st.error("❌ Backend connection failed!")

    # Study preferences
    st.subheader("📚 Study Preferences")

    preferences = SessionStateManager.get_user_preferences()

    study_hours = st.slider(
        "Daily Study Hours",
        1, 8,
        preferences.get("study_hours", 4)
    )

    difficulty = st.selectbox(
        "Preferred Difficulty",
        ["Easy", "Medium", "Hard"],
        index=["Easy", "Medium", "Hard"].index(preferences.get("difficulty", "Medium"))
    )

    notifications = st.checkbox(
        "Enable Notifications",
        value=preferences.get("notifications", True)
    )

    # AI preferences
    st.subheader("🤖 AI Preferences")
    
    ai_style = st.selectbox(
        "AI Coach Style",
        ["Encouraging", "Direct", "Detailed", "Concise"],
        index=["Encouraging", "Direct", "Detailed", "Concise"].index(preferences.get("ai_style", "Encouraging"))
    )

    # Save settings
    if st.button("💾 Save Settings"):
        new_preferences = {
            "study_hours": study_hours,
            "difficulty": difficulty,
            "notifications": notifications,
            "ai_style": ai_style
        }
        SessionStateManager.update_user_preferences(new_preferences)
        st.success("Settings saved successfully!")

    # Display current settings
    st.subheader("📋 Current Settings")
    st.json(preferences)

    # Reset options
    st.subheader("🔄 Reset Options")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear Chat History"):
            SessionStateManager.clear_chat_history()
            st.success("Chat history cleared!")

    with col2:
        if st.button("🔄 Reset Progress"):
            SessionStateManager.set_current_day(1)
            st.success("Progress reset to day 1!")

def main():
    """Main application entry point"""
    # Configure page
    st.set_page_config(**PAGE_CONFIG)

    # Initialize session state
    SessionStateManager.initialize()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar()

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Daily Plan",
        "💬 AI Chat",
        "📈 Progress Analytics",
        "📅 Study Calendar",
        "⚙️ Settings"
    ])

    # Render tab content
    with tab1:
        render_daily_plan()

    with tab2:
        render_ai_chat()

    with tab3:
        render_analytics()

    with tab4:
        render_calendar()

    with tab5:
        render_settings()

if __name__ == "__main__":
    main()
