import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from config import PAGE_CONFIG, CUSTOM_CSS, LEARNING_CATEGORIES, COLORS, DEFAULT_STUDY_HOURS, DEFAULT_TARGET_DAYS
from auth_manager import AuthManager
from goals_manager import GoalsManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize managers
auth_manager = AuthManager()
goals_manager = GoalsManager()

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Learning Assistant</h1>
        <p>Personalized learning plans powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

def render_auth_forms():
    """Render authentication forms"""
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                if email and password:
                    result = auth_manager.login_user(email, password)
                    if result["success"]:
                        st.session_state.token = result["data"]["access_token"]
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(result["error"])
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.markdown("### Create New Account")
        with st.form("register_form"):
            full_name = st.text_input("Full Name", key="register_name")
            username = st.text_input("Username", key="register_username")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")
            submit_register = st.form_submit_button("Register")
            
            if submit_register:
                if all([full_name, username, email, password, confirm_password]):
                    if password == confirm_password:
                        result = auth_manager.register_user(email, username, full_name, password)
                        if result["success"]:
                            st.success("Registration successful! Please login.")
                        else:
                            st.error(result["error"])
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

def render_sidebar():
    """Render the sidebar with navigation"""
    st.sidebar.title("🎯 Navigation")
    
    if auth_manager.is_authenticated():
        user = st.session_state.get("user", {})
        st.sidebar.markdown(f"**Welcome, {user.get('full_name', 'User')}!**")
        
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["Dashboard", "My Goals", "Create Goal", "Daily Plans", "Progress Tracking", "AI Chat", "Analytics", "Settings"]
        )
        
        if st.sidebar.button("Logout"):
            auth_manager.logout()
        
        return page
    else:
        st.sidebar.markdown("Please login to access your learning dashboard.")
        return None

def render_dashboard():
    """Render the main dashboard"""
    st.header("📊 Your Learning Dashboard")
    
    # Get user analytics
    analytics_result = goals_manager.get_analytics()
    
    if analytics_result["success"]:
        analytics = analytics_result["data"]
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Goals", analytics["total_goals"])
        
        with col2:
            st.metric("Active Goals", analytics["active_goals"])
        
        with col3:
            st.metric("Study Hours", f"{analytics['total_study_hours']:.1f}")
        
        with col4:
            st.metric("Avg Confidence", f"{analytics['average_confidence']:.1f}%")
        
        # Display insights
        st.subheader("💡 AI Insights")
        for insight in analytics["insights"]:
            st.info(insight)
        
        # Display recent goals
        goals_result = goals_manager.get_user_goals()
        if goals_result["success"]:
            goals = goals_result["data"]
            if goals:
                st.subheader("🎯 Your Goals")
                for goal in goals[:3]:  # Show first 3 goals
                    with st.expander(f"{goal['title']} - {goal['category']}"):
                        st.write(f"**Description:** {goal['description']}")
                        st.write(f"**Progress:** Day {goal['current_day']} of {goal['target_days']}")
                        progress = (goal['current_day'] / goal['target_days']) * 100
                        st.progress(progress / 100)
    else:
        st.warning("Unable to load analytics. Please try again.")

