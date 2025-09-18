from transformers import pipeline#Imports Hugging Face’s pipeline abstraction to easily load models like summarizers, classifiers, etc.

# Load the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)#device=-1 → run on CPU

def summarize_articles(articles):
    summarized = []
    for article in articles:
        title = article.get("title", "")
        content = article.get("content", "")
        url = article.get("url", "")

        # Skip if there's no usable content
        if not content or len(content.strip()) < 40:
            summary = "(No usable content)"
        else:
            try:
                summary = summarizer(content[:1024], max_length=100, min_length=30, do_sample=False)[0]['summary_text']#do_sample=False: Disables randomness; makes output deterministic.
                # Avoid echoing the title as summary
                if summary.strip().lower() == title.strip().lower():
                    summary = "(Summary same as title or not informative)"
            except Exception as e:
                summary = f"(Summarization failed: {e})"

        summarized.append({
            "title": title,
            "summary": summary,
            "url": url
        })

    return summarized
