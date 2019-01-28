# Command line tool to manage LetterXpress print jobs.

With this tool credentials can be managed, print jobs can be activated, monitored and deleted.

Overview
--------
The lxpservice tool has four sub commands:
- credentials (Create and maintain credentials)
- status (check the status of the placed print jobs)
- send (Send PDF files to print service)
- delete (Delete job(s))

All commands are equipped with a help function
```
$ lxpservice --help
Usage: lxpservice [OPTIONS] COMMAND [ARGS]...

  Command line tool to manage LetterXpress print jobs.

  With this tool credentials can be managed, print jobs can be activated,
  monitored and deleted.

  See https://www.letterxpress.de

Options:
  --version      Show the version and exit.
  -v, --verbose  Be communicative.
  --help         Show this message and exit.

Commands:
  credentials  Create and maintain credentials.
  delete       Delete job(s).
  send         Send PDF files to print service.
  status       Check the status of the placed print jobs.
```

Managing Credentials
--------------------

```
$ lxpservice credentials --help
Usage: lxpservice credentials [OPTIONS] [USER] [URL] [APIKEY]

  Create and maintain credentials.

  The login data consists of user, url and api key. If all three parameters
  are specified, lxpapi stores them securely and uses  them in the future.
  If only user and url are specified, lxpapi loads the api key from the
  password repository of the operating  system. If only user is specified,
  lxapi changes the user, keeps the url and loads the api key from the
  password repository.

Options:
  -d, --delete  Deletes password (requires user and url).
  --help        Show this message and exit.
```

First, the credentials are passed to lxpservice. Lxpservice stores the user name and the url in the file ".lxpservice.ini" 
in the home directory of the current user. The necessary Api Key is stored safely in the password manager of the operating 
system.
```
$ lxpservice credentials <User_1> <Url> <Api_Key_1>
```
The login data no longer needs to be entered. Lxpservice can handle credentials for multiple users. All credentials are 
entered one after the other. You can now easily switch between users if the url remains the same by calling lxpservice 
with the username.
```
$ lxpservice credentials <User_2> <Url> <Api_Key_2>
$ lxpservice credentials <User_1>
$ lxpservice credentials <User_2>
```
Send PDF Files
--------------

```
$ lxpservice send --help
Usage: lxpservice send [OPTIONS] FILE_OR_DIRECTORY

  Send PDF files to print service.

  Either individual files or the PDF files of a directory can be
  transferred. Different options can be selected.

Options:
  -c, --color          Send colored Letters.
  -i, --international  Send letters to international destinations.
  -d, --duplex         Send double sided printed letters.
  --help               Show this message and exit.
```
PDF files are sent by specifying the path to the file. By adding optional arguments, you can influence the way the document 
is delivered. If you specify a path to a directory, lxpservice loads all PDF documents in that directory to the server. See 
also the help pages. 
```
$ lxpservice send -c one-page.pdf
User <User>
Url https://sandbox.letterxpress.de/v1/

Sending file(s) to print server...
  one-page.pdf

$ lxpservice send -d nine-pages.pdf
User <User>
Url https://sandbox.letterxpress.de/v1/

Sending file(s) to print server...
  nine-pages.pdf
```
Check Status of Print Jobs
--------------------------

```
$ lxpservice status --help
Usage: lxpservice status [OPTIONS]

  Check the status of the placed print jobs.

  A distinction is made between jobs covered by the credit balance and jobs
  not covered.

Options:
  --help  Show this message and exit.
```
With the sub command status you can easily check which files have been uploaded to the server.
```
lxpservice status
User <User>
Url https://sandbox.letterxpress.de/v1/

These letters will be sent soon:
Date                     Id Pgs Col Cost Filename                           
2019-01-27 21:03:47    3424   9   1 1.63 nine-pages.pdf                     
2019-01-27 21:03:33    3423   1   4 0.87 one-page.pdf
2019-01-27 20:11:42    3422   1   1 0.74 one-page.pdf
```
Delete Print jobs
-----------------

```
$ lxpservice delete --help
Usage: lxpservice delete [OPTIONS]

  Delete job(s).

  Delete a job identified by the id or delete all jobs of the print service.

Options:
  -i, --id INTEGER  Delete a single order.
  -a, --all         Delete all jobs.
  --help            Show this message and exit.
```  
Print jobs can be deleted with the delete command. A distinction is made between deleting a file 
(-i id) and all files (-a).
```
$ lxpservice delete -i 3424
User <User>
Url https://sandbox.letterxpress.de/v1/

Deleting order(s):
  nine-pages.pdf
  
$ lxpservice delete -a
User <User>
Url https://sandbox.letterxpress.de/v1/

Deleting order(s):
  one-page.pdf
  one-page.pdf
