from transformers import pipeline

class DataSummarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
    
    def summarize_article(self, article):
        text = article['summary']
        if len(text) > 100:
            summarized = self.summarizer(text, max_length=150, min_length=50, do_sample=False)
            return summarized[0]['summary_text']
        return text

    def summarize_data(self, data):
        summarized_data = []
        for article in data:
            summary = self.summarize_article(article)
            article['summary'] = summary
            summarized_data.append(article)
        return summarized_data
