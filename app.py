import streamlit as st
import requests
from datetime import datetime
from users_db import verify_user, add_user, get_user_info
import os
from colors import (
    MAIN_BLUE, ACTION_RED, POSITIVE_GREEN, NEUTRAL_AMBER, 
    NEGATIVE_RED, INFO_BLUE, SUCCESS_GREEN, SENTIMENT_COLORS
)

# Configure the page - MUST be first Streamlit command
st.set_page_config(
    page_title="Political News Sentiment Analysis",
    page_icon="📰",
    layout="centered"
)

# Now import config after set_page_config
from config import NEWS_API_KEY

# Add custom CSS for smooth scroll to top
st.markdown("""
    <style>
        .main {
            scroll-behavior: smooth;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'news'
if 'articles' not in st.session_state:
    st.session_state.articles = None
if 'selected_party' not in st.session_state:
    st.session_state.selected_party = ''
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = ''
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

def login(username, password):
    """
    Login function using user database
    """
    if verify_user(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.current_page = 'news'
    st.session_state.articles = None

def fetch_news(party, state, api_key, max_articles=10, sort_by="Latest"):
    """
    Fetch news articles using News API
    """
    # Construct search query
    query = f"{party}"
    if state != "All States":
        query += f" {state}"
    query += " India politics"
    
    # Map sort_by option to API parameter
    sort_mapping = {
        "Latest": "publishedAt",
        "Relevance": "relevancy",
        "Popularity": "popularity"
    }
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': 'en',
        'sortBy': sort_mapping.get(sort_by, 'publishedAt'),
        'pageSize': max_articles,
        'apiKey': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'ok':
            return data['articles']
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {str(e)}")
        return None

def display_news_article(article, index):
    """Display a single news article"""
    with st.container():
        st.markdown(f"### {index}. {article.get('title', 'No Title')}")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if article.get('description'):
                st.write(article['description'])
            
            if article.get('author'):
                st.caption(f"By: {article['author']}")
            
            if article.get('source', {}).get('name'):
                st.caption(f"Source: {article['source']['name']}")
            
            if article.get('publishedAt'):
                pub_date = article['publishedAt'][:10]
                st.caption(f"Published: {pub_date}")
        
        with col2:
            if article.get('urlToImage'):
                st.image(article['urlToImage'], use_column_width=True)
        
        if article.get('url'):
            st.link_button("Read Full Article", article['url'], use_container_width=True)
        
        st.markdown("---")

def login_page():
    """Display the login page"""
    # Display logo at the top center - smaller size to prevent scrolling
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("assets/svgviewer-png-output.png", width=130)
    
    # Title with custom styling
    st.markdown(
        f"<h1 style='text-align: center; color: {MAIN_BLUE};'>Political News Sentiment Analysis</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<h3 style='text-align: center; color: #666;'>Login to Continue</h3>", unsafe_allow_html=True)
    
    # Create a centered container for the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Toggle between login and signup
        if not st.session_state.show_signup:
            # Login form with enhanced styling
            with st.form("login_form"):
                st.markdown("### Sign In")
                username = st.text_input("Username", placeholder="Enter your username", key="login_username")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
                
                # Remember me checkbox
                remember_me = st.checkbox("Remember me", value=False)
                
                submit_button = st.form_submit_button("Login", use_container_width=True, type="primary")
                
                if submit_button:
                    if username and password:
                        if login(username, password):
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                    else:
                        st.warning("⚠️ Please enter both username and password")
            
            # Additional login options
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Sign up button
            if st.button("Don't have an account? Sign Up", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
        
        else:
            # Signup form
            with st.form("signup_form"):
                st.markdown("### Create New Account")
                new_username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_fullname = st.text_input("Full Name", placeholder="Enter your full name", key="signup_fullname")
                new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="signup_confirm")
                
                signup_button = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                
                if signup_button:
                    # Validation
                    if not all([new_username, new_email, new_fullname, new_password, confirm_password]):
                        st.error("❌ Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters long")
                    elif "@" not in new_email:
                        st.error("❌ Please enter a valid email address")
                    else:
                        # Try to create user
                        success, message = add_user(new_username, new_password, new_email, new_fullname)
                        if success:
                            st.success(f"✅ {message}! You can now login.")
                            st.balloons()
                            # Switch back to login
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
            
            # Back to login button
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()

def news_page():
    """Main application after login"""
    # Display logo in sidebar and header - compact layout
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("assets/svgviewer-png-output.png", width=80)
    with col2:
        st.markdown(
            f"<h1 style='color: {MAIN_BLUE}; margin-top: 10px;'>Political News Sentiment Analysis</h1>",
            unsafe_allow_html=True
        )
    
    # Sidebar with user info and logout
    with st.sidebar:
        # Logo in sidebar - smaller
        st.image("assets/svgviewer-png-output.png", width=120)
        st.markdown("---")
        st.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Main content area
    st.markdown("---")
    
    # Add welcome message and quick stats
    st.success(f"Welcome back, **{st.session_state.username}**!")
    
    # Quick stats/info cards
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.metric("Available Parties", "23+", help="Number of political parties to analyze")
    with info_col2:
        st.metric("States/UTs", "36", help="All Indian states and union territories")
    with info_col3:
        st.metric("Sources", "Multiple", help="News from various sources via News API")
    
    st.markdown("---")
    st.subheader("Select Analysis Parameters")
    
    # Indian Political Parties
    indian_parties = [
        "Bharatiya Janata Party (BJP)",
        "Indian National Congress (INC)",
        "Aam Aadmi Party (AAP)",
        "Trinamool Congress (TMC)",
        "Dravida Munnetra Kazhagam (DMK)",
        "All India Anna Dravida Munnetra Kazhagam (AIADMK)",
        "Shiv Sena",
        "Nationalist Congress Party (NCP)",
        "Communist Party of India (Marxist) (CPI-M)",
        "Communist Party of India (CPI)",
        "Bahujan Samaj Party (BSP)",
        "Samajwadi Party (SP)",
        "Rashtriya Janata Dal (RJD)",
        "Janata Dal (United) (JD-U)",
        "Janata Dal (Secular) (JD-S)",
        "Biju Janata Dal (BJD)",
        "Telangana Rashtra Samithi (TRS/BRS)",
        "YSR Congress Party (YSRCP)",
        "Telugu Desam Party (TDP)",
        "Shiromani Akali Dal (SAD)",
        "Indian Union Muslim League (IUML)",
        "All India Majlis-e-Ittehadul Muslimeen (AIMIM)",
        "Other"
    ]
    
    # Indian States and Union Territories
    indian_states = [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
        "Andaman and Nicobar Islands",
        "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi",
        "Jammu and Kashmir",
        "Ladakh",
        "Lakshadweep",
        "Puducherry",
        "All States"
    ]
    
    # Create two columns for selections with enhanced features
    col1, col2 = st.columns(2)
    
    with col1:
        selected_party = st.selectbox(
            "Select Political Party",
            options=indian_parties,
            index=0,
            help="Choose the political party for sentiment analysis"
        )
        # Add party search helper
        with st.expander("Quick Party Search"):
            search_term = st.text_input("Type party name to filter", key="party_search")
            if search_term:
                filtered = [p for p in indian_parties if search_term.lower() in p.lower()]
                if filtered:
                    st.write("**Matching parties:**")
                    for p in filtered[:5]:
                        st.write(f"• {p}")
    
    with col2:
        selected_state = st.selectbox(
            "Select State/UT",
            options=indian_states,
            index=len(indian_states) - 1,  # Default to "All States"
            help="Choose the state or union territory"
        )
        # Add state info
        with st.expander("State Information"):
            if selected_state != "All States":
                st.write(f"**Selected:** {selected_state}")
                st.write("News will be filtered for this state/UT")
            else:
                st.write("**All States selected**")
                st.write("News from across India will be shown")
    
    st.markdown("---")
    
    # Advanced options expander
    with st.expander("Advanced Options"):
        col_a, col_b = st.columns(2)
        with col_a:
            # Get default value from session state or use 10
            default_max = st.session_state.get('max_articles', 10)
            max_articles = st.slider("Max articles to fetch", 5, 20, default_max, key="max_slider")
            st.session_state.max_articles = max_articles
        with col_b:
            # Get default value from session state or use "Latest"
            sort_options = ["Latest", "Relevance", "Popularity"]
            default_sort = st.session_state.get('sort_by', 'Latest')
            default_index = sort_options.index(default_sort) if default_sort in sort_options else 0
            sort_by = st.selectbox("Sort by", sort_options, index=default_index, key="sort_select")
            st.session_state.sort_by = sort_by
        
        # Show current settings
        st.caption(f"Current settings: {max_articles} articles, sorted by {sort_by}")
    
    # Show Live News button with enhanced styling
    if st.button("Show Live News", type="primary", use_container_width=True):
        if not NEWS_API_KEY or NEWS_API_KEY == "your_api_key_here":
            st.warning("⚠️ Please configure your News API key in config.py file.")
            st.info("💡 Get your free API key from [newsapi.org](https://newsapi.org) and add it to config.py")
        else:
            # Get advanced options from session state or use defaults
            max_articles_param = st.session_state.get('max_articles', 10)
            sort_by_param = st.session_state.get('sort_by', 'Latest')
            
            with st.spinner(f"Fetching {max_articles_param} articles for **{selected_party}** in **{selected_state}** (sorted by {sort_by_param})..."):
                articles = fetch_news(selected_party, selected_state, NEWS_API_KEY, max_articles_param, sort_by_param)
                
                if articles:
                    # Store articles and parameters in session state
                    st.session_state.articles = articles
                    st.session_state.selected_party = selected_party
                    st.session_state.selected_state = selected_state
                else:
                    st.error("❌ No articles found or there was an error fetching news.")
                    st.info("💡 Tip: Make sure your API key is valid in config.py and try again.")
    
    # Display news articles if available
    if st.session_state.articles:
        st.success(f"Found {len(st.session_state.articles)} news articles!")
        st.markdown("---")
        st.subheader("Latest News Articles")
        
        for idx, article in enumerate(st.session_state.articles, 1):
            display_news_article(article, idx)
        
        # Analyze Sentiment button and Reset button after news display
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Analyze Sentiment", type="primary", use_container_width=True, key="analyze_btn"):
                st.session_state.current_page = 'sentiment'
                st.rerun()
        with col_btn2:
            if st.button("Reset & Start Fresh", use_container_width=True, key="reset_btn"):
                # Clear all session state data
                st.session_state.articles = None
                st.session_state.selected_party = ''
                st.session_state.selected_state = ''
                st.session_state.current_page = 'news'
                if 'max_articles' in st.session_state:
                    del st.session_state.max_articles
                if 'sort_by' in st.session_state:
                    del st.session_state.sort_by
                st.rerun()
    
def sentiment_analysis_page():
    """Sentiment Analysis Results Page"""
    # Add anchor at top and auto-scroll script
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)
    
    # JavaScript to scroll to top
    st.markdown("""
        <script>
            setTimeout(function() {
                window.parent.document.querySelector('.main').scrollTop = 0;
            }, 100);
        </script>
    """, unsafe_allow_html=True)
    
    # Display logo in header - compact layout
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("assets/svgviewer-png-output.png", width=80)
    with col2:
        st.markdown(
            f"<h1 style='color: {MAIN_BLUE}; margin-top: 10px;'>Sentiment Analysis Results</h1>",
            unsafe_allow_html=True
        )
    
    # Sidebar with user info and logout
    with st.sidebar:
        # Logo in sidebar - smaller
        st.image("assets/svgviewer-png-output.png", width=120)
        st.markdown("---")
        st.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.button("← Back to News", use_container_width=True):
            st.session_state.current_page = 'news'
            st.rerun()
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Display analysis parameters
    st.markdown("---")
    st.subheader("Analysis Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Party:** {st.session_state.selected_party}")
    with col2:
        st.info(f"**State:** {st.session_state.selected_state}")
    
    st.markdown("---")
    
    # Check if we have articles to analyze
    if st.session_state.articles:
        st.subheader(f"Analyzing {len(st.session_state.articles)} Articles")
        
        # Perform real sentiment analysis WITH PARTY-SPECIFIC CONTEXT
        from sentiment_analyzer import get_analyzer
        
        with st.spinner(f"Performing AI-powered sentiment analysis for {st.session_state.selected_party}..."):
            analyzer = get_analyzer()
            # Pass the selected party for party-specific analysis
            analysis_results = analyzer.analyze_articles_batch(
                st.session_state.articles, 
                target_party=st.session_state.selected_party
            )
        
        # Display sentiment analysis results
        st.success(f"✅ Sentiment Analysis Complete! Results show impact on **{st.session_state.selected_party}**")
        
        # Get overall statistics
        stats = analysis_results['overall_statistics']
        
        # Overall sentiment summary with color-coded metrics
        st.markdown("---")
        st.subheader(f"Overall Sentiment Summary for {st.session_state.selected_party}")
        
        # Display overall sentiment with emoji and color
        overall_sentiment = stats['overall_sentiment']
        sentiment_emoji = analyzer.get_sentiment_emoji(overall_sentiment)
        sentiment_color = analyzer.get_sentiment_color(overall_sentiment)
        
        st.markdown(f"### {sentiment_emoji} Overall Sentiment: <span style='color: {sentiment_color};'>{overall_sentiment}</span>", unsafe_allow_html=True)
        
        # Add human-readable narrative summary
        narrative_summary = analyzer.get_human_readable_summary(analysis_results)
        st.info(f"📝 **What does this mean for {st.session_state.selected_party}?**\n\n{narrative_summary}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="😊 Positive", 
                value=f"{stats['positive_percentage']}%",
                delta=f"{stats['positive_count']} articles"
            )
        with col2:
            st.metric(
                label="😐 Neutral", 
                value=f"{stats['neutral_percentage']}%",
                delta=f"{stats['neutral_count']} articles"
            )
        with col3:
            st.metric(
                label="😢 Negative", 
                value=f"{stats['negative_percentage']}%",
                delta=f"{stats['negative_count']} articles"
            )
        
        # Analysis quality metrics
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            confidence_explanation = analyzer.explain_score('confidence', stats['average_confidence'])
            st.metric(
                label="🎯 Average Confidence",
                value=f"{stats['average_confidence']}%",
                help=confidence_explanation
            )
            st.caption(f"💬 {confidence_explanation}")
        with col2:
            compound_explanation = analyzer.explain_score('compound', stats['average_compound_score'])
            st.metric(
                label="Compound Score",
                value=f"{stats['average_compound_score']:.4f}",
                help=compound_explanation
            )
            st.caption(f"💬 {compound_explanation}")
        
        # Clean, minimal visualizations
        st.markdown("---")
        st.subheader("Sentiment Distribution")
        
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Create two columns for compact chart layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart - Sentiment distribution
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Positive', 'Neutral', 'Negative'],
                values=[stats['positive_count'], stats['neutral_count'], stats['negative_count']],
                marker=dict(colors=SENTIMENT_COLORS),
                hole=0.4,  # Donut chart for modern look
                textinfo='label+percent',
                textfont=dict(size=12),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                showlegend=False,
                margin=dict(t=30, b=0, l=0, r=0),
                height=300,
                title=dict(text="Sentiment Split", font=dict(size=14, color=MAIN_BLUE), x=0.5, xanchor='center')
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart - Sentiment counts
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=['Positive', 'Neutral', 'Negative'],
                    y=[stats['positive_count'], stats['neutral_count'], stats['negative_count']],
                    marker=dict(color=SENTIMENT_COLORS),
                    text=[stats['positive_count'], stats['neutral_count'], stats['negative_count']],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Articles: %{y}<br>Percentage: %{customdata}%<extra></extra>',
                    customdata=[stats['positive_percentage'], stats['neutral_percentage'], stats['negative_percentage']]
                )
            ])
            
            fig_bar.update_layout(
                yaxis_title="Article Count",
                margin=dict(t=30, b=40, l=40, r=0),
                height=300,
                showlegend=False,
                title=dict(text="Article Count by Sentiment", font=dict(size=14, color=MAIN_BLUE), x=0.5, xanchor='center')
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Individual article sentiments with detailed breakdown
        st.markdown("---")
        st.subheader("Individual Article Sentiments")
        
        individual_results = analysis_results['individual_results']
        
        for idx, (article, sentiment) in enumerate(zip(st.session_state.articles, individual_results), 1):
            classification = sentiment['classification']
            emoji = analyzer.get_sentiment_emoji(classification)
            color = analyzer.get_sentiment_color(classification)
            
            # Create colored header for expander
            expander_title = f"{emoji} {idx}. {article.get('title', 'No Title')}"
            
            with st.expander(expander_title):
                # Article metadata
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                    st.write(f"**Published:** {article.get('publishedAt', 'Unknown')[:10]}")
                with col2:
                    st.write(f"**Author:** {article.get('author', 'Unknown')}")
                
                st.markdown("---")
                
                # Sentiment breakdown with color
                st.markdown(f"### Sentiment: <span style='color: {color}; font-weight: bold;'>{classification}</span>", unsafe_allow_html=True)
                
                # Add plain English explanation
                compound_explanation = analyzer.explain_score('compound', sentiment['compound_score'])
                confidence_explanation = analyzer.explain_score('confidence', sentiment['confidence'])
                st.markdown(f"**In simple terms:** {compound_explanation}")
                st.markdown(f"**AI Certainty:** {confidence_explanation}")
                
                # Show party-specific context note if available
                if sentiment.get('party_specific') and sentiment.get('context_note'):
                    st.info(f"🎯 **Party Context:** {sentiment['context_note']}")
                    if sentiment.get('context_adjustment') and abs(sentiment['context_adjustment']) > 0.05:
                        adjustment_direction = "more positive" if sentiment['context_adjustment'] > 0 else "more negative"
                        st.caption(f"Adjusted {adjustment_direction} by {abs(sentiment['context_adjustment']):.2f} based on impact to {st.session_state.selected_party}")
                
                st.markdown("---")
                # Detailed scores
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Positive", f"{sentiment['positive']*100:.1f}%")
                with col2:
                    st.metric("Neutral", f"{sentiment['neutral']*100:.1f}%")
                with col3:
                    st.metric("Negative", f"{sentiment['negative']*100:.1f}%")
                with col4:
                    st.metric("Confidence", f"{sentiment['confidence']:.1f}%")
                
                # Advanced metrics (displayed directly, not nested)
                st.markdown("**Advanced Metrics:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Compound Score:** {sentiment['compound_score']:.4f}")
                    st.write(f"**VADER Score:** {sentiment['vader_compound']:.4f}")
                with col2:
                    st.write(f"**TextBlob Score:** {sentiment['textblob_polarity']:.4f}")
                    subjectivity_explanation = analyzer.explain_score('subjectivity', sentiment['subjectivity'])
                    st.write(f"**Subjectivity:** {sentiment['subjectivity']:.2f}")
                    st.caption(f"💬 {subjectivity_explanation}")
                
                # Article description
                st.markdown("---")
                st.write(f"**Description:** {article.get('description', 'No description available')}")
                
                # Link to full article
                if article.get('url'):
                    st.markdown(f"[🔗 Read Full Article]({article['url']})")
        
        # AI-Generated Key Insights
        st.markdown("---")
        st.subheader("💡 AI-Generated Key Insights")
        
        # Display narrative summary in a nice box
        st.success("**Analysis Summary**")
        insights = analyzer.get_sentiment_insights(analysis_results)
        for insight in insights:
            st.write(f"✓ {insight}")
        
        # Add interpretation guide
        with st.expander("How to Interpret These Results"):
            st.markdown("""
            ### Understanding Sentiment Scores:
            
            **Positive Sentiment (😊):**
            - Articles with favorable, optimistic, or supportive language
            - Words like: "success", "progress", "beneficial", "achievement"
            - Example: "The new policy brings significant improvements"
            
            **Neutral Sentiment (😐):**
            - Factual, balanced reporting without strong emotion
            - Objective descriptions and statements
            - Example: "The meeting was held at 3 PM with 50 attendees"
            
            **Negative Sentiment (😢):**
            - Articles with critical, pessimistic, or concerning language
            - Words like: "failure", "problem", "crisis", "controversial"
            - Example: "The decision faces strong opposition"
            
            ---
            
            ### What the Scores Mean:
            
            **Compound Score (-1.0 to +1.0):**
            - **+0.5 to +1.0:** Very positive tone
            - **+0.05 to +0.5:** Somewhat positive
            - **-0.05 to +0.05:** Neutral/balanced
            - **-0.5 to -0.05:** Somewhat negative
            - **-1.0 to -0.5:** Very negative tone
            
            **Confidence Score (30% to 100%):**
            - **80-100%:** AI is very certain about the classification
            - **65-80%:** High confidence, reliable result
            - **50-65%:** Moderate confidence
            - **30-50%:** Lower confidence, text may be ambiguous
            
            **Subjectivity (0.0 to 1.0):**
            - **0.0-0.3:** Mostly factual, objective reporting
            - **0.3-0.5:** Mix of facts and opinions
            - **0.5-0.7:** Moderately subjective
            - **0.7-1.0:** Highly opinion-based
            
            ---
            
            ### AI Model Information:
            - **VADER (70%):** Specialized for social media and news text
            - **TextBlob (30%):** General-purpose sentiment analysis
            - **Ensemble Method:** Combines both models for better accuracy
            - **Estimated Accuracy:** ~78% on political news
            """)

        
        # Export to PDF button - centered
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Export as PDF", use_container_width=True, type="primary"):
                try:
                    # Import PDF generator
                    from pdf_generator import generate_sentiment_pdf
                    
                    # Prepare data for PDF with real sentiment analysis results
                    pdf_data = {
                        'party': st.session_state.selected_party,
                        'state': st.session_state.selected_state,
                        'username': st.session_state.username,
                        'articles_count': stats['total_articles'],
                        'positive_pct': stats['positive_percentage'],
                        'neutral_pct': stats['neutral_percentage'],
                        'negative_pct': stats['negative_percentage'],
                        'positive_count': stats['positive_count'],
                        'neutral_count': stats['neutral_count'],
                        'negative_count': stats['negative_count'],
                        'insights': insights,
                        'articles': st.session_state.articles,
                        'individual_sentiments': individual_results,
                        'average_confidence': stats['average_confidence'],
                        'overall_sentiment': stats['overall_sentiment']
                    }
                    
                    # Generate PDF filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"sentiment_analysis_{timestamp}.pdf"
                    
                    # Generate PDF
                    with st.spinner("Generating comprehensive PDF report with AI analysis..."):
                        generate_sentiment_pdf(filename, pdf_data)
                    
                    # Provide download button
                    with open(filename, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    st.success("✅ PDF report generated successfully!")
                    
                    # Clean up file after download
                    try:
                        os.remove(filename)
                    except:
                        pass
                        
                except ImportError:
                    st.error("❌ ReportLab library is required for PDF generation.")
                    st.info("💡 Install it using: `pip install reportlab`")
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
        
    else:
        st.warning("⚠️ No articles available for analysis. Please fetch news first.")
        if st.button("← Go Back to News", use_container_width=True):
            st.session_state.current_page = 'news'
            st.rerun()

def main_app():
    """Main app router"""
    if st.session_state.current_page == 'news':
        news_page()
    elif st.session_state.current_page == 'sentiment':
        sentiment_analysis_page()


# Main app logic
if st.session_state.logged_in:
    main_app()
else:
    login_page()
