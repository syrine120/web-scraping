"""
BooksToScrape Web Scraper
This script scrapes book information (title, price, availability, rating)
from the BooksToScrape website (https://books.toscrape.com/) page by page
and prints the details in the terminal.
"""
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import json
BASE="https://books.toscrape.com/catalogue/"
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
rating_map = {
  "One": 1,
  "Two": 2,
  "Three": 3,
   "Four": 4,
   "Five": 5
    }
def scrape_page(url):
    """Scrape a single page of BooksToScrape and return (books, next_url)."""
    try:
      response = requests.get(url, headers=headers, timeout=10)
      response.raise_for_status()
    except requests.RequestException as e:
      print("Erreur réseau:", e)
      return [], None
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    results=[]
    for book in books:
        title = book.h3.a.get('title', '').strip()
        price_tag= book.find('p', class_='price_color')
        price = price_tag.text.replace('£', '').strip() if price_tag else "N/A"
        available_tag=book.find('p', class_='instock availability')
        availability = " ".join(available_tag.text.split()) if available_tag else "N/A"
        rating_tag=book.find('p', class_='star-rating')
        rating_str=rating_tag['class'][1] if rating_tag else "N/A"
        rating=rating_map.get(rating_str, 0)
        print(f"Titre: {title}")
        print(f"  Prix: £{price}")
        print(f"  Disponibilité: {availability}")
        print(f"  Note: {rating}")
        print("-" * 50)
        results.append({
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating
        })
    next_page = soup.find('li', class_='next')
    if next_page and next_page.a:
        next_href = next_page.a['href']
        next_url = urljoin(url, next_href) 
    else:
        next_url = None
    return results, next_url  
def main():
    url=BASE+"page-1.html"
    all_books = []
    page_count = 0
    while url:
        page_count+=1
        print(f"Scraping page {page_count}: {url}")
        books, url = scrape_page(url)
        if not books:
            print("Aucun livre trouvé ou une erreur s'est produite.")
            break
        for book in books:
            all_books.append(book)
        time.sleep(2)  # Pause de 2 secondes 
    print(f"Total books scraped: {len(all_books)}")
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(all_books, f, ensure_ascii=False, indent=4)
if __name__ == "__main__":
    main()