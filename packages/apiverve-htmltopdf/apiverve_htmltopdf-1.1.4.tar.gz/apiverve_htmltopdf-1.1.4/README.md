HTML to PDF API
============

HTML to PDF is a simple tool for converting HTML to PDF. It returns the PDF file generated from the HTML.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [HTML to PDF API](https://apiverve.com/marketplace/api/htmltopdf)

---

## Installation
	pip install apiverve-htmltopdf

---

## Configuration

Before using the htmltopdf API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The HTML to PDF API documentation is found here: [https://docs.apiverve.com/api/htmltopdf](https://docs.apiverve.com/api/htmltopdf).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_htmltopdf.apiClient import HtmltopdfAPIClient

# Initialize the client with your APIVerve API key
api = HtmltopdfAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = {  "marginTop": 0.4,  "marginBottom": 0.4,  "marginLeft": 0.4,  "marginRight": 0.4,  "landscape": false,  "html": "<!doctype html> <html> <head> <title>This is the title of the webpage!</title> </head> <body> <p>This is an example paragraph. Anything in the <strong>body</strong> tag will appear on the page, just like this <strong>p</strong> tag and its contents.</p> </body> </html>" } 
```

###### Simple Request

```
# Make a request to the API
result = api.execute(query)

# Print the result
print(result)
```

###### Example Response

```
{
  "status": "ok",
  "error": null,
  "data": {
    "marginLeft": "0.4in",
    "marginRight": "0.4in",
    "marginTop": "0.4in",
    "marginBottom": "0.4in",
    "landscape": false,
    "pdfName": "bb735c6b-83de-49d0-8153-1c9e4bdb7fbc.pdf",
    "expires": 1723788930036,
    "downloadURL": "https://storage.googleapis.com/apiverve.appspot.com/htmltopdf/bb735c6b-83de-49d0-8153-1c9e4bdb7fbc.pdf?GoogleAccessId=635500398038-compute%40developer.gserviceaccount.com&Expires=1723788930&Signature=VwcU0l%2FF1xCxUB4Ux5byIVEOU2I%2FA89h9%2B%2FNt0JzKx3ZLsBAvmbI%2BtqNCGhCPUoJxA1jMxwW7cfpV5bF88oaUlVL%2BEl2Ndpw%2FuOB3J0n9r3nEKi06RPjGcKpnzuHFh10G1qCfI4bDN%2BpyuXP6Gn%2FhhvpdquE8YAWGitC2Q4zCDHItpcYvgxkyK%2BhuijpEOUALYCI4oi5NdB4d01gBjmyHi0JkD4qC4INsaMVulM54QxWCDpdQOufxuiJ6C1xONvDXFPAHhZGRTMdNrXRxOVSp6OIvqXK3QmQJwI6EYmc5Y5oUxNl%2BDRdep%2Fk2PO9kOGhqZ7SnO2P8%2Bkqe5NvsDu9%2Bw%3D%3D"
  },
  "code": 200
}
```

---

## Customer Support

Need any assistance? [Get in touch with Customer Support](https://apiverve.com/contact).

---

## Updates
Stay up to date by following [@apiverveHQ](https://twitter.com/apiverveHQ) on Twitter.

---

## Legal

All usage of the APIVerve website, API, and services is subject to the [APIVerve Terms of Service](https://apiverve.com/terms) and all legal documents and agreements.

---

## License
Licensed under the The MIT License (MIT)

Copyright (&copy;) 2024 APIVerve, and Evlar LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.