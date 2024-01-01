import time

from selenium import webdriver


# Create a new instance of the Chrome drivers
chrome_path="/usr/local/bin/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')        # Run in headless mode
chrome_options.add_argument('--no-sandbox')      # Disable sandboxing (useful in some environments)
chrome_options.add_argument('--disable-gpu')     # Disable GPU acceleration

# Create a WebDriver instance with the configured options
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

try:
    # Open the web app in the browser
    driver.get("http://127.0.0.1:5000/users/get_user_id/5")

    # Wait for the page to load
    driver.implicitly_wait(60)
 
finally:
    # Close the browser window
    driver.quit()
