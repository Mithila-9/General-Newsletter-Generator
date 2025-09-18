import feedparser#Parses RSS feeds.
from urllib.request import Request, urlopen
from newspaper import Article  #Extracts full-text content from article URLs.
import concurrent.futures  #Enables multithreading for faster processing of articles.
import re #For regex-based HTML tag removal.
from html import unescape #Converts HTML entities to readable text

def strip_html_tags(text):
    clean = re.compile('<.*?>')                 #Removes all HTML tags from text using regex.Also converts HTML entities to normal characters
    return re.sub(clean, '', unescape(text))

def process_entry(entry):
    try:
        url = entry.link  # Get the article URL
        article = Article(url)  # Create Article object from Newspaper3k
        article.download()  # Download the article
        article.parse()  # Parse the article content

        # Extract the article's text and clean up any leading/trailing whitespace
        article_text = article.text.strip()

        print(f"Article text for {entry.title}:\n{article_text[:300]}...")  # Print first 300 characters of content for debugging purposes.

        # If no content in the article, fallback to the RSS summary
        rss_summary = strip_html_tags(entry.summary.strip()) if 'summary' in entry else ''

        # If article text is empty or too short, use RSS summary (if available)
        if len(article_text.split()) < 50:
            full_text = rss_summary if rss_summary else "Content not available."
        else:
            full_text = article_text

        # Return the article's title, URL, and content
        return {
            "title": entry.title,
            "url": url,
            "content": full_text
        }
    except Exception as e:
        print("Error processing entry:", e)
        return None  # Return None if there's an error

def get_articles_from_rss(topics):
    topic_list = [topic.strip() for topic in topics.split(",")]
    all_articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}#Initializes storage and headers to avoid blocks from user-agent filters.

    for topic in topic_list:
        feed_url = f"https://news.google.com/rss/search?q={topic}&hl=en-IN&gl=IN&ceid=IN:en"#Constructs a Google News RSS URL for each topic.
        try:
            req = Request(feed_url, headers=headers)
            response = urlopen(req, timeout=5) #Sends request, parses RSS XML feed.
            feed = feedparser.parse(response)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:#Uses multithreading to process articles faster (max 5 threads).
                results = executor.map(process_entry, feed.entries)
                for article in results: #Collects successfully processed articles.
                    if article is not None:
                        all_articles.append(article)
        except Exception as e: #Catches network or parsing errors and skips to the next topic.
            print(f"Error fetching RSS for topic '{topic}':", e)
            continue

    # Deduplicate by title
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        if article["title"] not in seen_titles:
            unique_articles.append(article)
            seen_titles.add(article["title"])
    # Adjust limit as needed; using 10 articles for now
    return unique_articles[:10]
