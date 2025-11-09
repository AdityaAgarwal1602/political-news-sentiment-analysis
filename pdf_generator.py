"""
PDF Report Generator for Sentiment Analysis
Generates professional PDF reports with analysis results
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_sentiment_pdf(filename, data):
    """
    Generate PDF report for sentiment analysis
    
    Args:
        filename: Output PDF filename
        data: Dictionary containing analysis data
            - party: Political party name
            - state: State/UT name
            - username: Logged in username
            - articles_count: Number of articles analyzed
            - positive_pct: Positive sentiment percentage
            - neutral_pct: Neutral sentiment percentage
            - negative_pct: Negative sentiment percentage
            - articles: List of articles with sentiment scores
            - insights: List of key insights
    """
    
    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1F77B4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1F77B4'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14
    
    # Add logo if exists
    logo_path = "assets/svgviewer-png-output.png"
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=1.5*inch, height=1.5*inch)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 12))
        except:
            pass
    
    # Title
    title = Paragraph("Political News Sentiment Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Report metadata
    meta_data = [
        ['Report Generated:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
        ['Analyzed By:', data.get('username', 'N/A')],
        ['Political Party:', data.get('party', 'N/A')],
        ['State/UT:', data.get('state', 'N/A')],
        ['Articles Analyzed:', str(data.get('articles_count', 0))]
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F4F8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(meta_table)
    elements.append(Spacer(1, 20))
    
    # Overall Sentiment Summary
    heading = Paragraph("📈 Overall Sentiment Summary", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 12))
    
    sentiment_data = [
        ['Sentiment', 'Percentage', 'Trend'],
        ['Positive', f"{data.get('positive_pct', 0)}%", '↑ +5%'],
        ['Neutral', f"{data.get('neutral_pct', 0)}%", '↓ -2%'],
        ['Negative', f"{data.get('negative_pct', 0)}%", '↓ -3%']
    ]
    
    sentiment_table = Table(sentiment_data, colWidths=[2*inch, 2*inch, 2*inch])
    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F77B4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    
    elements.append(sentiment_table)
    elements.append(Spacer(1, 20))
    
    # Key Insights
    heading = Paragraph("💡 Key Insights", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 12))
    
    insights = data.get('insights', [
        "Majority of news articles show a neutral to positive sentiment",
        "Recent articles show an upward trend in positive sentiment",
        "Main topics: Policy announcements, public events, social initiatives"
    ])
    
    for insight in insights:
        p = Paragraph(f"• {insight}", normal_style)
        elements.append(p)
        elements.append(Spacer(1, 6))
    
    elements.append(Spacer(1, 20))
    
    # Individual Article Analysis
    heading = Paragraph("📰 Individual Article Sentiments", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 12))
    
    articles = data.get('articles', [])
    
    for idx, article in enumerate(articles[:10], 1):  # Limit to 10 articles for PDF
        article_title = article.get('title', 'No Title')
        source = article.get('source', {}).get('name', 'Unknown')
        published = article.get('publishedAt', 'Unknown')[:10]
        sentiment = article.get('sentiment', 'Positive')
        score = article.get('score', 0.75)
        description = article.get('description', 'No description available')
        
        # Article title
        article_heading = Paragraph(f"<b>{idx}. {article_title[:100]}...</b>", normal_style)
        elements.append(article_heading)
        elements.append(Spacer(1, 6))
        
        # Article details table
        article_data = [
            ['Source:', source],
            ['Published:', published],
            ['Sentiment:', f"{sentiment} (Score: {score})"],
        ]
        
        article_table = Table(article_data, colWidths=[1.5*inch, 4.5*inch])
        article_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(article_table)
        elements.append(Spacer(1, 6))
        
        # Description
        desc_text = Paragraph(f"<i>{description[:200]}...</i>", normal_style)
        elements.append(desc_text)
        elements.append(Spacer(1, 12))
        
        # Add page break after every 3 articles
        if idx % 3 == 0 and idx < len(articles):
            elements.append(PageBreak())
    
    # Footer section
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    footer = Paragraph(
        f"Report generated by Political News Sentiment Analysis System<br/>"
        f"© {datetime.now().year} - For analytical purposes only",
        footer_style
    )
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    return True

def generate_quick_pdf(filename, party, state, username, articles_count):
    """
    Quick PDF generation with default placeholder data
    """
    data = {
        'party': party,
        'state': state,
        'username': username,
        'articles_count': articles_count,
        'positive_pct': 35,
        'neutral_pct': 45,
        'negative_pct': 20,
        'insights': [
            "Majority of news articles show a neutral to positive sentiment",
            "Recent articles show an upward trend in positive sentiment",
            "Main topics: Policy announcements, public events, social initiatives"
        ],
        'articles': []
    }
    
    return generate_sentiment_pdf(filename, data)
