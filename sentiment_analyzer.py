"""
Sentiment Analysis Module
Implements VADER + TextBlob hybrid sentiment analysis for political news
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


class SentimentAnalyzer:
    """
    Advanced sentiment analyzer using VADER and TextBlob ensemble method
    """
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text):
        """
        Analyze sentiment of given text using VADER and TextBlob
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment analysis results with scores and classification
        """
        if not text or not isinstance(text, str):
            return self._get_neutral_result()
        
        # VADER Analysis (better for social media and news)
        vader_scores = self.vader.polarity_scores(text)
        
        # TextBlob Analysis (good for general text)
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity  # -1 to 1
        textblob_subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Ensemble: Combine both methods (70% VADER, 30% TextBlob)
        # VADER is weighted more because it's optimized for social media/news
        compound_score = (vader_scores['compound'] * 0.7) + (textblob_polarity * 0.3)
        
        # Classify sentiment
        classification = self._classify_sentiment(compound_score)
        
        # Calculate confidence based on score strength
        confidence = self._calculate_confidence(compound_score, vader_scores, textblob_polarity)
        
        return {
            'classification': classification,
            'compound_score': round(compound_score, 4),
            'confidence': round(confidence, 2),
            'positive': round(vader_scores['pos'], 4),
            'neutral': round(vader_scores['neu'], 4),
            'negative': round(vader_scores['neg'], 4),
            'subjectivity': round(textblob_subjectivity, 4),
            'vader_compound': round(vader_scores['compound'], 4),
            'textblob_polarity': round(textblob_polarity, 4)
        }
    
    def analyze_article(self, article):
        """
        Analyze sentiment of a news article
        
        Args:
            article (dict): Article with 'title' and 'description'
            
        Returns:
            dict: Sentiment analysis results
        """
        # Combine title and description (title weighted more heavily)
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Title has 2x weight because it's more impactful
        combined_text = f"{title}. {title}. {description}"
        
        return self.analyze_text(combined_text)
    
    def analyze_articles_batch(self, articles):
        """
        Analyze sentiment of multiple articles
        
        Args:
            articles (list): List of article dictionaries
            
        Returns:
            dict: Overall sentiment statistics and individual results
        """
        if not articles:
            return self._get_empty_batch_result()
        
        results = []
        positive_count = 0
        neutral_count = 0
        negative_count = 0
        total_compound = 0
        total_confidence = 0
        
        for article in articles:
            sentiment = self.analyze_article(article)
            results.append(sentiment)
            
            # Count classifications
            if sentiment['classification'] == 'Positive':
                positive_count += 1
            elif sentiment['classification'] == 'Negative':
                negative_count += 1
            else:
                neutral_count += 1
            
            total_compound += sentiment['compound_score']
            total_confidence += sentiment['confidence']
        
        total_articles = len(articles)
        
        return {
            'individual_results': results,
            'overall_statistics': {
                'positive_percentage': round((positive_count / total_articles) * 100, 2),
                'neutral_percentage': round((neutral_count / total_articles) * 100, 2),
                'negative_percentage': round((negative_count / total_articles) * 100, 2),
                'positive_count': positive_count,
                'neutral_count': neutral_count,
                'negative_count': negative_count,
                'total_articles': total_articles,
                'average_compound_score': round(total_compound / total_articles, 4),
                'average_confidence': round(total_confidence / total_articles, 2),
                'overall_sentiment': self._classify_sentiment(total_compound / total_articles)
            }
        }
    
    def _classify_sentiment(self, compound_score):
        """
        Classify sentiment based on compound score
        
        Args:
            compound_score (float): Compound sentiment score (-1 to 1)
            
        Returns:
            str: 'Positive', 'Negative', or 'Neutral'
        """
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    
    def _calculate_confidence(self, compound_score, vader_scores, textblob_polarity):
        """
        Calculate confidence level of sentiment prediction
        
        Args:
            compound_score (float): Combined compound score
            vader_scores (dict): VADER sentiment scores
            textblob_polarity (float): TextBlob polarity score
            
        Returns:
            float: Confidence percentage (0-100)
        """
        # Base confidence from absolute score strength
        base_confidence = abs(compound_score) * 100
        
        # Agreement bonus: if both methods agree, increase confidence
        vader_sentiment = self._classify_sentiment(vader_scores['compound'])
        textblob_sentiment = self._classify_sentiment(textblob_polarity)
        
        if vader_sentiment == textblob_sentiment:
            agreement_bonus = 20
        else:
            agreement_bonus = 0
        
        # Calculate final confidence (capped at 100)
        confidence = min(base_confidence + agreement_bonus, 100)
        
        return max(confidence, 30)  # Minimum 30% confidence
    
    def _get_neutral_result(self):
        """Return neutral sentiment result for empty/invalid text"""
        return {
            'classification': 'Neutral',
            'compound_score': 0.0,
            'confidence': 30.0,
            'positive': 0.0,
            'neutral': 1.0,
            'negative': 0.0,
            'subjectivity': 0.0,
            'vader_compound': 0.0,
            'textblob_polarity': 0.0
        }
    
    def _get_empty_batch_result(self):
        """Return empty result for batch analysis with no articles"""
        return {
            'individual_results': [],
            'overall_statistics': {
                'positive_percentage': 0.0,
                'neutral_percentage': 0.0,
                'negative_percentage': 0.0,
                'positive_count': 0,
                'neutral_count': 0,
                'negative_count': 0,
                'total_articles': 0,
                'average_compound_score': 0.0,
                'average_confidence': 0.0,
                'overall_sentiment': 'Neutral'
            }
        }
    
    def get_sentiment_emoji(self, classification):
        """
        Get emoji representation of sentiment
        
        Args:
            classification (str): 'Positive', 'Negative', or 'Neutral'
            
        Returns:
            str: Emoji representing sentiment
        """
        emoji_map = {
            'Positive': '😊',
            'Negative': '😢',
            'Neutral': '😐'
        }
        return emoji_map.get(classification, '😐')
    
    def get_sentiment_color(self, classification):
        """
        Get color code for sentiment visualization
        
        Args:
            classification (str): 'Positive', 'Negative', or 'Neutral'
            
        Returns:
            str: Color name or hex code
        """
        color_map = {
            'Positive': '#28a745',  # Green
            'Negative': '#dc3545',  # Red
            'Neutral': '#ffc107'    # Yellow
        }
        return color_map.get(classification, '#6c757d')
    
    def get_sentiment_insights(self, batch_results):
        """
        Generate insights from batch sentiment analysis
        
        Args:
            batch_results (dict): Results from analyze_articles_batch
            
        Returns:
            list: List of insight strings
        """
        stats = batch_results['overall_statistics']
        insights = []
        
        # Overall sentiment insight
        overall = stats['overall_sentiment']
        insights.append(f"Overall sentiment is **{overall}** across all articles")
        
        # Dominant sentiment
        if stats['positive_percentage'] > 50:
            insights.append(f"Majority of coverage is **positive** ({stats['positive_percentage']}%)")
        elif stats['negative_percentage'] > 50:
            insights.append(f"Majority of coverage is **negative** ({stats['negative_percentage']}%)")
        elif stats['neutral_percentage'] > 50:
            insights.append(f"Majority of coverage is **neutral** ({stats['neutral_percentage']}%)")
        else:
            insights.append("Coverage is **mixed** with no dominant sentiment")
        
        # Confidence insight
        avg_conf = stats['average_confidence']
        if avg_conf >= 80:
            insights.append(f"Analysis confidence is **very high** ({avg_conf}%)")
        elif avg_conf >= 60:
            insights.append(f"Analysis confidence is **high** ({avg_conf}%)")
        elif avg_conf >= 40:
            insights.append(f"Analysis confidence is **moderate** ({avg_conf}%)")
        else:
            insights.append(f"Analysis confidence is **low** ({avg_conf}%)")
        
        # Distribution insight
        if abs(stats['positive_percentage'] - stats['negative_percentage']) < 10:
            insights.append("Coverage is **balanced** between positive and negative sentiments")
        
        return insights


# Singleton instance for easy import
_analyzer_instance = None

def get_analyzer():
    """Get singleton instance of SentimentAnalyzer"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = SentimentAnalyzer()
    return _analyzer_instance
