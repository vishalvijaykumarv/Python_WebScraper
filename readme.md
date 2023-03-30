# Webscraper
This is a Python web scraper designed to crawl and extract data from a given website.

## Installation
1. Clone the repository
2. Install the required packages by running pip install -r requirements.txt
3. Run the crawler.py file to start the scraper
## Usage
The scraper takes in a list of URLs to crawl and a limit on the number of URLs to process.

There are also a few additional parameters that can be configured:

* `tags_list` (optional): A list of HTML tags to extract data from (e.g. ['h1', 'h2', 'p'])
* `retry` (optional): The number of times to retry a failed request (default: 1)
* `timeout` (optional): The timeout for each request in seconds (default: 2)
## Variables
The following variables are used in the scraper:

* limit: The maximum number of URLs to process (set to 0 for unlimited)
* url_list: An empty list to store all the URLs to be processed
* processed_urls_list: A list to store processed URLs after crawling
* output_site_data: A list to store the extracted data from each URL
* threads: A list to store all threads used in the scraper
* thread_count: The number of threads to use in the scraper (default: 4)
* data_count: A counter variable used in the while loop to compare with the user limit
* processed_urls_count: A counter variable used in the while loop to compare with the data count (in case of no new URLs scenario)
* scraper: An instance of the Webscraper class
## Input
The user provides a list of URLs to crawl as an input to the `process_urls` function. This is necessary as process_urls runs with threads.

Additionally, the user must specify the `limit` parameter to indicate the maximum number of URLs to process.

If the user wants to extract data from specific HTML tags, they can pass a `tags_list` parameter while initializing the Webscraper class.

### Example
Here's an example of initializing the `Webscraper` class with a `tags_list` parameter:

`scraper = Webscraper(tags_list=['h1', 'h3', 'h4'])`
This would extract data only from the h1, h3, and h4 tags.

### Future Improvements
* Allow the scraper to crawl pages that require authentication
* Improve the error handling to prevent the scraper from crashing in case of a failed request
* Add more options for extracting data (e.g. extract text based on CSS selectors)
* implement elastic search for store the data 