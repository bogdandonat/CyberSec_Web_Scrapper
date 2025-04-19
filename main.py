from fetcher import DataFetcher
from summarizer import DataSummarizer
from opensearchpy import OpenSearch

class MainApp:
    def __init__(self, sources_file, opensearch_host='localhost', opensearch_port=9200, index_name='cybersecurity'):
        self.fetcher = DataFetcher(sources_file)
        self.summarizer = DataSummarizer()
        self.client = OpenSearch(hosts=[{'host': opensearch_host, 'port': opensearch_port}])
        self.index_name = index_name

    def save_to_opensearch(self, data):
        for article in data:
            response = self.client.index(index=self.index_name, body=article)
            print(f"Document ID: {response['_id']} saved to OpenSearch.")

    def run(self):
        print("Fetching data...")
        raw_data = self.fetcher.fetch_data()
        print(f"Fetched {len(raw_data)} articles/posts.")
        
        print("Summarizing data...")
        summarized_data = self.summarizer.summarize_data(raw_data)
        
        print("Saving summarized data to OpenSearch...")
        self.save_to_opensearch(summarized_data)

if __name__ == "__main__":
    app = MainApp(sources_file='sources.yaml')
    app.run()
