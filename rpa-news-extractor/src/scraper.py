import os
import re
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from openpyxl import Workbook
from RPA.Browser.Selenium import Selenium

class ReutersScraper:
    def __init__(self, search_phrase, news_category, start_date, end_date):
        self.search_phrase = search_phrase
        self.news_category = news_category
        self.start_date = start_date
        self.end_date = end_date
        self.browser = Selenium()
        self.browser.open_available_browser('https://www.reuters.com/')

    def scrape(self):
        logging.info("Starting the scraping process")
        # Click the "Open search bar" button
        self.browser.click_button('aria-label:Open search bar')
        # Enter the search phrase in the input field
        self.browser.input_text('data-testid:FormField:input', self.search_phrase)
        # Click the search button to initiate the search
        self.browser.click_button('aria-label:Search')

        # Wait for the search results to load
        self.browser.wait_until_element_is_visible('css:ul.search-results__list__2SxSK')

        news_data = []
        articles = self.browser.find_elements('css:li.search-results__item__2oqiX')
        for article in articles:
            title_element = article.find_element_by_css_selector('a[data-testid="Title"] span[data-testid="Heading"]')
            title = title_element.text
            date_element = article.find_element_by_css_selector('time[data-testid="Text"]')
            date = date_element.get_attribute('datetime')
            description_element = article.find_element_by_css_selector('div.basic-card__body__2ZzGC > span[data-testid="Label"]')
            description = description_element.text if description_element else ""
            image_element = article.find_element_by_css_selector('div[data-testid="Image"] img')
            image_url = image_element.get_attribute('src') if image_element else ""

            # Check if the article falls within the date range
            article_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            if not (self.start_date <= article_date <= self.end_date):
                continue

            # Download the image
            image_filename = self.download_image(image_url)

            # Count search phrases in title and description
            phrase_count = title.lower().count(self.search_phrase.lower()) + description.lower().count(self.search_phrase.lower())

            # Check for monetary values
            contains_money = bool(re.search(r'\$\d+(\.\d{1,2})?|(\d+,\d{3})+(\.\d{1,2})?|\d+ dollars|\d+ USD', title + description))

            news_data.append({
                'title': title,
                'date': date,
                'description': description,
                'image_filename': image_filename,
                'phrase_count': phrase_count,
                'contains_money': contains_money
            })

        self.browser.close_browser()
        return news_data

    def download_image(self, url):
        response = requests.get(url)
        filename = os.path.join('output', os.path.basename(url))
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename

    def save_to_excel(self, data, filename):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(['Title', 'Date', 'Description', 'Image Filename', 'Phrase Count', 'Contains Money'])
        for item in data:
            sheet.append([
                item['title'],
                item['date'],
                item['description'],
                item['image_filename'],
                item['phrase_count'],
                item['contains_money']
            ])
        workbook.save(filename)
        logging.info(f"Data saved to {filename}")