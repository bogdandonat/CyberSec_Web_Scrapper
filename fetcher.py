import feedparser
import praw
import yaml
import os

class DataFetcher:
    def __init__(self, sources_file):
        self.sources_file = sources_file
        self.reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"], 
            client_secret=os.environ["REDDIT_CLIENT_SECRET"], 
            user_agent=os.environ["REDDIT_CLIENT_AGENT"]
        )
        self.keywords = self.load_keywords()

    def load_sources(self):
        try:
            with open(self.sources_file, 'r') as file:
                yaml_file = yaml.safe_load(file)
            
            sources = {
                'rss_feeds': yaml_file.get('rss_feeds', []),
                'reddit_feeds': yaml_file.get('reddit_feeds', [])
            }
            return sources
        except Exception as e:
            print(f"Error in loading sources: {str(e)}")

    def load_keywords(self):
        try:
            with open(self.sources_file, 'r') as file:
                yaml_file = yaml.safe_load(file)
            
            return yaml_file.get('keywords', [])
        except Exception as e:
            print(f"Error in loading keywords: {str(e)}")

    def fetch_rss(self, rss_url, max_articles=5, min_keyword_counter=3):
        try:
            feed = feedparser.parse(rss_url)
            articles = []
            for entry in feed.entries[:max_articles]:
                content = (entry.title + " " + entry.summary).lower()
                matched_keywords = [k for k in self.keywords if k.lower() in content]
                
                if len(matched_keywords) >= min_keyword_counter:
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.summary,
                        #'matched_keywords': matched_keywords  # optional
                    })
            return articles
        except feedparser.exceptions.NonXMLContentType as e:
            print(f"Error fetching articles for feedparser: {str(e)}")



    def fetch_reddit(self, subreddit_name, max_results=5, min_keyword_counter=3):
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        try:
            for submission in subreddit.new(limit=max_results):  # sau .hot()
                content = (submission.title + " " + submission.selftext).lower()
                matched_keywords = [k for k in self.keywords if k.lower() in content]
                
                if len(matched_keywords) >= min_keyword_counter:
                    posts.append({
                        'title': submission.title,
                        'link': submission.url,
                        'summary': submission.selftext,
                        #'matched_keywords': matched_keywords  # optional
                    })
        except praw.exceptions.PRAWException as e:
            print(f"Error fetching posts for subreddit {subreddit_name}: {str(e)}")
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
            print(reddit_feed)
            posts = self.fetch_reddit(reddit_feed['name'])
            all_articles.extend(posts)
        
        return all_articles
