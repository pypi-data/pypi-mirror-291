import time

from fbc.checker import run_block_check


def fast_blockcheck(urls: list[str], timeout: int, shuffle: bool, repeat: int):
    """
    Monitor URLs availability
    :param urls: URLs to test
    :param timeout: request timeout in seconds
    :param shuffle: whether to shuffle URLs each iteration
    :param repeat: repeat interval in minutes, 0 to run only once
    """
    while True:
        run_block_check(urls, timeout=timeout, shuffle=shuffle)
        if not repeat:
            break
        else:
            print(f"Waiting for {repeat}min to repeat")
            time.sleep(60 * repeat)
