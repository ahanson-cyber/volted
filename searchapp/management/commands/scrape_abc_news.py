import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


def clean_and_filter_articles(articles: list[dict]) -> list[dict]:
    result = []

    for article in articles:
        name = article.get("article_name")
        if len(name.split()) > 4:
            result.append(article)

    return result


class Command(BaseCommand):
    help = "Scrape top news articles from ABC News and save in JSON format"

    def handle(self, *args, **options):
        abc_news_url = "https://abcnews.go.com/"
        response = requests.get(abc_news_url)

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = []

            # Find all <a> elements within the main content area
            for anchor_element in soup.select("main a"):
                article_name = anchor_element.get_text(strip=True)
                article_link = anchor_element.get("href", "No Link")

                if article_name:
                    articles.append(
                        {
                            "article_name": article_name,
                            "article_link": article_link,
                            "article_date": current_date,
                        }
                    )

            articles = clean_and_filter_articles(articles)

            output_file = "abc_news_articles.json"
            with open(output_file, "w") as f:
                json.dump(articles, f, indent=2)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully scraped and saved {len(articles)} articles to {output_file}"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to fetch data from ABC News (Status Code: {response.status_code})"
                )
            )
