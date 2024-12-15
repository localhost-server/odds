from bs4 import BeautifulSoup
import requests
import logging
from tenacity import retry, stop_after_attempt, wait_fixed, wait_random, after_log

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(10), wait=wait_fixed(5) + wait_random(0, 1), after=after_log(logger, logging.DEBUG), retry_error_callback = lambda retry_state: None)
def get(url, xhr = False):
    logger.debug(f'GET {url}')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    if xhr:
        headers = {'User-Agent': user_agent, 'referer': 'https://www.oddsportal.com/', 'x-requested-with': 'XMLHttpRequest'}
    else:
        headers = {'User-Agent': user_agent, 'referer': 'https://www.oddsportal.com/'}
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    return res.text
