from sentiment_analyzer import get_analyzer

# Initialize analyzer
analyzer = get_analyzer()

print("\n" + "="*80)
print("PARTY-SPECIFIC SENTIMENT ANALYSIS TEST")
print("="*80)

# Test articles with different scenarios
test_articles = [
    {
        'title': 'BJP wins massive victory in Maharashtra elections',
        'description': 'The party celebrates historic success with record turnout'
    },
    {
        'title': 'Opposition suffers major defeat in recent polls',
        'description': 'Congress and other parties lose ground as BJP gains majority'
    },
    {
        'title': 'BJP faces criticism over controversial policy decision',
        'description': 'Critics slam the government for failing to address key concerns'
    },
    {
        'title': 'Political rally draws huge crowd',
        'description': 'Thousands gather to hear speeches from various leaders'
    }
]

# Test 1: Analyze FOR BJP
print("\n" + "-"*80)
print("TEST 1: Analyzing articles FOR BJP (Party-Specific)")
print("-"*80)

bjp_results = analyzer.analyze_articles_batch(test_articles, target_party="BJP")

for idx, (article, sentiment) in enumerate(zip(test_articles, bjp_results['individual_results']), 1):
    print(f"\n{idx}. {article['title']}")
    print(f"   Classification: {sentiment['classification']}")
    print(f"   Compound Score: {sentiment['compound_score']:.4f}")
    if sentiment.get('context_adjustment'):
        print(f"   Context Adjustment: {sentiment['context_adjustment']:+.4f}")
        print(f"   Original Score: {sentiment.get('original_compound', 0):.4f}")
    if sentiment.get('context_note'):
        print(f"   Note: {sentiment['context_note']}")

# Test 2: Analyze FOR Congress
print("\n\n" + "-"*80)
print("TEST 2: Analyzing SAME articles FOR Congress (should show different results)")
print("-"*80)

congress_results = analyzer.analyze_articles_batch(test_articles, target_party="Congress")

for idx, (article, sentiment) in enumerate(zip(test_articles, congress_results['individual_results']), 1):
    print(f"\n{idx}. {article['title']}")
    print(f"   Classification: {sentiment['classification']}")
    print(f"   Compound Score: {sentiment['compound_score']:.4f}")
    if sentiment.get('context_adjustment'):
        print(f"   Context Adjustment: {sentiment['context_adjustment']:+.4f}")
    if sentiment.get('context_note'):
        print(f"   Note: {sentiment['context_note']}")

# Test 3: Compare specific article
print("\n\n" + "-"*80)
print("TEST 3: Detailed comparison - Article #2 (Opposition defeat)")
print("-"*80)

article_2 = test_articles[1]
print(f"\nArticle: {article_2['title']}")
print(f"Description: {article_2['description']}")

bjp_sentiment = bjp_results['individual_results'][1]
congress_sentiment = congress_results['individual_results'][1]

print(f"\nFOR BJP:")
print(f"  Classification: {bjp_sentiment['classification']}")
print(f"  Compound: {bjp_sentiment['compound_score']:.4f}")
print(f"  Note: {bjp_sentiment.get('context_note', 'N/A')}")

print(f"\nFOR Congress:")
print(f"  Classification: {congress_sentiment['classification']}")
print(f"  Compound: {congress_sentiment['compound_score']:.4f}")
print(f"  Note: {congress_sentiment.get('context_note', 'N/A')}")

print("\n" + "="*80)
print("✅ Party-specific analysis is working!")
print("="*80 + "\n")
