import feedparser
import praw
import yaml

class DataFetcher:
    def __init__(self, sources_file):
        self.sources_file = sources_file
        self.reddit = praw.Reddit(client_id='YOUR_ID', client_secret='YOUR_SECRET', user_agent='YOUR_AGENT')
        self.keywords = self.load_keywords()

    def load_sources(self):
        with open(self.sources_file, 'r') as file:
            sources = yaml.safe_load(file)
        return sources

    def load_keywords(self):
        sources = self.load_sources()
        return sources['keywords']

    def fetch_rss(self, rss_url, max_articles=5):
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:max_articles]:
            # Verificăm dacă titlul sau descrierea conțin cuvinte cheie
            if any(keyword.lower() in (entry.title + entry.summary).lower() for keyword in self.keywords):
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.summary
                })
        return articles

    def fetch_reddit(self, subreddit_name, keyword, max_results=5):
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for submission in subreddit.search(keyword, limit=max_results):
            # Verificăm dacă titlul sau descrierea conțin cuvinte cheie
            if any(k.lower() in submission.title.lower() or k.lower() in submission.selftext.lower() for k in self.keywords):
                posts.append({
                    'title': submission.title,
                    'link': submission.url,
                    'summary': submission.selftext
                })
        return posts

    def fetch_data(self):
        sources = self.load_sources()
        all_articles = []
        
        # Fetch RSS articles
        for feed in sources['rss_feeds']:
            articles = self.fetch_rss(feed['url'])
            all_articles.extend(articles)
        
        # Fetch Reddit posts
        for reddit_feed in sources['reddit_feeds']:
            posts = self.fetch_reddit(reddit_feed['name'], reddit_feed['query'])
            all_articles.extend(posts)
        
        return all_articles
