# LxpApi
Library and Command-Line Interface for the LxpApi (www.letterxpress.de)

The package consists of two building blocks:
- Python library LxpApi to integrate the interface into Python applications.
- Command line tool lxpservice, which is [explained here](https://github.com/Simsys/LxpApi/blob/master/lxpservice.md). 

Installing LxpApi
-----------------

As usual, LxpApi is installed with pip (or pip3). This will install both the library and the command line tool.
```
$pip install lxpservice
```
Using LxpApi
------------

First import the LxpAPi library and pprint for nice view on complex python types.
```python
>>> from LxpApi import LxpApi
>>> from pprint import pprint
```
Create an instance of LxpApi with the credentials
```python
>>> url = "https://sandbox.letterxpress.de/v1/"
>>> user = <User-Name>
>>> api_key = <Api-Key>
>>> lxp_api = LxpApi(url, user, api_key)
```
Now we can work with the API and execute various commands. The library always returns an answer from which it can be seen if the function could be executed successfully.

Let's first look at the current credit balance.
```python
>>> response = lxp_api.get_balance()
>>> pprint(response)
{'auth': {'id': '46', 'status': 'active', 'user': <User-Name>},
 'balance': {'currency': 'EUR', 'value': '91.59'},
 'message': 'OK',
 'status': 200}
```
Now we upload a PDF file to the server
```python
>>> response=lxp_api.set_job('one-page.pdf')
>>> pprint(response)
{'auth': {'id': '46', 'status': 'active', 'user': <User-Name>},
 'letter': {'job_id': '3422',
            'price': 0.74,
            'specification': {'color': 1,
                              'mode': 'simplex',
                              'page': 1,
                              'ship': 'national'},
            'status': 'queue'},
 'message': 'OK',
 'status': 200}
```
In response, we receive some information such as the price or other attributes of the order. These attributes can be influenced during upload. How todo this and other information can be found in the [library documentation](https://github.com/Simsys/LxpApi/blob/master/LxpApi/lxpapi.py). Alternatively they can be retrieved with help(LxpApi). All available methods and possible parameters are described here.
