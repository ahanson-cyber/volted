from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from datetime import datetime


class Command(BaseCommand):
    help = "Delete documents from Elasticsearch by query"

    def add_arguments(self, parser):
        parser.add_argument("date", help='Date in the format "YYYY-MM-DD"')

    def handle(self, *args, **options):
        es = Elasticsearch(["http://localhost:9200"])

        index = "articles"

        date_str = options["date"]
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            self.stderr.write(
                self.style.ERROR("Invalid date format. Please use 'YYYY-MM-DD'")
            )
            return

        query = {
            "query": {
                "range": {
                    "article_date": {"gte": date_obj.strftime("%Y-%m-%dT00:00:00")}
                }
            }
        }

        # Use the Delete By Query API to delete documents matching the query
        response = es.delete_by_query(index=index, body=query)

        self.stdout.write(self.style.SUCCESS(str(response)))
