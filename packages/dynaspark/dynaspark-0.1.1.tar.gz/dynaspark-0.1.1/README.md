# DynaSpark API

Currently only Python package is available.

A Python client for interacting with the DynaSpark API.

## Installation

You can install the package via pip:

```bash
pip install dynaspark
```

## Usage

```python
#Example Code
from dynaspark import dsai

# Initialize the client with your API key
client = dsai(api_key='YOUR_API_KEY')

# Generate a text response
user_input = "Tell me a joke."
response = client.generate_response(user_input)

print(response)

```
## Free API KEY
```
TH3_API_KEY
```