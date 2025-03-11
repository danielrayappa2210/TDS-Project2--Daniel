from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def fetch_authenticated_html(url, output_filename):
    # Set up Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Open the target URL
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        
        # Inject a dummy user into localStorage to bypass the sign-in check
        dummy_user = '{"email": "daniel@gramener.com"}'
        driver.execute_script(f'window.localStorage.setItem("user", \'{dummy_user}\');')
        print("Dummy user set in localStorage.")
        
        # Reload the page so that the script picks up the dummy user
        driver.refresh()
        time.sleep(5)  # Wait for the page to load with dummy authentication
        
        # Extract the full HTML of the authenticated page
        html_content = driver.page_source
        
        # Save the HTML content to a file
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Authenticated HTML content saved to {output_filename}.")
    
    except Exception as e:
        print("An error occurred:", e)
    
    finally:
        driver.quit()

if __name__ == '__main__':
    # Replace with your target URL
    target_url = "https://exam.sanand.workers.dev/tds-2025-01-ga1#hq-use-excel" # GA1
    # target_url = "https://exam.sanand.workers.dev/tds-2025-01-ga2#hq-use-colab" # GA2
    output_file = "GA1.html"
    fetch_authenticated_html(target_url, output_file)