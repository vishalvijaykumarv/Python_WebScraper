import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib3 import Retry
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from ConsoleLogger import ConsoleLogger

console_log = ConsoleLogger('console_log').logger


def convert_tags_to_list(soup_tag_list):
    console_log.debug(f"{__name__} => convert_tags_to_list ")
    text_data_list_from_soup = [one_item.text for one_item in soup_tag_list]
    clean_tags_list = [tag.strip() for tag in text_data_list_from_soup if tag.strip()]
    return clean_tags_list


def get_new_header():
    console_log.debug(f"{__name__} => get_new_header ")
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.OPERA.value,
                      SoftwareName.SAFARI.value, SoftwareName.EDGE.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    random_user_agent = user_agent_rotator.get_random_user_agent()
    headers = {"User-Agent": random_user_agent}
    return headers


def format_the_urls(urls_list, domain_name):
    console_log.debug(f"{__name__} => format_the_urls => {domain_name}  ")
    converted_urls = []
    for url in urls_list:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url if re.search(domain_name, url) else "https://" + domain_name + url
        elif url.startswith("http://"):
            url = url.replace("http://", "https://")
        if url == "/":
            converted_url = "https://" + domain_name
        elif url.startswith("/"):
            converted_url = "https://" + domain_name + url if len(url) > 1 else "https://" + domain_name
        else:
            url = "https://" + url if url.startswith("www.") else (
                "https://www." + url if not url.startswith("https://") else url)
            converted_url = url
        converted_urls.append(converted_url[:-1] if converted_url.endswith("/") else converted_url)
    return converted_urls


class Webscraper:
    def __init__(self, retry=1, timeout=2, tags_list=None):
        console_log.debug(f"{__name__} => __init__ => ")
        self.domain = None
        self.url = None
        self.page_size, self.response, self.soup_data, self.page_resp_code, self.elapsed_time, \
            = None, None, None, None, None
        self.tags_list = tags_list if tags_list is not None else ['h1', 'h2', 'title']  # Default tags_list
        self.retry = retry
        self.timeout = timeout
        self.session = requests.Session()
        retries = Retry(total=self.retry, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def download_url(self, url=None):
        """
        :param url: only one url at a time,
        :return:  if url have response then return the bs4 soup object else return None
        """
        self.url = url if url is not None else self.url
        console_log.info(f'Running {self.url}')
        console_log.debug(f"{__name__} => download_url => {self.url}  ")
        try:
            self.domain = urllib.parse.urlparse(self.url).netloc
            self.response = self.session.get(self.url, timeout=self.timeout, headers=get_new_header())
            self.soup_data = BeautifulSoup(self.response.content, "html.parser")
            self.elapsed_time = "{:.2f}".format(float(self.response.elapsed.total_seconds()))
            self.page_resp_code = self.response.status_code
            return self.soup_data, self.page_resp_code
        except Exception as exception:
            console_log.warning(f'Exception found => {self.url}  ')
            console_log.debug(f"{exception}   Check {self.url} manually with browser  ")
            return None, None

    def get_html_tags(self, soup_data=None, tags_list=None):
        """
        :param soup_data:   any urls request response will be the input
        :param tags_list:  what type of data we need to extract from the html
        :return: a dict with the tags & their data
        """
        console_log.debug(f"{__name__} => get_html_tags => {self.url}  ")
        self.soup_data = soup_data if soup_data is not None else self.soup_data
        self.tags_list = tags_list if tags_list is not None else self.tags_list
        output_dict = {}
        for tag in self.tags_list:
            try:
                output_dict[tag] = convert_tags_to_list(self.soup_data.find_all(tag))
            except Exception as exception:
                console_log.warning(f'Exception found => {self.url}   {exception}')
                pass
        try:
            self.elapsed_time = "{:.2f}".format(float(self.response.elapsed.total_seconds()))
            self.page_resp_code = self.response.status_code
            self.page_size = len(self.soup_data.get_text().encode("utf-8"))
            output_dict.update({'page_size': self.page_size})
            output_dict.update({'page_resp_code': self.page_resp_code})
            output_dict.update({'elapsed_time': self.elapsed_time})
        except Exception as exception:
            console_log.warning(f'Exception found => {self.url}   {exception}')
            pass
        return output_dict

    def get_links(self, url=None, soup_data=None):
        """
        // clean urls, only from the given domain
        :param soup_data: for extracting the href links
        :param url: for filter the href links based on the given url
        :return: a list of urls with `https://` + `domain_name` + ( if any subdirectory )
        """
        console_log.debug(f"{__name__} => get_links => {self.url}  ")
        self.url = url if url is not None else self.url
        self.soup_data = soup_data if soup_data is not None else self.soup_data
        try:
            href_links = self.soup_data.find_all('a')
            internal_links_list = [one_link.get('href') for one_link in href_links if one_link.get('href') is not None]
            format_urls = format_the_urls(internal_links_list, self.domain)
            clean_urls = [one_url for one_url in format_urls if self.domain in one_url]
            return clean_urls
        except Exception as exception:
            console_log.warning(
                f'Exception found => {self.url}   {exception}   Check the url manually with browser  ')
            return None
