"""
Color Palette Configuration for Political News Sentiment Analysis
Professional, modern color scheme optimized for dark theme dashboards
"""

# ========================================
# PRIMARY COLORS (Brand + Headings)
# ========================================
MAIN_BLUE = "#1E6FB8"           # Main headings and titles
DARK_NAVY = "#0E1117"           # Base theme background
ACTION_RED = "#FF4D4F"          # Primary action buttons (Login/Analyze/Export)
INACTIVE_GRAY = "#2A2D33"       # Inactive/hover states

# ========================================
# SENTIMENT COLORS (Charts + Metrics)
# ========================================
POSITIVE_GREEN = "#2ECC71"      # Emerald Green - Positive sentiment
NEUTRAL_AMBER = "#F1C40F"       # Soft Amber - Neutral sentiment
NEGATIVE_RED = "#E74C3C"        # Carmine Red - Negative sentiment

# ========================================
# SUPPORTING UI COLORS (Cards + Alerts)
# ========================================
INFO_BLUE = "#2F80ED"           # Information cards and messages
SUCCESS_GREEN = "#27AE60"       # Success messages
WARNING_YELLOW = "#F2C94C"      # Warning messages

# ========================================
# CHART COLOR ARRAYS
# ========================================
SENTIMENT_COLORS = [POSITIVE_GREEN, NEUTRAL_AMBER, NEGATIVE_RED]
SENTIMENT_COLOR_MAP = {
    'Positive': POSITIVE_GREEN,
    'Neutral': NEUTRAL_AMBER,
    'Negative': NEGATIVE_RED
}

# ========================================
# BUTTON STYLES
# ========================================
PRIMARY_BUTTON_COLOR = ACTION_RED
SECONDARY_BUTTON_COLOR = INACTIVE_GRAY

# ========================================
# TEXT COLORS
# ========================================
HEADING_COLOR = MAIN_BLUE
WHITE_TEXT = "#FFFFFF"
LIGHT_GRAY_TEXT = "#B0B0B0"

# ========================================
# USAGE NOTES
# ========================================
"""
Color Usage Guidelines:
----------------------

Headings / Titles:
    → Use MAIN_BLUE (#1E6FB8)

Sentiment Charts (Pie, Donut, Bars):
    → Positive: POSITIVE_GREEN (#2ECC71)
    → Neutral: NEUTRAL_AMBER (#F1C40F)
    → Negative: NEGATIVE_RED (#E74C3C)

Buttons:
    → Primary Action: ACTION_RED (#FF4D4F)
    → Secondary/Inactive: INACTIVE_GRAY (#2A2D33)

Info Boxes:
    → Info: INFO_BLUE (#2F80ED)
    → Success: SUCCESS_GREEN (#27AE60)
    → Warning: WARNING_YELLOW (#F2C94C)

Background:
    → Base: DARK_NAVY (#0E1117)

Why This Palette?
----------------
✓ Works beautifully on dark theme
✓ Professional analytics dashboard aesthetic
✓ No relation to any political colors
✓ Enhances readability
✓ Modern and industry-grade
✓ High contrast for accessibility
"""
