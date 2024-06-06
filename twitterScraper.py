from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from portability import resource_path
import pathlib
import time
import pandas as pd
import json

from loggingSettings import logger_wrapper, logger_initialization


def load_settings():
    """The function loads the settings and creates saveback path.

    Args:
        None
    """
 
    with open(pathlib.Path(resource_path('Settings/settings.txt'))) as source:
        settings_dict = json.load(source)

    filepath = pathlib.Path(
        resource_path(f'SaveBacks/{settings_dict["result_name"]}'))
    
    return settings_dict, filepath


def initialize_connection(user_agent):
    """The function creates a driver with applied user agent.

    Args:
        user_agent (str): Description of the user agent.
    """ 

    driverpath = pathlib.Path(resource_path('ChromeDriver/chromedriver.exe'))

    my_user_agent = user_agent

    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", 
                                           ['enable-automation']) 
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(f"--user-agent={my_user_agent}")


    # Driver instance initialization.
    driver = webdriver.Chrome(service=Service(driverpath), 
                              options=chrome_options)
    
    return driver



# Initialization of the results DataFrame.
def define_result_table():
    """The function creates a list of headers, and an empty 
    list for lists of results from each scraping loop.

    Args:
        None                
    """ 

    headers = ['Author', 'Tweet', 'Link']
    rows = []

    return headers, rows

def load_data_rest_time():
    """The function creates a rest time needed to ensure 
    fluent data load.

    Args:
        None                
    """

    time.sleep(2)

@logger_wrapper
def entry_data_click(driver, entry_data, css_field_locator, 
                     xpath_button_locator):
    """The function is a reusable code snippet to enter login 
    credentials through the login process. It detects a field 
    for data entry and clicks the Next button.

    Args:
        driver (class): Driver object.
        entry_data (str): Credential data for the given stage 
        of login.
        css_field_locator (str): CSS characteristic for 
        the entry field.
        xpath_button_locator (str): XPATH to the confirmation 
        button.
    """
                         
    try:
        WebDriverWait(
            driver, 5).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, css_field_locator))).send_keys(entry_data)
        WebDriverWait(
            driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, xpath_button_locator))).click()
    except:
        pass

@logger_wrapper
def refuse_cookies(driver, xpath_button_locator):
    """The function clicks on the refuse cookies button when detected.

    Args:
        driver (class): Driver object.    
        xpath_button_locator (str): XPATH location of the button.
    """
    
    try:
        WebDriverWait(
            driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, xpath_button_locator))).click()
    except:
        pass

@logger_wrapper
def use_searchbar(driver, entry_data, css_field_locator):
    """The function takes a string an inputs it to the search bar 
    and initiate its search.

    Args:
        driver (class): Driver object.    
        entry_data (str): Search entry.
        css_field_locator (str): CSS locator for the search bar field.
    """

    try:
        WebDriverWait(
            driver, 5).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, css_field_locator))).send_keys(entry_data)
        WebDriverWait(
            driver, 5).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, css_field_locator))).send_keys(Keys.ENTER)
    except:
        pass

@logger_wrapper
def go_directly_to_search_latest(driver, entry_data):
    """The function takes a string an creates dynamically an search 
    url with latests tweets on given subject, to which the driver is 
    moved to.

    Args:
        driver (class): Driver object.    
        entry_data (str): Search entry.
    """

    try:
        entry_data = entry_data.replace(" ", "%20")
    except:
        pass

    url = f'https://twitter.com/search?q={entry_data}&src=typed_query&f=live'
    driver.get(url)

@logger_wrapper
def scrap_postings_data(driver):
    """The function scraps the available in current view tweet boxes, 
    and extracts a [tweeter_handler, tweet_text, tweet_link] list for 
    a single tweet that is appended to a temporary aggregating table 
    that fetches tweets available in the current view.

    Args:
        driver (class): Driver object.
    """

    aggregating_temp_table = []

    try:
        tweet_box_css = '[data-testid="tweet"]'
        postings = WebDriverWait(
            driver, 2).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, tweet_box_css)))
        postings = driver.find_elements(By.CSS_SELECTOR, tweet_box_css)
    except:
        pass

    for post in postings:
        try:
            tweet_link = post.find_elements(
                By.CSS_SELECTOR, '[role="link"]')[3].get_attribute('href')
            tweet_text = post.find_element(
                By.CSS_SELECTOR, '[data-testid="tweetText"]').text
            tweeter_handler = post.find_elements(
                By.CSS_SELECTOR, 
                '[style="text-overflow: unset;"]')[3].text
            
            scrap_result = [tweeter_handler, tweet_text, tweet_link]
            aggregating_temp_table.append(scrap_result)
        except:
            pass

    return aggregating_temp_table


def scraping_loop(driver, expected_screen_scrolls, rows):
    """The function scrolls through the page and fires 
    the scrap_postings_data() function after every scroll 
    to collect data.

    Args:
        driver (class): Driver object.
        expected_screen_scrolls (int): number of screens to scan.
        rows (list): List of collected rows.
    """

    iteration_counter = 1
    # Approx. 1080 px. is one screen scroll
    incremental_screen_scroll = 1200
    while iteration_counter < expected_screen_scrolls:
        try:
            rows.extend(scrap_postings_data(driver))
            driver.execute_script(
                f"window.scrollTo(0, {incremental_screen_scroll});")
            time.sleep(2)
            iteration_counter += 1
            incremental_screen_scroll += 1200
        except:
            continue


def prep_results(headers, rows, filepath):
    """The function prepares a DataFrame object to aggregate 
    and organize the collected data, cleaning it from duplicates.

    Args:
        headers (list): List of columns.
        rows (list): List of collected rows.
        filepath (str): Saveback location.
    """  

    result_table = pd.DataFrame(
        rows, columns = headers).drop_duplicates(subset="Link")

    result_table.to_csv(filepath, index_label='Index')



def main():
    settings_dict, filepath = load_settings()

    logger = logger_initialization(settings_dict["log_name"])
    logger.info('Scraping script started.')

    headers, rows = define_result_table()
    driver = initialize_connection(settings_dict["user_agent"])
    
    driver.get('https://twitter.com/i/flow/login')
    
    # E-mail address entry
    entry_data_click(driver,
                     settings_dict["email"], 
                     "[autocomplete='username']", 
                     "//button[@role='button'][contains(.,'Next')]")
    load_data_rest_time()
    # Username entry - happens as precaution when bot detected
    entry_data_click(driver,
                     settings_dict["account_name"], 
                     "[autocapitalize='none']", 
                     "//button[@role='button'][contains(.,'Next')]")
    load_data_rest_time()
    # Password entry
    entry_data_click(driver,
                     settings_dict["password"], 
                     "[autocomplete='current-password']", 
                     "//button[@role='button'][contains(.,'Log in')]")
    load_data_rest_time()
    # Refuse cookies
    refuse_cookies(driver, 
                   ("//button[@role='button']"+
                    "[contains(.,'Refuse non-essential cookies')]"))

    # Search section
    go_directly_to_search_latest(driver, settings_dict["search_query"])


    scraping_loop(driver, settings_dict["expected_screen_scrolls"], rows)

    prep_results(headers, rows, filepath)

    driver.quit()

if __name__ == "__main__":
    main()



