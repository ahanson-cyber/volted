import json
from elasticsearch import Elasticsearch
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Index data from a JSON file into Elasticsearch"

    def handle(self, *args, **options):
        with open("abc_news_articles.json", "r") as f:
            data = json.load(f)

        es = Elasticsearch(["http://localhost:9200"])

        index_name = "articles"
        mapping = {
            "mappings": {
                "properties": {
                    "article_name": {"type": "text"},
                    "article_link": {"type": "keyword"},
                    "article_date": {"type": "date"},
                }
            }
        }

        es.indices.create(index=index_name, body=mapping, ignore=400)

        # Index each document in the data
        for article in data:
            es.index(index=index_name, body=article)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully indexed {len(data)} documents into Elasticsearch"
            )
        )
