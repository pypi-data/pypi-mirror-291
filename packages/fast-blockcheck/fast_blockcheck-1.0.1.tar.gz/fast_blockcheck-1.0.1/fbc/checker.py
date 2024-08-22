import datetime
import logging
import random

import requests
import urllib3

from fbc.format import format_time


def run_block_check(urls: list[str], timeout: int, shuffle: bool) -> int:
    """
    Run full test iteration
    :param urls: URLs to check
    :param timeout: request timeout
    :param shuffle: whether to shuffle urls
    :return: number of successfully (HTTP < 400) accessed entries
    """
    number_of_successful = 0
    total_number = len(urls)

    if shuffle:
        random.shuffle(urls)
    start_time = format_time(datetime.datetime.now())
    print(f"{start_time}: starting test")

    for url in urls:
        r = test_url_availability(url, timeout)
        number_of_successful += int(r)

    print(f"{number_of_successful}/{total_number} domains loaded")
    return number_of_successful


def test_url_availability(url: str, timeout: int = 5) -> bool:
    """
    Check if URL is available
    :param url:
    :param timeout:
    :return: True, if HTTP status code is < 400
    """
    try:
        response = requests.get(url, timeout=timeout)
        status_code = response.status_code
        success = response.ok

    except requests.exceptions.ConnectionError as e:
        success = False

        if (isinstance(e.args[0], urllib3.exceptions.ReadTimeoutError) or
                isinstance(e.args[0], requests.exceptions.ReadTimeout)):
            status_code = "TIME"
        else:
            # any other ConnectionError
            status_code = "ERR"
            logging.debug(e.args[0])
            logging.debug(type(e.args[0]))

    receive_time = datetime.datetime.now()
    time_label = format_time(receive_time)
    print(f"{time_label}: ({status_code}) {url}")
    return success
