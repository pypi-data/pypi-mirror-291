from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time
from pathlib import Path
from selenium.webdriver.chrome.service import Service

class BrowserController:
    def __init__(self, path_chrome_driver):
        """
        Initializes the Chrome browser with configured options.
        
        :param path_chrome_driver: Path to the Chrome driver executable.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(path_chrome_driver)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.downloads = str(Path.home() / "Downloads")

        self.dowloads = str(Path.home() / "Downloads")
        
    def url_browser(self, url):
        """
        Navigates to the specified URL and waits 3 seconds for the page to load.
        
        :param url: The URL to navigate to.
        """
        self.driver.get(url)
        time.sleep(3)

    def find_element(self, locator_type, locator_value, wait_time=5):
        """
        Finds an element on the web page using the specified locator type and value, and waits until it is present.
        
        :param locator_type: Type of locator (By.XPATH, By.ID, By.NAME, By.CLASS_NAME, By.CSS_SELECTOR, etc.).
        :param locator_value: Value of the locator.
        :param wait_time: Maximum wait time in seconds.
        :return: True if the element is found, False otherwise.
        """
        try:
            selector_type = self._get_selector_type(locator_type)
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((selector_type, locator_value))
            )
            return True
        except Exception as e:
            print(f"Error finding element: {e}")
            return False

    def switch_to_iframe(self, locator_type, locator_value, wait_time=5):
        """
        Switches the context to the specified iframe by its locator type and value.
        
        :param locator_type: Type of locator (By.XPATH, By.ID, By.NAME, etc.).
        :param locator_value: Value of the locator.
        :param wait_time: Maximum wait time in seconds.
        """
        try:
            selector_type = self._get_selector_type(locator_type)
            iframe_element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((selector_type , locator_value))
            )
            self.driver.switch_to.frame(iframe_element)
        except Exception as e:
            print(f"Error switching to iframe: {e}")

    def switch_window(self, index, wait_time=5):
        """
        Switches to the window specified by its index in the list of open windows.
        
        :param index: Index of the window to switch to.
        :param wait_time: Maximum wait time in seconds.
        """
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda d: len(d.window_handles) > index
            )
            self.driver.switch_to.window(self.driver.window_handles[index])
        except Exception as e:
            print(f"Error switching window: {e}")

    def print_pdf(self):
        """
        Prints the current page as a PDF.
        """
        self.driver.execute_script('window.print();')

    def read(self, locator_type, locator_value):
        """
        Reads the text of the element specified by its locator type and value.
        
        :param locator_type: Type of locator (By.XPATH, By.ID, By.NAME, etc.).
        :param locator_value: Value of the locator.
        :return: Text of the element.
        """
        try:
            selector_type = self._get_selector_type(locator_type)
            element = self.driver.find_element(selector_type, locator_value)
            return element.text
        except Exception as e:
            print(f"Error reading element: {e}")
            return ""

    def write(self, locator_type, locator_value, text, key=''):
        """
        Writes text to an input field specified by its locator type and value.
        
        :param locator_type: Type of locator (By.XPATH, By.ID, By.NAME, etc.).
        :param locator_value: Value of the locator.
        :param text: Text to write in the field.
        :param key: Optional key to send.
        """
        try:
            selector_type = self._get_selector_type(locator_type)
            element = self.driver.find_element(selector_type, locator_value)
            element.click()
            if key:
                element.send_keys(key)
            else:
                element.clear()
                element.send_keys(text)
        except Exception as e:
            print(f"Error writing to field: {e}")

    def click(self, locator_type, locator_value):
        """
        Clicks on the element specified by its locator type and value.
        
        :param locator_type: Type of locator (By.XPATH, By.ID, By.NAME, etc.).
        :param locator_value: Value of the locator.
        """
        try:
            selector_type = self._get_selector_type(locator_type)
            element = self.driver.find_element(selector_type, locator_value)
            element.click()
        except Exception as e:
            print(f"Error clicking element: {e}")

    def execute_js(self, script):
        """
        Executes a JavaScript script on the current page.
        
        :param script: JavaScript code to execute.
        :return: Result of the script execution.
        """
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            print(f"Error executing script: {e}")
            return None

    def close(self):
        """
        Closes the current browser window.
        """
        self.driver.close()

    def scroll(self, x, y):
        """
        Scrolls the page to the specified coordinates.
        
        :param x: Horizontal coordinate.
        :param y: Vertical coordinate.
        """
        js = f"window.scrollTo({x}, {y})"
        self.execute_js(js)

    def locate_element_click_or_visibility(self, css_selector, method='click'):
        """
        Finds an element using a CSS selector and performs a specified action.
        
        :param css_selector: CSS selector of the element.
        :param method: Interaction method ('click' or 'search').
        :return: WebDriverWait element that was found.
        """
        try:
            if method == "click":
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
                )
            elif method == "search":
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
                )
            return element
        except Exception as e:
            print(f"Error finding or clicking element: {e}")
            return None
    
    
    def reload_page(self):
        """
            Reloads the current web page.
        """
        try:
            self.driver.refresh()
            print("Page reloaded successfully.")
        except Exception as e:
            print(f"Error reloading page: {e}")

    def navigate_back(self):
        """
        Navigates back to the previous page in the browser history.
        """
        try:
            self.driver.back()
            print("Navigated back successfully.")
        except Exception as e:
            print(f"Error navigating back: {e}")
    
    def double_click(self, locator_type, locator_value):
        """
        Performs a double-click action on an element specified by its locator type and value.
        
        :param locator_type: Type of locator (e.g., "xpath", "id", "name", "css_selector").
        :param locator_value: The locator value to identify the element.
        """
        try:            
            selector_type = self._get_selector_type(locator_type)            
            element = self.driver.find_element(selector_type, locator_value)
            action_chains = ActionChains(self.driver)
            action_chains.double_click(element).perform()           
        except Exception as e:
            print(f"Error performing double-click on the element: {e}")
    
    def force_download(self, url_file, name_file):
        """
        Forces the browser to download a file from the given URL and saves it with the specified file name.
        
        :param url_file: The URL of the file to be downloaded.
        :param name_file: The desired name for the downloaded file.
        """
        try:
            # JavaScript code to create a temporary download link and trigger the download
            script = """
                var url = arguments[0];
                var filename = arguments[1];
                var link = document.createElement('a');
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            """
            
            # Execute the JavaScript in the browser context
            self.driver.execute_script(script, url_file, name_file)            
            print(f"Download initiated for {name_file} from {url_file}")
        except Exception as e:
            print(f"Error initiating download: {e}")

    
    def open_new_tab(self, url):
        """
        Opens a new browser tab with the specified URL and switches to it.
        
        :param url: The URL to open in the new tab.
        """
        try:
            
            self.driver.execute_script(f'window.open("{url}", "_blank");') 
            self.driver.switch_to.window(self.driver.window_handles[-1])            
            print(f"New tab opened with URL: {url}")
        except Exception as e:
            print(f"Error opening new tab: {e}")

    def upload_files(self, locator_type, locator_value, files, single_file=None):
        """
        Uploads files to a specified web element (like an input[type="file"]).
        
        :param data_: The locator value to find the upload element.
        :param data_type: The type of locator (e.g., By.XPATH, By.ID).
        :param files: A list of file paths or a single file path to be uploaded.
        :param single_file: A single file path to be uploaded (optional). If provided, it overrides the 'files' parameter.
        """
        try:
            # Get the appropriate selector type
            selector_type = self._get_selector_type(locator_type)
            
            # Locate the element using the provided locator
            element = self.driver.find_element(selector_type, locator_value)
            
            # If a single file is provided, upload it
            if single_file:
                print(f"Uploading single file: {single_file}")
                element.send_keys(single_file)
            else:
                # If multiple files are provided, prepare the paths
                files = files.replace("\\", "/")
                
                if files.startswith("["):
                    files = eval(files)  # Convert string representation of list to actual list
                    files = "\n".join(files)  # Join paths with newline for multiple file upload
                
                print(f"Uploading files: {files}")
                element.send_keys(files)
        except Exception as e:
            print(f"Error uploading files: {e}")

        
    def _get_selector_type(self, selector_type):
        selector_type = selector_type.lower().replace(" ", "_")
        types = {
            "name": By.NAME,
            "id": By.ID,
            "class_name": By.CLASS_NAME,
            "xpath": By.XPATH,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "css_selector": By.CSS_SELECTOR
        }
        
        if selector_type in types:
            return types[selector_type]
        else:
            raise ValueError(f"Invalid selector type: {selector_type}. Valid types are: {', '.join(types.keys())}")
