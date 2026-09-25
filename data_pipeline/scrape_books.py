"""Scrape 60+ books from three Books to Scrape categories into a CSV file."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


CATEGORIES = {
    "Travel": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "Mystery": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "Historical Fiction": (
        "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
    ),
}
OUTPUT_FILE = Path(__file__).with_name("books_3_categories.csv")


def clean_text(element) -> str:
    """Return visible text with internal whitespace normalized."""
    return " ".join(element.get_text(" ", strip=True).split())


def scrape_category(session: requests.Session, category: str, first_url: str) -> list[dict[str, str]]:
    """Follow a category's pagination and return its book rows."""
    books = []
    url = first_url

    while url:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for card in soup.select("article.product_pod"):
            title_link = card.select_one("h3 a")
            price = card.select_one("p.price_color")
            availability = card.select_one("p.instock.availability")
            rating = card.select_one("p.star-rating")

            # The rating is the second class: e.g., ['star-rating', 'Three'].
            books.append(
                {
                    "title": title_link["title"],
                    "price": clean_text(price),
                    "star_rating": rating["class"][1],
                    "availability": clean_text(availability),
                    "category": category,
                }
            )

        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None

    return books


def main() -> None:
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (educational scraper)"

    all_books = []
    for category, url in CATEGORIES.items():
        rows = scrape_category(session, category, url)
        print(f"{category}: {len(rows)} books")
        all_books.extend(rows)

    if len(all_books) < 60:
        raise RuntimeError(f"Expected at least 60 books; got {len(all_books)}")

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["title", "price", "star_rating", "availability", "category"],
        )
        writer.writeheader()
        writer.writerows(all_books)

    print(f"Wrote {len(all_books)} books to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
