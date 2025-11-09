# News API Configuration
# Get your free API key from https://newsapi.org

import os

# Try to get API key from Streamlit secrets (for cloud deployment)
# Otherwise use the hardcoded value (for local development)
try:
    # Only import streamlit if needed
    import streamlit as st
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except (ImportError, FileNotFoundError, KeyError):
    # Fallback to environment variable or empty string
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_api_key_here")
