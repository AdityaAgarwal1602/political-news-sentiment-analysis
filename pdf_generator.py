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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_sentiment_charts(data):
    """
    Create sentiment visualization charts and save as images using matplotlib
    
    Args:
        data: Dictionary containing sentiment data
        
    Returns:
        tuple: (pie_chart_path, bar_chart_path)
    """
    positive_count = data.get('positive_count', 0)
    neutral_count = data.get('neutral_count', 0)
    negative_count = data.get('negative_count', 0)
    positive_pct = data.get('positive_pct', 0)
    neutral_pct = data.get('neutral_pct', 0)
    negative_pct = data.get('negative_pct', 0)
    
    colors_list = ['#28a745', '#ffc107', '#dc3545']  # Green, Yellow, Red
    labels = ['Positive', 'Neutral', 'Negative']
    counts = [positive_count, neutral_count, negative_count]
    percentages = [positive_pct, neutral_pct, negative_pct]
    
    # Create pie chart
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax1.pie(
        counts, 
        labels=labels, 
        colors=colors_list,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 11, 'weight': 'bold'}
    )
    
    # Make percentage text white
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
    
    ax1.set_title('Sentiment Distribution', fontsize=14, weight='bold', color='#1F77B4', pad=20)
    ax1.axis('equal')
    
    # Save pie chart
    pie_path = 'temp_pie_chart.png'
    plt.tight_layout()
    plt.savefig(pie_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Create bar chart
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    bars = ax2.bar(labels, counts, color=colors_list, edgecolor='black', linewidth=1.5)
    
    # Add percentage labels on bars
    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{pct}%',
                ha='center', va='bottom', fontsize=12, weight='bold')
    
    ax2.set_ylabel('Article Count', fontsize=11, weight='bold')
    ax2.set_title('Article Count by Sentiment', fontsize=14, weight='bold', color='#1F77B4', pad=20)
    ax2.set_ylim(0, max(counts) * 1.2 if max(counts) > 0 else 10)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    # Save bar chart
    bar_path = 'temp_bar_chart.png'
    plt.tight_layout()
    plt.savefig(bar_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return pie_path, bar_path

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
    overall_sentiment = data.get('overall_sentiment', 'N/A')
    avg_confidence = data.get('average_confidence', 0)
    
    meta_data = [
        ['Report Generated:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
        ['Analyzed By:', data.get('username', 'N/A')],
        ['Political Party:', data.get('party', 'N/A')],
        ['State/UT:', data.get('state', 'N/A')],
        ['Articles Analyzed:', str(data.get('articles_count', 0))],
        ['Overall Sentiment:', overall_sentiment],
        ['AI Confidence:', f"{avg_confidence}%"]
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
    
    # Overall Sentiment Summary with real data
    heading = Paragraph("� AI-Powered Sentiment Analysis Results", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 12))
    
    positive_pct = data.get('positive_pct', 0)
    neutral_pct = data.get('neutral_pct', 0)
    negative_pct = data.get('negative_pct', 0)
    
    sentiment_data = [
        ['Sentiment Type', 'Percentage', 'Article Count', 'Status'],
        ['😊 Positive', f"{positive_pct}%", str(data.get('positive_count', 0)), '✓'],
        ['😐 Neutral', f"{neutral_pct}%", str(data.get('neutral_count', 0)), '✓'],
        ['😢 Negative', f"{negative_pct}%", str(data.get('negative_count', 0)), '✓']
    ]
    
    sentiment_table = Table(sentiment_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F77B4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    
    elements.append(sentiment_table)
    elements.append(Spacer(1, 15))
    
    # Analysis Quality Metrics
    quality_note = Paragraph(
        f"<b>Analysis Method:</b> VADER + TextBlob Ensemble AI Model | "
        f"<b>Average Confidence:</b> {avg_confidence}% | "
        f"<b>Overall Result:</b> {overall_sentiment}",
        normal_style
    )
    elements.append(quality_note)
    elements.append(Spacer(1, 20))
    
    # Generate and add visualization charts
    try:
        pie_path, bar_path = create_sentiment_charts(data)
        
        # Add charts heading
        heading = Paragraph("📊 Visual Analysis", heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        # Create table with two charts side by side
        chart_table_data = []
        
        # Add pie chart and bar chart
        if os.path.exists(pie_path) and os.path.exists(bar_path):
            pie_img = Image(pie_path, width=3*inch, height=2.4*inch)
            bar_img = Image(bar_path, width=3*inch, height=2.4*inch)
            chart_table_data.append([pie_img, bar_img])
            
            chart_table = Table(chart_table_data, colWidths=[3*inch, 3*inch])
            chart_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(chart_table)
            elements.append(Spacer(1, 20))
            
    except Exception as e:
        # If chart generation fails, skip silently
        pass
    
    # AI-Generated Key Insights
    heading = Paragraph("💡 AI-Generated Key Insights", heading_style)
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
    
    # Individual Article Analysis with real sentiment data
    heading = Paragraph("📰 Detailed Article-by-Article Sentiment Analysis", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 12))
    
    articles = data.get('articles', [])
    individual_sentiments = data.get('individual_sentiments', [])
    
    for idx, article in enumerate(articles[:10], 1):  # Limit to 10 articles for PDF
        article_title = article.get('title', 'No Title')
        source = article.get('source', {}).get('name', 'Unknown')
        published = article.get('publishedAt', 'Unknown')[:10]
        description = article.get('description', 'No description available')
        
        # Get real sentiment data if available
        if idx <= len(individual_sentiments):
            sentiment_data = individual_sentiments[idx-1]
            classification = sentiment_data.get('classification', 'Neutral')
            confidence = sentiment_data.get('confidence', 0)
            compound_score = sentiment_data.get('compound_score', 0)
            positive = sentiment_data.get('positive', 0) * 100
            neutral = sentiment_data.get('neutral', 0) * 100
            negative = sentiment_data.get('negative', 0) * 100
        else:
            # Fallback to default
            classification = 'Neutral'
            confidence = 50
            compound_score = 0
            positive = neutral = negative = 33
        
        # Get emoji for sentiment
        emoji = '😊' if classification == 'Positive' else '😢' if classification == 'Negative' else '😐'
        
        # Article title with emoji
        article_heading = Paragraph(f"<b>{emoji} {idx}. {article_title[:80]}{'...' if len(article_title) > 80 else ''}</b>", normal_style)
        elements.append(article_heading)
        elements.append(Spacer(1, 6))
        
        # Article details table with real sentiment scores
        article_data = [
            ['Source:', source, 'Published:', published],
            ['Sentiment:', f"{classification} ({confidence:.1f}% confidence)", 'Score:', f"{compound_score:.4f}"],
            ['Positive:', f"{positive:.1f}%", 'Neutral:', f"{neutral:.1f}%"],
            ['Negative:', f"{negative:.1f}%", '', '']
        ]
        
        article_table = Table(article_data, colWidths=[1.2*inch, 2.2*inch, 1.2*inch, 1.4*inch])
        article_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F0F0F0')),
        ]))
        
        elements.append(article_table)
        elements.append(Spacer(1, 6))
        
        # Description
        desc_text = Paragraph(f"<i>{description[:250]}{'...' if len(description) > 250 else ''}</i>", normal_style)
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
        f"Report generated by Political News Sentiment Analysis System with AI (VADER + TextBlob)<br/>"
        f"© {datetime.now().year} - For analytical and informational purposes only",
        footer_style
    )
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Clean up temporary chart images
    try:
        if os.path.exists('temp_pie_chart.png'):
            os.remove('temp_pie_chart.png')
        if os.path.exists('temp_bar_chart.png'):
            os.remove('temp_bar_chart.png')
    except:
        pass
    
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
