# Live Options Data Fetcher

## Description

This Python package retrieves live data for options trade of Tehran Stock Exchange and Iran Farabourse Exchange based on the underlying asset's ticker and option type. It supports tickers such as "خودرو" and option types including "call" and "put."

## Features

- Fetch live option data for specified tickers.
- Support for multiple option types: "call" and "put."
- Easy integration with your existing applications.

## Installation

You can install the package via pip:

```python
pip install tse_derivatives
```
<div>
## Example
</div>

```python
from tse_derivative import tse_options

ticker = "خودرو" # or "اهرم" ...
type = "call"  # or "put"
data = tse_options(ticker, type)
print(data)
```
