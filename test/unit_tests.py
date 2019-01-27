#!/usr/bin/python3

# This is completly unfinished

from lxpapi import LxpApi       # local imports

if __name__ == '__main__':
    from utils import Logger
    base_url = 'https://sandbox.letterxpress.de/v1/'
    user_name = 'winfried.simon@gmail.com'
    api_key = 'a96ff7f4c77fb961cdcb8f1f8572250446bb571c'

    logger = Logger(verbose=True)
    lxpApi = LxpApi(base_url, user_name, api_key, logger=logger)
    balance = lxpApi.get_balance()
    deljob = lxpApi.delete_job(3394)

    pass