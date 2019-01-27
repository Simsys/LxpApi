import datetime                 # standard library imports
import os
import json
import base64
import hashlib
from pathlib import PurePath

import requests                 # additional library imports

class LxpApi():
    def __init__(self, base_url, user_name, api_key, logger=None, catch_exceptions=False):
        """Realizes the LetterXpress API v1 https://www.letterxpress.de/dokumentation/api
        
        Parameters:
            base_url (str): Url of the print service
            user_name (str): Name of user
            api_key (str): API key of the print service (see documentation)
            logger (obj): Logging of processing and error messages (see unit tests or cli)
            catch_exceptions (bool): If True: errors are intercepted and commented on
        """
        if base_url[-1] != '/':
            base_url += '/'
        self._base_url = base_url
        self._user_name = user_name
        self._api_key = api_key
        self._logger = logger
        self._catch_exceptions = catch_exceptions

    def get_balance(self):
        """Get balance information (see API documentation)

        Returns:
            dict: Balance information
        """
        return self._request('get', 'getBalance')

    def get_price(self, pages, color, mode, ship, c4=None):
        """Get price information (see API documentation)
        
        Parameters:
            pages (int): Pages of the document
            color (int): Color or black/white print (collor is 1 or 4)
            mode (str): Mode of printing (simplex or duplex)
            ship (str): Shipping national or international
            c4 (str): C4 Mailing bag

        Returns:
            dict: Price information
        """
        letter = {}
        letter['specification'] = {'page': pages, 'color': color, 'mode': mode, 'ship': ship}
        if c4 is not None:
            letter['specification']['c4'] = c4
        return self._request('get', 'getPrice', {'letter': letter})

    def get_jobs(self, job_type='queue', days=0):
        """Get list of jobs

        Parameters:
            job_type (str): Define type of jobs (queue, hold, sent, timer)
            days (int): Show onliy jobs of last days (queue, sent)

        Returns:
            dict: List of jobs
        """
        if job_type in ('queue', 'sent'):
            sub_url = "getJobs/%s/%d" % (job_type, days)
        else:
            sub_url = "getJobs/%s" % job_type
        return self._request('get', sub_url)

    def get_job(self, id):
        """Get single job selected by id

        Parameters:
            id (int): Id of the job

        Returns:
            dict: Job information
        """
        sub_url = "getJob/%d" % id
        return self._request('get', sub_url)

    def set_job(self, file_path, color=1, mode='simplex', ship='national', dispatch_date=None):
        """Upload PDF file to print service

        Parameters:
            file_path (str): Path to PDF file
            color (int): Color or black/white print (collor is 1 or 4)
            mode (str): Mode of printing (simplex or duplex)
            ship (str): Shipping national or international
            dispatch_date (datetime): Date, when to dispatch

        Returns:
            dict: Job information
        """
        letter = {}
        with open(file_path, "rb") as pdf_file:
            b64 = base64.b64encode(pdf_file.read())
            md5 = hashlib.md5()
            md5.update(b64)
            letter['base64_checksum'] = md5.hexdigest()
            letter['base64_file'] = b64.decode("utf-8")
        letter['address'] = PurePath(file_path).name
        if dispatch_date is not None:                                   # Dispatch date is optional
            letter['dispatchdate'] = dispatch_date.strftime('%d.%m.%Y')
        letter['specification'] = {'color': color, 'mode': mode, 'ship': ship}
        return self._request('post', 'setJob', {'letter': letter})

    def update_job(self, id, color=1, mode='simplex', ship='national', dispatch_date=None):
        """Update (change) job attributes

        Parameters:
            id (int): Id of job
            color (int): Color or black/white print (collor is 1 or 4)
            mode (str): Mode of printing (simplex or duplex)
            ship (str): Shipping national or international
            dispatch_date (datetime): Date, when to dispatch

        Returns:
            dict: Job information
        """
        sub_url = "updateJob/%d" % id
        letter = {}
        if dispatch_date is not None:                                   # Dispatch date is optional
            letter['dispatchdate'] = dispatch_date.strftime('%d.%m.%Y')
        letter['specification'] = {'color': color, 'mode': mode, 'ship': ship}
        return self._request('put', sub_url, {'letter': letter})

    def delete_job(self, id):
        """Delete single job selected by id

        Parameters:
            id (int): Id of the job

        Returns:
            dict: Process information
        """
        sub_url = "deleteJob/%d" % id
        return self._request('delete', sub_url)

    def list_invoices(self):
        """Get all invoices

        Returns:
            dict: List of all invoices
        """
        return self._request('get', 'listInvoices')

    def get_invoice(self, id):
        """Get invoice

        Returns:
            dict: Invoice information
        """
        sub_url = "getInvoice/%d" % id
        return self._request('get', sub_url)

    # The following methods are private and not part of the official API
    def _request(self, *args, **kwargs):
        if self._catch_exceptions:
            result = None
            try:
                result = self._pure_request(*args, **kwargs)
            except requests.RequestException as err:
                self._log('error', 'Invalid Url "%s"' % err)
            except json.decoder.JSONDecodeError as err:
                self._log('error', 'Wrong Url "%s"' % err)
        else:
            result = self._pure_request(*args, **kwargs)
        
        return result

    def _pure_request(self, method, sub_url, data={}):
        url = self._base_url + sub_url
        data['auth'] = {"apikey": self._api_key, "username": self._user_name}
        self._log('verbose', '%s %s' % (method, url))
        self._last_response = requests.request(method, url, data=json.dumps(data))
        result = self._last_response.json()
        self._log('verbose', 'Status %d %s' % (result['status'], result['message']))
        return(result)

    def _log(self, method, msg):
        if self._logger is not None:
            flog = getattr(self._logger, method)
            flog(msg)
