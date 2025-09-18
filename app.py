from flask import Flask, render_template, request# request Lets you access data sent by the user via HTTP methods like GET or POST.
from news_scraper import get_articles_from_rss
from summarizer import summarize_articles

app = Flask(__name__) # Creating an instance of the Flask app.

@app.route("/", methods=["GET", "POST"])#Creating a route for the home page (/) that handles both GET and POST requests.
def index(): #This function is executed when a request is made to the / route.
    topics = request.form.get("topics", "").strip()
    if not topics:
        topics = "technology, world, science"
    print("Fetching articles for topics:", topics)
    articles = get_articles_from_rss(topics)#get_articles_from_rss function with the given topics to scrape news articles.
    print(f"Fetched {len(articles)} articles.")#Logs how many articles were fetched, useful for debugging.
    summaries = summarize_articles(articles)#Passes the fetched articles to the summarization function and stores the summarized content.
    print(f"Summaries generated for {len(summaries)} articles.")
    return render_template("index.html", summaries=summaries)

if __name__ == "__main__":#Checks if this script is being run directly 
    app.run(debug=True)
