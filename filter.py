def filter_articles_by_keywords(articles, keywords):
    filtered = []
    for article in articles:
        if any(keyword.lower() in article['text'].lower() for keyword in keywords):
            filtered.append(article)
    return filtered
