import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/page-{}.html"

books_data = []

# Scrape first 5 pages (you can increase this number)
for page in range(1, 6):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    books = soup.find_all("article", class_="product_pod")
    
    for book in books:
        title_tag = book.find("h3").find("a")
        title = title_tag["title"].strip() if title_tag else "N/A"
        
        price_tag = book.find("p", class_="price_color")
        price = price_tag.text.strip() if price_tag else "N/A"
        
        rating_tag = book.find("p", class_="star-rating")
        rating = rating_tag["class"][1] if rating_tag else "N/A"
        
        link = "http://books.toscrape.com/catalogue/" + title_tag["href"] if title_tag else "N/A"
        
        books_data.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Link": link
        })

# Save to Excel
df = pd.DataFrame(books_data)
df.to_excel("books_data.xlsx", index=False)

print("✅ Books scraped and saved to 'books_data.xlsx'")
