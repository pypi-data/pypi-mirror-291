QR Code Generator API
============

QR Code Generator is a simple tool for generating QR codes. It returns a PNG image of the QR code.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [QR Code Generator API](https://apiverve.com/marketplace/api/qrcodegenerator)

---

## Installation
	pip install apiverve-qrcodegenerator

---

## Configuration

Before using the qrcodegenerator API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The QR Code Generator API documentation is found here: [https://docs.apiverve.com/api/qrcodegenerator](https://docs.apiverve.com/api/qrcodegenerator).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_qrcodegenerator.apiClient import QrcodegeneratorAPIClient

# Initialize the client with your APIVerve API key
api = QrcodegeneratorAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = {  "value": "https://myspace.com",  "type": "url",  "format": "png",  "margin": "0" }
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
    "id": "62cfbf09-2532-431c-aed0-6d4c1a6c7140",
    "format": "png",
    "type": "url",
    "correction": "M",
    "size": 5,
    "margin": 0,
    "expires": 1723788997986,
    "downloadURL": "https://storage.googleapis.com/apiverve.appspot.com/qrcodegenerator/157c42c1-d8f9-4d6b-90c8-0d9d1e63d0b2.png?GoogleAccessId=635500398038-compute%40developer.gserviceaccount.com&Expires=1723788997&Signature=VEa1VkikAPtd7MAsC7DyiQwj5RtLxh9IC063Cz8eAafaJ9NuZ1zm5F1Eq4ukM%2FPWES5ro%2BU2mgDKHEPoNXQHWBeEgIK7E1JjUMZJaY%2BrgIYnv7dViAnbNmcd6T%2BayBy9Ewv62kE7hRoHWHmmQM8tOsJxExo7KiXoW6qnz8ldm4brkSVvo3Jop6nAMOGptq2oo0PjWOhG0oYGJ0TWjyNBwWQg5t8pK%2BdarCZwfM8JHViQSgVZBIsdiu%2FNBe64U1Jx%2FKoRdY8gpjyt4b01vqP1tZ0erdQmk%2FLJOjJB9EzoftaHQ8rRw7MkVkFqxiFhdRHp9qHu51Ga2Lm2ctUUsJO%2Fpw%3D%3D"
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