import csv
import json
import os
import sys
import time
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Base configurations
BASE_URL = "http://books.toscrape.com/"
INDEX_URL = urljoin(BASE_URL, "index.html")

# Mapping of text ratings to numerical values
RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5
}

class BookScraper:
    def __init__(self, base_url=BASE_URL, delay=0.1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        # Add headers to look like a standard browser request
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def fetch_page(self, url):
        """Fetches HTML content of a URL with error handling."""
        try:
            time.sleep(self.delay)  # Polite scraping delay
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "lxml")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            return None

    def get_categories(self):
        """Scrapes the sidebar to get categories and their relative URLs."""
        print("Fetching categories from index page...")
        soup = self.fetch_page(INDEX_URL)
        if not soup:
            print("Failed to load main page. Exiting.")
            return []

        categories = []
        # Find side categories container
        side_categories = soup.find("div", class_="side_categories")
        if not side_categories:
            print("Could not find categories panel.")
            return []

        # Find the nested list under 'Books'
        books_list = side_categories.find("ul").find("li")
        category_links = books_list.find("ul").find_all("a") if books_list.find("ul") else []

        for link in category_links:
            cat_name = link.text.strip()
            cat_href = link.get("href")
            # Resolve to absolute URL
            cat_url = urljoin(INDEX_URL, cat_href)
            categories.append({
                "name": cat_name,
                "url": cat_url
            })

        print(f"Found {len(categories)} categories to scrape.")
        return categories

    def parse_books_on_page(self, soup, category_name, page_url):
        """Parses all books from a listing page."""
        books = []
        book_pods = soup.find_all("article", class_="product_pod")

        for pod in book_pods:
            # 1. Title (contained in full inside the 'title' attribute of the link)
            title_tag = pod.find("h3").find("a")
            title = title_tag.get("title") or title_tag.text.strip()

            # 2. Detail URL
            detail_href = title_tag.get("href")
            detail_url = urljoin(page_url, detail_href)

            # 3. Price
            price_tag = pod.find("p", class_="price_color")
            price_str = price_tag.text.strip() if price_tag else "£0.00"
            try:
                price_gbp = float(price_str.replace("£", "").replace("Â", "").strip())
                price = round(price_gbp * 385.0, 2)  # Convert to Rs. (1 GBP = 385 LKR)
            except ValueError:
                price = 0.0

            # 4. Rating (class star-rating holds the rating name)
            rating_tag = pod.find("p", class_="star-rating")
            rating_num = 0
            if rating_tag:
                # Find the class that matches rating (e.g. 'Three')
                classes = rating_tag.get("class", [])
                for cls in classes:
                    if cls.lower() in RATING_MAP:
                        rating_num = RATING_MAP[cls.lower()]
                        break

            # 5. Availability
            avail_tag = pod.find("p", class_="availability")
            availability = "In stock"
            if avail_tag:
                availability = avail_tag.text.strip()

            books.append({
                "title": title,
                "category": category_name,
                "price": price,
                "rating": rating_num,
                "availability": availability,
                "url": detail_url
            })

        return books

    def scrape_all(self):
        """Scrapes all books by going through each category."""
        categories = self.get_categories()
        all_books = []

        for index, cat in enumerate(categories, 1):
            cat_name = cat["name"]
            cat_url = cat["url"]
            print(f"[{index}/{len(categories)}] Scraping Category: {cat_name}")

            current_url = cat_url
            page_num = 1

            while current_url:
                soup = self.fetch_page(current_url)
                if not soup:
                    print(f"  Failed to load page for {cat_name}. Skipping remainder.")
                    break

                books = self.parse_books_on_page(soup, cat_name, current_url)
                all_books.extend(books)
                print(f"  Page {page_num}: Found {len(books)} books.")

                # Check if there is a next page button
                next_tag = soup.find("li", class_="next")
                if next_tag:
                    next_href = next_tag.find("a").get("href")
                    current_url = urljoin(current_url, next_href)
                    page_num += 1
                else:
                    current_url = None

        print(f"\nScraping complete! Total books scraped: {len(all_books)}")
        return all_books

def save_data(books, csv_path, json_path):
    """Saves list of books to CSV and JSON formats."""
    df = pd.DataFrame(books)

    # Reorder columns for readability
    cols = ["title", "category", "price", "rating", "availability", "url"]
    df = df[cols]

    # Save to CSV
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved CSV dataset to: {csv_path}")

    # Save to JSON
    df.to_json(json_path, orient="records", indent=4, force_ascii=False)
    print(f"Saved JSON dataset to: {json_path}")

if __name__ == "__main__":
    print("==================================================")
    print("          Books to Scrape Web Scraper             ")
    print("==================================================")
    
    # Run the scraper
    scraper = BookScraper(delay=0.1)
    scraped_books = scraper.scrape_all()

    if scraped_books:
        # Define paths
        csv_file = "books_dataset.csv"
        json_file = "books_dataset.json"
        
        save_data(scraped_books, csv_file, json_file)
        print("\nProcess finished successfully.")
    else:
        print("\nNo books scraped. Check network connection or website structure.")
