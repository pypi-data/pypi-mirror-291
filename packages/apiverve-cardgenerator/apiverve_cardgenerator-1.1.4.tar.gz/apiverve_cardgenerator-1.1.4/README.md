Card Generator API
============

Card Generator is a simple tool for generating test/sample card numbers. It returns a list of card numbers for testing.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [Card Generator API](https://apiverve.com/marketplace/api/cardgenerator)

---

## Installation
	pip install apiverve-cardgenerator

---

## Configuration

Before using the cardgenerator API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The Card Generator API documentation is found here: [https://docs.apiverve.com/api/cardgenerator](https://docs.apiverve.com/api/cardgenerator).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_cardgenerator.apiClient import CardgeneratorAPIClient

# Initialize the client with your APIVerve API key
api = CardgeneratorAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = { "brand": "visa",  "count": 5 }
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
    "brand": "visa",
    "count": 5,
    "cards": [
      {
        "cvv": 781,
        "issuer": "SWEDBANK AB",
        "number": "4581973945415963",
        "expiration": "2029-08-14T06:13:55.186Z",
        "brand": "visa",
        "number_alt": "4581 9739 4541 5963"
      },
      {
        "cvv": 785,
        "issuer": "CAJA LABORAL POPULAR DE MONDRAGON",
        "number": "4548594469310661",
        "expiration": "2029-08-14T06:13:55.189Z",
        "brand": "visa",
        "number_alt": "4548 5944 6931 0661"
      },
      {
        "cvv": 995,
        "issuer": "JSC KOR STANDARD BANK",
        "number": "4244088464600744",
        "expiration": "2029-08-14T06:13:55.192Z",
        "brand": "visa",
        "number_alt": "4244 0884 6460 0744"
      },
      {
        "cvv": 966,
        "issuer": "NEW WINDSOR STATE BANK",
        "number": "4138171569648237",
        "expiration": "2029-08-14T06:13:55.194Z",
        "brand": "visa",
        "number_alt": "4138 1715 6964 8237"
      },
      {
        "cvv": 693,
        "issuer": "OJSC SOCIAL COMMERCIAL BANK OF PRIMORYE PRIMSOTSBANK",
        "number": "4195798981462852",
        "expiration": "2029-08-14T06:13:55.196Z",
        "brand": "visa",
        "number_alt": "4195 7989 8146 2852"
      }
    ],
    "owner": {
      "name": "Shelly Botsford Sr.",
      "address": {
        "street": "83263 Jones Crescent",
        "city": "Bergeland",
        "state": "Maryland",
        "zipCode": "03258"
      }
    }
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