import os
from robocorp.tasks import task, get_output_dir
from robocorp import log
from RPA.Robocorp.WorkItems import WorkItems
from scraper import NewsScraper

@task
def main():
    work_items = WorkItems()
    work_items.get_input_work_item()
    search_phrase = work_items.get_work_item_variable("search_phrase")
    news_category = work_items.get_work_item_variable("news_category")
    months = work_items.get_work_item_variable("months") scraper = NewsScraper(search_phrase, news_category, months)

    scraper.run() work_items.save_work_item()
    work_items.release_input_work_item()
    
if __name__ == "__main__":
    main()