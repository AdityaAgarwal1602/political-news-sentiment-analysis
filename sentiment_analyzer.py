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
    
    def analyze_article(self, article, target_party=None):
        """
        Analyze sentiment of a news article with party-specific context
        
        Args:
            article (dict): Article with 'title' and 'description'
            target_party (str): The party being analyzed (e.g., "BJP", "Congress")
            
        Returns:
            dict: Sentiment analysis results (party-specific if target_party provided)
        """
        # Combine title and description (title weighted more heavily)
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Title has 2x weight because it's more impactful
        combined_text = f"{title}. {title}. {description}"
        
        # Get base sentiment analysis
        result = self.analyze_text(combined_text)
        
        # If target party specified, adjust sentiment based on party context
        if target_party:
            result = self._adjust_for_party_context(result, combined_text, target_party)
            result['party_specific'] = True
            result['target_party'] = target_party
        else:
            result['party_specific'] = False
        
        return result
    
    def _adjust_for_party_context(self, base_result, text, target_party):
        """
        Adjust sentiment based on whether events are good/bad for the target party
        
        Args:
            base_result (dict): Base sentiment analysis
            text (str): Article text
            target_party (str): Party being analyzed
            
        Returns:
            dict: Adjusted sentiment analysis
        """
        text_lower = text.lower()
        party_lower = target_party.lower()
        
        # Keywords indicating good news for a party
        positive_indicators = [
            'win', 'victory', 'success', 'achievement', 'triumph', 'leads',
            'gains', 'progress', 'support', 'approval', 'popular', 'majority',
            'growth', 'development', 'benefit', 'advantage', 'celebrate',
            'acclaimed', 'praised', 'commended', 'strengthen'
        ]
        
        # Keywords indicating bad news for a party
        negative_indicators = [
            'defeat', 'loss', 'failure', 'scandal', 'criticism', 'protest',
            'opposition', 'decline', 'controversy', 'allegation', 'crisis',
            'setback', 'problem', 'issue', 'concern', 'doubt', 'questioned',
            'slammed', 'attacked', 'condemned', 'criticized'
        ]
        
        # Opposition keywords (defeats of opposition = good for target party)
        opposition_terms = ['opposition', 'rival', 'competitor', 'against']
        
        # Check if article mentions the target party
        party_mentioned = party_lower in text_lower
        
        if not party_mentioned:
            # If party not mentioned, return base result
            base_result['context_note'] = f"Article may not be directly about {target_party}"
            return base_result
        
        # Count positive and negative indicators near party mentions
        party_context_positive = 0
        party_context_negative = 0
        
        # Simple context analysis: check words around party name
        sentences = text.split('.')
        for sentence in sentences:
            if party_lower in sentence.lower():
                sentence_lower = sentence.lower()
                
                # Check for positive indicators
                for indicator in positive_indicators:
                    if indicator in sentence_lower:
                        party_context_positive += 1
                
                # Check for negative indicators
                for indicator in negative_indicators:
                    if indicator in sentence_lower:
                        # Check if it's about opposition (negative for them = positive for target)
                        is_about_opposition = any(opp in sentence_lower for opp in opposition_terms)
                        if is_about_opposition and party_lower not in sentence_lower[:sentence_lower.index(indicator)]:
                            party_context_positive += 0.5  # Opposition's negative = our positive
                        else:
                            party_context_negative += 1
        
        # Adjust compound score based on party-specific context
        context_adjustment = 0
        if party_context_positive > party_context_negative:
            context_adjustment = 0.1 * (party_context_positive - party_context_negative)
        elif party_context_negative > party_context_positive:
            context_adjustment = -0.1 * (party_context_negative - party_context_positive)
        
        # Apply adjustment (capped at ±0.3 to avoid over-correction)
        context_adjustment = max(-0.3, min(0.3, context_adjustment))
        adjusted_compound = base_result['compound_score'] + context_adjustment
        adjusted_compound = max(-1.0, min(1.0, adjusted_compound))  # Keep in valid range
        
        # Reclassify with adjusted score
        adjusted_classification = self._classify_sentiment(adjusted_compound)
        
        # Update result
        base_result['compound_score'] = round(adjusted_compound, 4)
        base_result['classification'] = adjusted_classification
        base_result['context_adjustment'] = round(context_adjustment, 4)
        base_result['original_compound'] = round(base_result['compound_score'] - context_adjustment, 4)
        
        # Add explanation
        if context_adjustment > 0.05:
            base_result['context_note'] = f"Adjusted more positive for {target_party} based on favorable context"
        elif context_adjustment < -0.05:
            base_result['context_note'] = f"Adjusted more negative for {target_party} based on unfavorable context"
        else:
            base_result['context_note'] = f"Sentiment directly reflects impact on {target_party}"
        
        return base_result
    
    def analyze_articles_batch(self, articles, target_party=None):
        """
        Analyze sentiment of multiple articles with optional party-specific context
        
        Args:
            articles (list): List of article dictionaries
            target_party (str): Optional party name for party-specific analysis
            
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
            sentiment = self.analyze_article(article, target_party=target_party)
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
            str: Color hex code
        """
        from colors import SENTIMENT_COLOR_MAP
        return SENTIMENT_COLOR_MAP.get(classification, SENTIMENT_COLOR_MAP['Neutral'])
    
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
    
    def get_human_readable_summary(self, batch_results):
        """
        Generate a natural language narrative summary of the sentiment analysis
        
        Args:
            batch_results (dict): Results from analyze_articles_batch
            
        Returns:
            str: Human-readable narrative summary
        """
        stats = batch_results['overall_statistics']
        
        # Build narrative
        narrative_parts = []
        
        # Opening statement
        total = stats['total_articles']
        overall = stats['overall_sentiment'].lower()
        narrative_parts.append(
            f"After analyzing {total} news {'article' if total == 1 else 'articles'}, "
            f"the AI detected an overall **{overall}** sentiment."
        )
        
        # Distribution narrative
        pos_pct = stats['positive_percentage']
        neu_pct = stats['neutral_percentage']
        neg_pct = stats['negative_percentage']
        
        # Find dominant sentiment
        sentiments = [
            (pos_pct, 'positive', stats['positive_count']),
            (neu_pct, 'neutral', stats['neutral_count']),
            (neg_pct, 'negative', stats['negative_count'])
        ]
        sentiments.sort(reverse=True)
        
        dominant_pct, dominant_type, dominant_count = sentiments[0]
        
        if dominant_pct > 60:
            narrative_parts.append(
                f"The coverage is **strongly {dominant_type}**, with {dominant_count} out of {total} "
                f"{'article' if total == 1 else 'articles'} ({dominant_pct}%) showing {dominant_type} tone."
            )
        elif dominant_pct > 40:
            narrative_parts.append(
                f"The coverage **leans {dominant_type}**, representing {dominant_pct}% of all articles analyzed."
            )
        else:
            narrative_parts.append(
                f"The coverage is **evenly distributed** across sentiment types, "
                f"with no single sentiment dominating the conversation."
            )
        
        # Confidence narrative
        avg_conf = stats['average_confidence']
        if avg_conf >= 75:
            confidence_desc = "very reliable"
        elif avg_conf >= 60:
            confidence_desc = "reliable"
        elif avg_conf >= 45:
            confidence_desc = "moderately confident"
        else:
            confidence_desc = "somewhat uncertain"
        
        narrative_parts.append(
            f"The AI's analysis is **{confidence_desc}** with an average confidence of {avg_conf:.1f}%."
        )
        
        # Compound score interpretation
        compound = stats['average_compound_score']
        if compound > 0.5:
            tone_desc = "strongly positive tone"
        elif compound > 0.1:
            tone_desc = "mildly positive tone"
        elif compound > -0.1:
            tone_desc = "neutral/balanced tone"
        elif compound > -0.5:
            tone_desc = "mildly negative tone"
        else:
            tone_desc = "strongly negative tone"
        
        narrative_parts.append(
            f"The language used in these articles carries a **{tone_desc}** (compound score: {compound:.3f})."
        )
        
        return " ".join(narrative_parts)
    
    def explain_score(self, score_type, score_value):
        """
        Provide plain English explanation for technical scores
        
        Args:
            score_type (str): Type of score ('compound', 'confidence', 'subjectivity')
            score_value (float): The score value
            
        Returns:
            str: Human-readable explanation
        """
        if score_type == 'compound':
            # Compound score is -1 to +1
            if score_value >= 0.5:
                return "Very positive language - strong favorable terms used"
            elif score_value >= 0.05:
                return "Somewhat positive - more favorable than critical"
            elif score_value > -0.05:
                return "Balanced/neutral - no strong positive or negative bias"
            elif score_value > -0.5:
                return "Somewhat negative - more critical than favorable"
            else:
                return "Very negative language - strong critical terms used"
        
        elif score_type == 'confidence':
            # Confidence is 30-100%
            if score_value >= 80:
                return "The AI is very certain about this classification"
            elif score_value >= 65:
                return "The AI is quite confident in this assessment"
            elif score_value >= 50:
                return "The AI has moderate confidence in this result"
            elif score_value >= 40:
                return "The AI is somewhat unsure about this classification"
            else:
                return "The AI finds this text ambiguous or unclear"
        
        elif score_type == 'subjectivity':
            # Subjectivity is 0 to 1
            if score_value >= 0.7:
                return "Highly opinion-based - lots of personal views/judgments"
            elif score_value >= 0.5:
                return "Moderately subjective - mix of facts and opinions"
            elif score_value >= 0.3:
                return "Mostly factual with some opinion elements"
            else:
                return "Very objective - primarily factual reporting"
        
        return "Score explanation unavailable"


# Singleton instance for easy import
_analyzer_instance = None

def get_analyzer():
    """Get singleton instance of SentimentAnalyzer"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = SentimentAnalyzer()
    return _analyzer_instance
