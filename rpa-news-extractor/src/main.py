import os
import sys
import logging
from datetime import datetime, timedelta
from RPA.Robocorp.WorkItems import WorkItems
from scraper import ReutersScraper

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Load work item variables
    work_items = WorkItems()
    work_items.get_input_work_item()
    search_phrase = work_items.get_work_item_variable('search_phrase')
    news_category = work_items.get_work_item_variable('news_category')
    months = int(work_items.get_work_item_variable('months'))

    # Calculate the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)

    # Initialize the scraper
    scraper = ReutersScraper(search_phrase, news_category, start_date, end_date)

    # Perform the scraping
    news_data = scraper.scrape()

    # Save the results to an Excel file
    output_file = os.path.join('output', 'news_data.xlsx')
    scraper.save_to_excel(news_data, output_file)

    # Mark the work item as completed
    work_items.complete_work_item()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)