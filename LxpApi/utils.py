from pathlib import Path                # standard library imports
from configparser import ConfigParser
import sys

import keyring                          # additional library imports
import click

from .lxpapi import LxpApi               # local imports

VERSION = '0.0.3'
NAME = 'lxpservice'

class Logger():
    def __init__(self, verbose=False):
        '''Handle Log Messages

        verbose: if True print all messegas 
        '''
        self._verbose = verbose

    def setVerbose(self, verbose):
        self._verbose = verbose

    def info(self, msg):
        click.echo(msg)

    def error(self, msg):
        txt = 'Error: ' + msg
        click.echo(txt, err=True)

    def verbose(self, msg):
        if self._verbose:
            click.echo(msg)


def access(logger, delete=None, user=None, url=None, apikey=None, verbose=True):
    config = ConfigParser()
    ini_file = Path.home() / '.lxpapi.ini'
    if ini_file.is_file():
        config.read(ini_file)

    if not 'credentials' in config:
        config['credentials'] = {'user': '', 'url': ''}
    if not 'user' in config['credentials']:
        config['credentials']['user'] = ''
    if not 'url' in config['credentials']:
        config['credentials']['url'] = ''

    if user is None:
        user = config['credentials']['user']
    else:
        config['credentials']['user'] = user
    if url is None:
        url = config['credentials']['url']
    else:
        config['credentials']['url'] = url

    with open(ini_file, 'w') as f:
        config.write(f)

    key = user + '@' + url
    if delete:
        try: 
            keyring.delete_password('lxpapi', key)
            logger.info('lxpapi key deleted')
        except:
            pass
    else:
        if apikey is None:    
            apikey = keyring.get_password('lxpapi', key)
        else:
            keyring.set_password('lxpapi', key, apikey)


    logger.info('User %s' % user)
    logger.info('Url %s' % url)

    lxpApi = LxpApi(url, user, apikey, logger, True)

    try:
        msg = lxpApi.get_balance()
    except:
        logger.error('No access')
        sys.exit(1)

    if msg['status'] != 200:
        logger.error(msg['message'])
        sys.exit(1)

    return lxpApi
