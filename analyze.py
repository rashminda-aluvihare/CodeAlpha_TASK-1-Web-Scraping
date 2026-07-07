import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(csv_path):
    """Loads the book dataset from CSV."""
    if not os.path.exists(csv_path):
        print(f"Error: Dataset file '{csv_path}' not found.")
        return None
    return pd.read_csv(csv_path)

def analyze_dataset(df):
    """Prints key statistics of the dataset."""
    total_books = len(df)
    avg_price = df['price'].mean()
    min_price = df['price'].min()
    max_price = df['price'].max()
    median_price = df['price'].median()
    
    print("\n" + "="*50)
    print("           BOOK DATASET STATISTICAL SUMMARY")
    print("="*50)
    print(f"Total Books Scraped:      {total_books}")
    print(f"Average Book Price:       £{avg_price:.2f}")
    print(f"Median Book Price:        £{median_price:.2f}")
    print(f"Price Range:              £{min_price:.2f} - £{max_price:.2f}")
    print("-"*50)
    
    # Rating Distribution
    print("Rating Distribution:")
    rating_counts = df['rating'].value_counts().sort_index(ascending=False)
    for rating, count in rating_counts.items():
        stars = "*" * int(rating) + "-" * (5 - int(rating))
        percentage = (count / total_books) * 100
        print(f"  {rating} Star ({stars}): {count} books ({percentage:.1f}%)")
    print("-"*50)

    # Categories Summary
    categories = df['category'].nunique()
    print(f"Total Categories:         {categories}")
    print("\nTop 10 Largest Categories:")
    cat_counts = df['category'].value_counts().head(10)
    for cat, count in cat_counts.items():
        print(f"  - {cat:<20}: {count} books")
    
    print("\nTop 5 Most Expensive Categories (Average Price):")
    expensive_cats = df.groupby('category')['price'].mean().sort_values(ascending=False).head(5)
    for cat, avg_p in expensive_cats.items():
        print(f"  - {cat:<20}: £{avg_p:.2f}")
        
    print("\nTop 5 Cheapest Categories (Average Price):")
    cheapest_cats = df.groupby('category')['price'].mean().sort_values().head(5)
    for cat, avg_p in cheapest_cats.items():
        print(f"  - {cat:<20}: £{avg_p:.2f}")
    print("="*50)

def generate_visualizations(df, output_dir="visualizations"):
    """Generates and saves premium data visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")
    
    # Palette definition for cohesive look
    primary_color = "#4C6EF5"  # Modern royal/indigo blue
    accent_color = "#FAB005"   # Warm yellow for stars
    
    # 1. Price Distribution Histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], kde=True, color=primary_color, bins=30, line_kws={"linewidth": 2.5})
    plt.title("Distribution of Book Prices", pad=20, fontsize=16, fontweight='bold')
    plt.xlabel("Price (£)", labelpad=10)
    plt.ylabel("Number of Books", labelpad=10)
    plt.tight_layout()
    price_dist_path = os.path.join(output_dir, "price_distribution.png")
    plt.savefig(price_dist_path, dpi=300)
    plt.close()
    print(f"Generated plot: {price_dist_path}")

    # 2. Rating Count Distribution (Bar Chart)
    plt.figure(figsize=(8, 5))
    rating_data = df['rating'].value_counts().sort_index()
    # Create rating label with stars for aesthetics
    labels = [f"{r} Star\n" + "*"*r for r in rating_data.index]
    
    bars = plt.bar(labels, rating_data.values, color="#F59F00", width=0.6, edgecolor="#E67E22", linewidth=1.2)
    # Add count values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 3, str(yval), ha='center', va='bottom', fontsize=12, fontweight='bold')
        
    plt.title("Distribution of Star Ratings", pad=20, fontsize=16, fontweight='bold')
    plt.xlabel("Rating Category", labelpad=10)
    plt.ylabel("Number of Books", labelpad=10)
    plt.ylim(0, max(rating_data.values) * 1.15)
    plt.tight_layout()
    rating_dist_path = os.path.join(output_dir, "ratings_distribution.png")
    plt.savefig(rating_dist_path, dpi=300)
    plt.close()
    print(f"Generated plot: {rating_dist_path}")

    # 3. Top 15 Categories by Book Count
    plt.figure(figsize=(12, 8))
    cat_order = df['category'].value_counts().head(15).index
    sns.countplot(data=df[df['category'].isin(cat_order)], y='category', order=cat_order, hue='category', palette="viridis", legend=False)
    plt.title("Top 15 Categories by Book Count", pad=20, fontsize=16, fontweight='bold')
    plt.xlabel("Number of Books", labelpad=10)
    plt.ylabel("Category", labelpad=10)
    plt.tight_layout()
    cat_count_path = os.path.join(output_dir, "categories_by_count.png")
    plt.savefig(cat_count_path, dpi=300)
    plt.close()
    print(f"Generated plot: {cat_count_path}")

    # 4. Average Price per Category (Top 15 Categories)
    plt.figure(figsize=(12, 8))
    avg_prices = df.groupby('category')['price'].mean().sort_values(ascending=False).head(15)
    sns.barplot(x=avg_prices.values, y=avg_prices.index, hue=avg_prices.index, palette="mako", legend=False)
    # Add average price labels on the bars
    for i, val in enumerate(avg_prices.values):
        plt.text(val + 0.5, i, f"£{val:.2f}", va='center', fontsize=11, fontweight='semibold')
        
    plt.title("Top 15 Most Expensive Categories (Average Price)", pad=20, fontsize=16, fontweight='bold')
    plt.xlabel("Average Price (£)", labelpad=10)
    plt.ylabel("Category", labelpad=10)
    plt.xlim(0, max(avg_prices.values) * 1.12)
    plt.tight_layout()
    cat_price_path = os.path.join(output_dir, "categories_by_price.png")
    plt.savefig(cat_price_path, dpi=300)
    plt.close()
    print(f"Generated plot: {cat_price_path}")

if __name__ == "__main__":
    csv_file = "books_dataset.csv"
    data = load_data(csv_file)
    if data is not None:
        analyze_dataset(data)
        generate_visualizations(data)
        print("\nVisualizations saved to 'visualizations/' folder.")
