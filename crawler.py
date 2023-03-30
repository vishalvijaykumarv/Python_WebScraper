from WebScraper import *
import pandas as pd
import time
import threading
import sys
import hashlib


def que_func(one_url, count):
    scraper.download_url(one_url)
    one_url_data = scraper.get_html_tags()
    new_links = scraper.get_links()
    url_list.extend(new_links)
    one_url_data.update({'url': one_url})       # Manually updating the running url with the one_url_data dict
    output_site_data.append(one_url_data)       # keep all one_url_data dict into 1 specified list , for dataframe
    count += 1
    return new_links


def process_urls():
    """
    :return:  this function return nothing, it's used to update the url_list with new urls &
    run entire process in while loop based on any 3 conditions
    """
    global data_count, processed_urls_count, url_list, processed_urls_list, output_site_data

    try:
        url_list = [sys.argv[1]]
    except Exception as exception:
        url_list = ["https://realpython.github.io/fake-jobs/"]  # you can manually change this url for test
        console_log.info(f'No URL Found from user, Starting the process with default list {url_list}')
        console_log.debug(f"No URL from the user\n {exception} ")
        pass

    while data_count <= limit or limit == 0 or data_count != processed_urls_count:
        try:
            s_one_url = url_list.pop(0)
            result = que_func(s_one_url, data_count)
            console_log.debug(f"Current length for the url_list: {len(url_list)} data_count : {data_count} "
                              f"processed_urls_count : {processed_urls_count} ")
            hashed_url = hashlib.sha256(s_one_url.encode()).hexdigest()
            url_list.extend([value for value in result if value not in processed_urls_list and value not in url_list])
            if hashed_url not in processed_urls_list:
                processed_urls_list.append(hashed_url)
            data_count += 1
            processed_urls_count += 1
        except Exception as exception:
            console_log.info(f'No more urls left in queue \n {exception}')
            break


if __name__ == '__main__':
    start_time = time.time()
    """
    From the user `input url` is Taken from `process_urls` function // Due to `process_urls` is running with Threads
    `limit` needs to be given from user end 
    if user needs extra tags from the urls they can pass `tags_list` while Initialize `Webscraper` class
    also retry & timeout you can pass it's optional by default it's retry=1, timeout=2 
    eg:  scraper = Webscraper(tags_list=['h1','h3','h4'])
    """
    # `0` for unlimited crawling ;)
    limit = 1000

    url_list = []               # Initialize Empty storage for all urls
    processed_urls_list = []    # This list will be stored processed urls after crawling
    output_site_data = []       # After crawling the tags data will be stored here
    threads = []                # used to store all Threads
    thread_count = 4            # how many thread user want .?
    data_count = 0              # used for while loop to compare with user limit
    processed_urls_count = 0    # used for while loop to compare with data_count ( if no new urls scenario )
    scraper = Webscraper()      # Initialize Webscraper class

    # ---------------------------------- starting point -----------------------------------------------------
    for i in range(int(thread_count)):  # create n number of threads
        t = threading.Thread(target=process_urls)  # Thread target function config
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # ---------------------------------- Output writing  -----------------------------------------------------

    data_only_df = pd.DataFrame(output_site_data, dtype=str)
    data_only_df = data_only_df.drop_duplicates(subset=['url'])  # removing duplicate data based on url column
    data_only_df.to_csv(f'data_{len(output_site_data)}_{str(time.time())}.csv', index=False)
    end_time = time.time()
    total_time = end_time - start_time
    console_log.info(f"Total running time: {total_time:.2f} seconds")