def render_goals():
    """Render goals management page"""
    st.header("🎯 My Learning Goals")
    
    goals_result = goals_manager.get_user_goals()
    
    if goals_result["success"]:
        goals = goals_result["data"]
        
        if goals:
            for goal in goals:
                with st.container():
                    st.markdown(f"""
                    <div class="goal-card">
                        <h3>{goal['title']}</h3>
                        <p><strong>Category:</strong> {goal['category']}</p>
                        <p><strong>Description:</strong> {goal['description']}</p>
                        <p><strong>Progress:</strong> Day {goal['current_day']} of {goal['target_days']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"View Plan", key=f"plan_{goal['id']}"):
                            st.session_state.selected_goal = goal['id']
                            st.session_state.current_page = "Daily Plans"
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Track Progress", key=f"progress_{goal['id']}"):
                            st.session_state.selected_goal = goal['id']
                            st.session_state.current_page = "Progress Tracking"
                            st.rerun()
                    
                    with col3:
                        if st.button(f"Chat with AI", key=f"chat_{goal['id']}"):
                            st.session_state.selected_goal = goal['id']
                            st.session_state.current_page = "AI Chat"
                            st.rerun()
        else:
            st.info("You haven't created any goals yet. Create your first learning goal!")
    else:
        st.error("Unable to load goals. Please try again.")

def render_create_goal():
    """Render goal creation page"""
    st.header("🎯 Create New Learning Goal")
    
    with st.form("create_goal_form"):
        title = st.text_input("Goal Title", placeholder="e.g., Master Python Programming")
        description = st.text_area("Description", placeholder="Describe what you want to achieve...")
        
        category = st.selectbox(
            "Learning Category",
            options=list(LEARNING_CATEGORIES.keys()),
            format_func=lambda x: LEARNING_CATEGORIES[x]["name"]
        )
        
        target_days = st.slider("Target Days", min_value=7, max_value=90, value=DEFAULT_TARGET_DAYS)
        
        submit = st.form_submit_button("Create Goal")
        
        if submit:
            if title and description:
                result = goals_manager.create_goal(title, description, category, target_days)
                if result["success"]:
                    st.success("Goal created successfully!")
                    st.rerun()
                else:
                    st.error(result["error"])
            else:
                st.error("Please fill in all required fields")

def render_daily_plans():
    """Render daily plans page"""
    st.header("📅 Daily Learning Plans")
    
    goals_result = goals_manager.get_user_goals()
    
    if goals_result["success"]:
        goals = goals_result["data"]
        
        if goals:
            # Goal selection
            selected_goal_id = st.selectbox(
                "Select a goal:",
                options=[goal["id"] for goal in goals],
                format_func=lambda x: next(goal["title"] for goal in goals if goal["id"] == x)
            )
            
            # Day selection
            selected_day = st.slider("Select Day", min_value=1, max_value=30, value=1)
            
            if st.button("Generate Plan"):
                with st.spinner("Generating your personalized plan..."):
                    plan_result = goals_manager.get_daily_plan(selected_goal_id, selected_day)
                    
                    if plan_result["success"]:
                        plan = plan_result["data"]
                        
                        st.subheader(f"📋 Day {selected_day} Plan")
                        
                        # Topics
                        st.write("**Topics to Cover:**")
                        for topic in plan["topics"]:
                            st.write(f"• {topic}")
                        
                        # Learning Objectives
                        st.write("**Learning Objectives:**")
                        for topic, objectives in plan["learning_objectives"].items():
                            st.write(f"**{topic}:**")
                            for objective in objectives:
                                st.write(f"  • {objective}")
                        
                        # Practice Problems
                        st.write("**Practice Activities:**")
                        for problem in plan["practice_problems"]:
                            difficulty = problem.get("difficulty_level", "Medium")
                            description = problem.get("description", "Practice activity")
                            
                            if difficulty == "Easy":
                                st.write(f"🟢 {description}")
                            elif difficulty == "Medium":
                                st.write(f"🟡 {description}")
                            else:
                                st.write(f"🔴 {description}")
                        
                        # Resources
                        st.write("**Recommended Resources:**")
                        for resource in plan["resources"]:
                            st.write(f"• {resource}")
                        
                        # Summary
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Estimated Hours", f"{plan['estimated_hours']:.1f}")
                        with col2:
                            st.metric("Difficulty", plan["difficulty_level"])
                        with col3:
                            st.metric("Focus Areas", len(plan["focus_areas"]))
                    else:
                        st.error(plan_result["error"])
        else:
            st.info("Create a goal first to generate daily plans!")
    else:
        st.error("Unable to load goals. Please try again.")

def render_progress_tracking():
    """Render progress tracking page"""
    st.header("📊 Progress Tracking")
    
    goals_result = goals_manager.get_user_goals()
    
    if goals_result["success"]:
        goals = goals_result["data"]
        
        if goals:
            # Goal selection
            selected_goal_id = st.selectbox(
                "Select a goal to track:",
                options=[goal["id"] for goal in goals],
                format_func=lambda x: next(goal["title"] for goal in goals if goal["id"] == x)
            )
            
            # Progress logging form
            with st.form("progress_form"):
                st.subheader("Log Today's Progress")
                
                day = st.number_input("Day", min_value=1, value=1)
                topics_covered = st.multiselect(
                    "Topics Covered",
                    options=["Topic 1", "Topic 2", "Topic 3", "Topic 4"],
                    default=[]
                )
                hours_studied = st.slider("Hours Studied", min_value=0.5, max_value=8.0, value=2.0, step=0.5)
                problems_solved = st.number_input("Problems/Activities Completed", min_value=0, value=0)
                confidence_level = st.slider("Confidence Level", min_value=0, max_value=100, value=50)
                notes = st.text_area("Notes (optional)")
                
                submit_progress = st.form_submit_button("Log Progress")
                
                if submit_progress:
                    if topics_covered:
                        result = goals_manager.log_progress(
                            selected_goal_id, day, topics_covered, 
                            hours_studied, problems_solved, confidence_level, notes
                        )
                        
                        if result["success"]:
                            st.success("Progress logged successfully!")
                            st.info(f"AI Feedback: {result['data']['ai_feedback']}")
                        else:
                            st.error(result["error"])
                    else:
                        st.error("Please select at least one topic covered")
            
            # Show progress history
            st.subheader("Progress History")
            progress_result = goals_manager.get_goal_progress(selected_goal_id)
            
            if progress_result["success"]:
                progress_logs = progress_result["data"]
                
                if progress_logs:
                    # Create progress chart
                    days = [log["day"] for log in progress_logs]
                    hours = [log["hours_studied"] for log in progress_logs]
                    confidence = [log["confidence_level"] for log in progress_logs]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=days, y=hours, name="Study Hours", mode="lines+markers"))
                    fig.add_trace(go.Scatter(x=days, y=confidence, name="Confidence Level", mode="lines+markers", yaxis="y2"))
                    
                    fig.update_layout(
                        title="Progress Over Time",
                        xaxis_title="Day",
                        yaxis_title="Study Hours",
                        yaxis2=dict(title="Confidence Level", overlaying="y", side="right"),
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No progress logged yet. Start tracking your progress!")
        else:
            st.info("Create a goal first to track progress!")
    else:
        st.error("Unable to load goals. Please try again.")

def render_ai_chat():
    """Render AI chat page"""
    st.header("🤖 AI Learning Coach")
    
    goals_result = goals_manager.get_user_goals()
    
    if goals_result["success"]:
        goals = goals_result["data"]
        
        if goals:
            # Goal selection
            selected_goal_id = st.selectbox(
                "Select a goal for context:",
                options=[goal["id"] for goal in goals],
                format_func=lambda x: next(goal["title"] for goal in goals if goal["id"] == x)
            )
            
            # Chat interface
            st.markdown("""
            <div class="chat-container">
                <p>Ask your AI learning coach anything about your studies!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Chat input
            user_message = st.text_input("Your question:", key="chat_input")
            
            if st.button("Send Message"):
                if user_message:
                    with st.spinner("Getting AI response..."):
                        result = goals_manager.chat_with_ai(selected_goal_id, user_message)
                        
                        if result["success"]:
                            response = result["data"]
                            
                            st.markdown("### AI Response:")
                            st.write(response["response"])
                            
                            st.markdown("### Confidence Level:")
                            st.progress(response["confidence"] / 100)
                            
                            st.markdown("### Suggestions:")
                            for suggestion in response["suggestions"]:
                                st.write(f"• {suggestion}")
                        else:
                            st.error(result["error"])
                else:
                    st.error("Please enter a message")
        else:
            st.info("Create a goal first to chat with the AI coach!")
    else:
        st.error("Unable to load goals. Please try again.")

def render_analytics():
    """Render analytics page"""
    st.header("📈 Learning Analytics")
    
    analytics_result = goals_manager.get_analytics()
    
    if analytics_result["success"]:
        analytics = analytics_result["data"]
        
        # Key metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Goals", analytics["total_goals"])
            st.metric("Active Goals", analytics["active_goals"])
            st.metric("Total Study Hours", f"{analytics['total_study_hours']:.1f}")
        
        with col2:
            st.metric("Average Confidence", f"{analytics['average_confidence']:.1f}%")
            st.metric("Streak Days", analytics["streak_days"])
            st.metric("Completion Rate", f"{analytics['completion_rate']:.1f}%")
        
        # Insights
        st.subheader("💡 AI-Generated Insights")
        for insight in analytics["insights"]:
            st.info(insight)
        
        # Goals progress chart
        goals_result = goals_manager.get_user_goals()
        if goals_result["success"]:
            goals = goals_result["data"]
            
            if goals:
                goal_names = [goal["title"] for goal in goals]
                progress_values = [(goal["current_day"] / goal["target_days"]) * 100 for goal in goals]
                
                fig = px.bar(
                    x=goal_names,
                    y=progress_values,
                    title="Goal Progress",
                    labels={"x": "Goals", "y": "Progress (%)"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Unable to load analytics. Please try again.")

def render_settings():
    """Render settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("Account Information")
    user = st.session_state.get("user", {})
    
    if user:
        st.write(f"**Name:** {user.get('full_name', 'N/A')}")
        st.write(f"**Email:** {user.get('email', 'N/A')}")
        st.write(f"**Username:** {user.get('username', 'N/A')}")
    
    st.subheader("Preferences")
    st.write("Settings and preferences will be available here.")

def main():
    """Main application function"""
    render_header()
    
    # Check authentication
    if not auth_manager.is_authenticated():
        # Get user info if token exists
        token = auth_manager.get_token()
        if token:
            user_result = auth_manager.get_current_user(token)
            if user_result["success"]:
                st.session_state.user = user_result["data"]
            else:
                auth_manager.logout()
        
        # Show auth forms
        render_auth_forms()
        return
    
    # User is authenticated, show main app
    page = render_sidebar()
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "My Goals":
        render_goals()
    elif page == "Create Goal":
        render_create_goal()
    elif page == "Daily Plans":
        render_daily_plans()
    elif page == "Progress Tracking":
        render_progress_tracking()
    elif page == "AI Chat":
        render_ai_chat()
    elif page == "Analytics":
        render_analytics()
    elif page == "Settings":
        render_settings()

if __name__ == "__main__":
    main()
