# BrowserController

`BrowserController` is a Python library that simplifies browser automation using Selenium. It provides a set of utility methods for common web automation tasks, such as navigating to URLs, interacting with elements, handling iframes and windows, executing JavaScript, and more.

## Installation

To use `BrowserController`, you need to have the following installed:

- Python 3.x
- Selenium (`pip install selenium`)
- ChromeDriver (Download the version compatible with your Chrome browser)

## Usage

### Initialization

To get started, initialize the `BrowserController` class with the path to your ChromeDriver:

```python
from webautomate import BrowserController

# Initialize the browser
browser =  BrowserController(path_chrome_driver='/path/to/chromedriver.exe')
