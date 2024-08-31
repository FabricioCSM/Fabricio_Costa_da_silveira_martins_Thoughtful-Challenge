# RPA News Scraper

This is the project for the Thoutful AI chalenge, is an RPA process to extract news data based on a search phrase, news category, and date range. In the end, the data is saved to an Excel file.

## Setup

1. Clone the repository

2. Create a virtual environment and install dependencies:
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Create a `requirements.txt` file with the following content:
    beautifulsoup4==4.9.3
    openpyxl==3.0.7
    requests==2.25.1
    rpaframework==10.6.0

## Running the Project

1. Ensure you have the Robocorp CLI installed and configured.
2. Run the main script:
    ```bash
    python src/main.py
    ```

## Parameters

The script processes the following parameters via a Robocloud work item:
- `search_phrase`: The phrase to search for.
- `news_category`: The news category or section to filter by.
- `months`: The number of months for which to receive news.

## Output

The output is saved to an Excel file in the `output` directory with the following columns:
- Title
- Date
- Description
- Image Filename
- Phrase Count
- Contains Money