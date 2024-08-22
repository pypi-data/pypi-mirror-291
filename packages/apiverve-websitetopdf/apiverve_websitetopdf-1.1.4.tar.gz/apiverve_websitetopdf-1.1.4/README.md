Website to PDF API
============

Website to PDF is a simple tool for converting a website to PDF. It returns the PDF file generated from the website.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [Website to PDF API](https://apiverve.com/marketplace/api/websitetopdf)

---

## Installation
	pip install apiverve-websitetopdf

---

## Configuration

Before using the websitetopdf API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The Website to PDF API documentation is found here: [https://docs.apiverve.com/api/websitetopdf](https://docs.apiverve.com/api/websitetopdf).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_websitetopdf.apiClient import WebsitetopdfAPIClient

# Initialize the client with your APIVerve API key
api = WebsitetopdfAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = {  "marginTop": 0.4,  "marginBottom": 0.4,  "marginLeft": 0.4,  "marginRight": 0.4,  "landscape": false,  "url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts" }
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
    "pdfName": "512e8a7c-32f6-4fc4-9d48-33d8de1c07a8.pdf",
    "expires": 1723789170645,
    "url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts",
    "downloadURL": "https://storage.googleapis.com/apiverve.appspot.com/websitetopdf/512e8a7c-32f6-4fc4-9d48-33d8de1c07a8.pdf?GoogleAccessId=635500398038-compute%40developer.gserviceaccount.com&Expires=1723789170&Signature=bgLti%2FSsLz%2BCmsv2LK77sezP%2FDyhlOr5haK6SMZUAuuL5F8ZtRmXDSQGlpYe4jvpauUPSF5MeW%2Bs%2B1D7o3DqX1rh7NQ1h8ct1qG5th0qWlchqPolP%2BxkpWVib6NAWmfRx3LeepgIYs%2BezwYUIMFgoLoXj3p3lEcyCTv9dlZGV9MdZfoDoJSKc2xAMBEXj6nRCMCBRBLLVgpycxGh3qhJrWEET%2FbkxaEcQ1QbYVTYC5V1fGaEJyTKjJc0JySuoGM0lvatqjJ5%2BHDDKLedjh718Qyr1caiq52vcFH4sIlF9%2B0mse%2FCtmRsVL0Nb8udKnLODBo9CmcJmvKAkWqquMljIQ%3D%3D"
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