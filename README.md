# Web Scraping & Data Analysis (Task 1)

Welcome to the **Web Scraping & Data Analysis** project completed as part of the **CodeAlpha Data Analytics Internship**. 

This project demonstrates how to build a robust Python web scraper, clean and structure the collected data, perform statistical data analysis, and produce high-quality data visualizations.

---

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Target Website](#-target-website)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Scraper Design & Implementation](#-scraper-design--implementation)
- [Data Analysis Summary](#-data-analysis-summary)
- [Data Visualizations](#-data-visualizations)
- [How to Setup and Run](#-how-to-setup-and-run)
- [LinkedIn Video Explanation Draft](#-linkedin-video-explanation-draft)

---

## 🌟 Project Overview
The goal of this task is to extract, structure, and analyze product information from a web catalog. The system consists of two major components:
1. **Web Scraper (`scraper.py`)**: Crawls a target site recursively category-by-category, extracting titles, prices, ratings, availability, and URLs.
2. **Data Analysis (`analyze.py`)**: Cleans the raw data, runs statistical computations (averages, distributions, limits), and outputs professional-grade visualization plots.

---

## 🎯 Target Website
We utilize **[Books to Scrape](http://books.toscrape.com/)**, a famous sandbox environment specifically created for practicing web scraping. It simulates a fully featured bookstore containing 1,000 books spread across 50 categories.

---

## 🛠️ Technology Stack
- **Python**: Core programming language.
- **Requests**: For managing HTTP session connections and retrieving pages.
- **BeautifulSoup4 & lxml**: For robust, fast HTML parsing and element extraction.
- **Pandas**: For organizing data structures, cleaning data, and running statistics.
- **Matplotlib & Seaborn**: For generating high-definition data charts.

---

## 📁 Project Structure
```text
Task 1/
│
├── requirements.txt            # Project dependencies
├── scraper.py                 # Core scraping engine
├── analyze.py                 # Core data analysis and visualization engine
├── books_dataset.csv          # Scraped dataset (CSV format)
├── books_dataset.json         # Scraped dataset (JSON format)
│
├── visualizations/            # Automatically generated charts
│   ├── price_distribution.png
│   ├── ratings_distribution.png
│   ├── categories_by_count.png
│   └── categories_by_price.png
│
└── README.md                  # Detailed documentation (This file)
```

---

## ⚙️ Scraper Design & Implementation
To scrape 1,000 books politely and efficiently:
1. **Polite Crawling**: We implemented a `0.1-second` request delay between pages to avoid placing an unnecessary load on the server.
2. **Category Traversal**: Instead of hitting all 1,000 book detail pages (which would take ~10 minutes and make 1,000 requests), we parse the main landing page, find the URL for each of the **50 categories**, and traverse the category listings. This reduced the requests to ~55-60 total, taking only **~15 seconds**!
3. **Robust Parsers**: 
   - Ratings are converted from textual classes (`One`, `Two`...) to numerical stars (`1-5`).
   - Prices are stripped of junk symbols (like `Â` or `£`) and converted to numeric values.
   - Text is trimmed and cleaned.

---

## 📊 Data Analysis Summary
Running `python analyze.py` outputs the following statistics on the console:

```text
==================================================
           BOOK DATASET STATISTICAL SUMMARY
==================================================
Total Books Scraped:      1000
Average Book Price:       £35.07
Median Book Price:        £35.98
Price Range:              £10.00 - £59.99
--------------------------------------------------
Rating Distribution:
  5 Star (*****): 196 books (19.6%)
  4 Star (****-): 179 books (17.9%)
  3 Star (***--): 203 books (20.3%)
  2 Star (**---): 196 books (19.6%)
  1 Star (*----): 226 books (22.6%)
--------------------------------------------------
Total Categories:         50

Top 10 Largest Categories:
  - Default             : 152 books
  - Nonfiction          : 110 books
  - Sequential Art      : 75 books
  - Add a comment       : 67 books
  - Fiction             : 65 books
  - Young Adult         : 54 books
  - Fantasy             : 48 books
  - Romance             : 35 books
  - Mystery             : 32 books
  - Food and Drink      : 30 books

Top 5 Most Expensive Categories (Average Price):
  - Suspense            : £58.33
  - Novels              : £54.81
  - Politics            : £53.61
  - Health              : £51.45
  - New Adult           : £46.38

Top 5 Cheapest Categories (Average Price):
  - Crime               : £10.97
  - Academic            : £13.12
  - Adult Fiction       : £15.36
  - Paranormal          : £15.40
  - Erotica             : £19.19
==================================================
```

---

## 📈 Data Visualizations
The analysis script saves premium charts inside the `visualizations/` folder:

1. **Price Distribution (`price_distribution.png`)**: A kernel density estimate (KDE) overlaid on a price histogram, showing that prices are uniformly distributed between £10 and £60.
2. **Ratings Distribution (`ratings_distribution.png`)**: A clean bar chart plotting rating counts, displaying a relatively uniform distribution with 1-star ratings being slightly more frequent.
3. **Categories by Count (`categories_by_count.png`)**: A horizontal bar chart mapping the top 15 categories by number of books, showing that *Default*, *Nonfiction*, and *Sequential Art* are the largest categories.
4. **Categories by Price (`categories_by_price.png`)**: A ranked horizontal bar chart mapping average book price per category, highlighting that *Suspense* is the most expensive category.

---

## 🚀 How to Setup and Run

### 1. Clone/Download the Workspace
Navigate into the `Task 1` directory:
```bash
cd "Task 1"
```

### 2. Install Dependencies
Run the package manager to install the libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Run the Scraper
Run the scraper script to fetch data from the web page and generate the CSV/JSON files:
```bash
python scraper.py
```
This will fetch category indexes and compile `books_dataset.csv` and `books_dataset.json` in the folder.

### 4. Run the Data Analysis
Run the analyzer script to process the data, print statistics, and output the visualization plots:
```bash
python analyze.py
```
This will output the summary to your terminal and create the charts inside the `visualizations/` directory.

