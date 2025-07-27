from datetime import datetime, timedelta
from airflow import DAG
import requests
import pandas as pd
from bs4 import BeautifulSoup
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

headers = {
    "Referer": 'https://www.amazon.com/',
    "Sec-Ch-Ua": "Not_A Brand",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# EXTRACT 

def get_amazon_data_books(num_books, ti):
    #base url
    base_url = f"https://www.amazon.com/s?k=data+engineering+books"

    books = []

    title_seen = set()

    page = 1

    while len(books) < num_books:
        url = f"{base_url}&page={page}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            book_containers = soup.find_alll("div",{"class":"s-result-item"})

            for book in book_containers:
                title = book.find("span", {"class": "a-text-normal"})
                author = book.find("a", {"class": "a-size-base"})
                price = book.find("span", {"class": "a-price-whole"})
                rating = book.find("span", {"class": "a-icon-alt"})

                if title and author and price and rating:
                    book_title = title.text.strip()

                    if book_title not in title_seen:
                        title_seen.add(book_title)
                        books.append({
                            "Title": book_title,
                            "Author" : author.text.strip(),
                            "Price" : price.text.strip(),
                            "Rating" : rating.text.strip()
                        })
            page += 1
        else:
            print("Failed to retrieve the page")
            break