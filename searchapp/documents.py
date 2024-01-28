from django_elasticsearch_dsl import Document, Index
from .models import Article

# Create an Elasticsearch index
articles = Index("articles")


@articles.document
class ArticleDocument(Document):
    class Django:
        model = Article

    class Index:
        name = "articles"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
