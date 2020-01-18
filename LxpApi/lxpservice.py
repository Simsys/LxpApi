#!/usr/bin/python3

import fnmatch              # standard library imports
import os
from pathlib import Path

import click                # additional library imports

from . import utils         # local imports

logger = utils.Logger()

@click.group()
@click.version_option(version=utils.VERSION, prog_name=utils.NAME)
@click.option('-v', '--verbose', is_flag=True, default=False, help='Be communicative.')
def lxpservice(verbose=False, version=False):
    """Command line tool to manage LetterXpress print jobs.

    With this tool credentials can be managed, print jobs can be activated, monitored and deleted.

    See https://www.letterxpress.de
    """
    logger.setVerbose(verbose)


@lxpservice.command('credentials')
@click.option('-d', '--delete', is_flag=True, default=False, help='Deletes password (requires user and url).')
@click.argument('user', required=False)
@click.argument('url', required=False)
@click.argument('apikey', required=False)
def credentials(delete, user, url, apikey):
    """Create and maintain credentials.

    The login data consists of user, url and api key. If all three parameters are specified, lxpapi stores them securely and uses 
    them in the future. If only user and url are specified, lxpapi loads the api key from the password repository of the operating 
    system. If only user is specified, lxapi changes the user, keeps the url and loads the api key from the password repository.
    """
    utils.access(logger, delete, user, url, apikey)


@lxpservice.command('status')
def status():
    """Check the status of the placed print jobs.

    A distinction is made between jobs covered by the credit balance and jobs not covered.
    """
    lxpApi = utils.access(logger)
    def print_jobs(jobs, comment):
        if jobs['status'] == 200:
            logger.info(comment)
            logger.info('%-20s %6s %3s %3s %4s %-35s' % ('Date', 'Id', 'Pgs', 'Col', 'Cost', 'Filename'))
            for idx in jobs['jobs']:
                job = jobs['jobs'][idx]
                cost = float(job['cost']) + float(job['cost_vat'])
                logger.info('%-20s %6s %3s %3s %4.2f %-35s' % 
                     (job['date'], job['jid'], job['pages'], job['color'], cost, job['address'][0:35]))
        elif jobs['status'] == 404:
            logger.info("%s\n  <%s>" % (comment, jobs['message']))

    hold_jobs = lxpApi.get_jobs('hold')
    print_jobs(hold_jobs, '\nThese letters are in the queue (credit exhausted):')
    queue_jobs = lxpApi.get_jobs('queue')
    print_jobs(queue_jobs, '\nThese letters will be sent soon:')
    

@lxpservice.command('send')
@click.option('-c', '--color', is_flag=True, default=False, help='Send colored Letters.')
@click.option('-i', '--international', is_flag=True, default=False, help='Send letters to international destinations.')
@click.option('-d', '--duplex', is_flag=True, default=False, help='Send double sided printed letters.')
@click.argument('file_or_directory', type=click.Path(exists=True))
def send(color, international, duplex, file_or_directory):
    """Send PDF files to print service.

    Either individual files or the PDF files of a directory can be transferred. Different options can be selected. 
    """
    if color:
        color = 4
    else:
        color = 1
    if duplex:
        mode = 'duplex'
    else:
        mode = 'simplex'
    if international:
        ship = 'international'
    else:
        ship = 'national'

    lxpApi = utils.access(logger)
    files_to_be_sent = []
    if os.path.isfile(file_or_directory):
        files_to_be_sent.append(Path(file_or_directory))
    else:
        files = os.listdir(file_or_directory)
        for name in files:
            if fnmatch.fnmatch(name.lower(), '*.pdf'):
                files_to_be_sent.append(Path(file_or_directory) / name)

    logger.info('\nSending file(s) to print server...')
    for fname in files_to_be_sent:
        lxpApi.set_job(fname, color, mode, ship)
        logger.info('  ' + fname.name)


@lxpservice.command('delete')
@click.option('-i', '--id', default=0, help='Delete a single order.')
@click.option('-a', '--all', is_flag=True, default=False, help='Delete all jobs.')
def delete(id, all):
    """Delete job(s).

    Delete a job identified by the id or delete all jobs of the print service.
    """
    lxpApi = utils.access(logger)

    pdf_files = {}                          # We need this only to know the file names
    def add_group_to_pdf_files(group):
        jobs = lxpApi.get_jobs(group)
        if jobs['status'] == 200:
            for idx in jobs['jobs']:
                jid = int(jobs['jobs'][idx]['jid'])
                fname = jobs['jobs'][idx]['address']
                pdf_files[jid] = fname
    add_group_to_pdf_files('hold')
    add_group_to_pdf_files('queue')

    jobs_to_delete = []                     # In this list we store the ids of jobs to delete
    def add_group_to_delete(group):
        jobs = lxpApi.get_jobs(group)
        if jobs['status'] == 200:
            for idx in jobs['jobs']:
                jobs_to_delete.append(int(jobs['jobs'][idx]['jid']))
    if id > 0:
        jobs_to_delete.append(id)
    elif all:
        add_group_to_delete('hold')
        add_group_to_delete('queue')

    if len(jobs_to_delete) == 0:
        logger.info('\nNothing to delete')
    else:
        logger.info('\nDeleting order(s):')
        for id in jobs_to_delete:
            lxpApi.delete_job(id)
            logger.info('  %s' % pdf_files[id])

if __name__ == '__main__':
    lxpservice()
