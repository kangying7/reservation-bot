from calendar import Calendar, calendar, day_name
from xmlrpc.client import boolean
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from pathlib import Path
from configparser import ConfigParser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re
from datetime import datetime
from lib.custom_logger import CustomLogger
from lib.test_day_function import dayOnNextWeek
from lib.test_day_function import dayOnThisWeek
import argparse
from timeit import default_timer as timer
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import traceback

def save_screenshot_fullscreen(driver: webdriver.Chrome, path: str) -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    # driver.save_screenshot(path)  # has scrollbar
    driver.find_element_by_tag_name('body').screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])

def save_html_fullscreen(driver: webdriver.Chrome, path: str) -> None:
    with open(path, 'w') as file:
        file.write(driver.page_source)

def start_up(website_link:str, headless_mode:bool, logger:CustomLogger):
    start_time_chrome = timer()
    website_link = website_link

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(website_link)

    assert "Welcome to Kota Permai Golf and Country Club" in driver.title
    print(driver.title)

    logger.add_to_log(f"Time taken to start chrome - {timer() - start_time_chrome}s") 
    return driver

def main(driver: webdriver.Chrome, start_time_range:str, end_time_range:str, session:str, allow_booking:bool, logger:CustomLogger, day_to_book, username, password, output_folder, raw_day_of_the_week):
    logger.add_to_log(f"Current time after starting chrome is {datetime.now().strftime('%b %d %H:%M %S %f')}")
    start_time_login_page = timer()

    # Proceed to Login page
    online_booking_radio_button = driver.find_element(by=By.ID, value="cpMain_btnLogin")
    online_booking_radio_button.click()

    # Log on using credentials
    membership_no_input = driver.find_element(by=By.ID, value="cpMain_txtUserName")
    membership_no_input.send_keys(username)
    password_input = driver.find_element(by=By.ID, value="cpMain_txtPassword")
    password_input.send_keys(password)

    logon_button = driver.find_element(by=By.ID, value="cpMain_btnLogin")
    logon_button.click()

    # Timer
    logger.add_to_log(f"Time taken to log onto website - {timer() - start_time_login_page}s") 
    start_time_booking = timer()

    # Start booking
    click_here_button = driver.find_element(by=By.CLASS_NAME, value="btn-success")
    click_here_button.click()

    # Timer
    logger.add_to_log(f"Time taken to start booking - {timer() - start_time_booking}s") 
    start_time_booking_window = timer()

    # Switch to new Booking Window
    original_window = driver.current_window_handle

    for handle in driver.window_handles:
        driver.switch_to.window(handle)

    # Find all Tee Off Date
    all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))

    # Select date for reservation
    try:
        all_tee_off_date_select.select_by_value(day_to_book)
    except Exception as e:
        logger.add_to_log(f"There are no available Tee Off Date for - {day_to_book}")
        return
        
    # TODO: Create a function which returns driver if there exists an available tee time matching our criteria
       
    # Relocate element after selecting
    all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))
    selected_tee_off_date = all_tee_off_date_select.first_selected_option.get_attribute("value")
    logger.add_to_log(f"Currently selected date {selected_tee_off_date}")

    # Select session based on input
    try:
        session_select = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cpMain_cboSession"))
        ))
        session_select.select_by_value(session)
    except Exception as e:
        logger.add_to_log(f"No morning sessions are found for {selected_tee_off_date} -  \n{e}")
        raise e

    # Select only tee time where it is earlier than 7.30am
    try:
        tee_time_select = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cpMain_cboTeeTime"))
        ))
    except Exception as e:
        logger.add_to_log(f"No tee time select options could be found! - \n{e}")
        raise e

    all_tee_time_options_value = [tee_time_options.get_attribute('value') for tee_time_options in tee_time_select.options]
    logger.add_to_log(f"All tee time options are: {all_tee_time_options_value}")
    
    # Find a tee time slot matching both start and end range criteria
    after_time_list = []
    before_time_list = []
    final_time_list = []

    for tee_time_options_value in all_tee_time_options_value:
        # Retrieve date_time value from element value - 08:13 AM#@#10
        matched_date_time = re.match(r"(?:\d+:\d+)\s(?:AM|PM)", tee_time_options_value).group()
        selected_tee_time: datetime.time = datetime.strptime(matched_date_time, "%I:%M %p").time()

        start_tee_time_range: datetime.time = datetime.strptime(start_time_range, "%I:%M %p").time()
        end_tee_time_range: datetime.time = datetime.strptime(end_time_range, "%I:%M %p").time()

        is_tee_time_within_start_range: bool = selected_tee_time >= start_tee_time_range
        is_tee_time_within_end_range: bool = selected_tee_time < end_tee_time_range

        if is_tee_time_within_start_range:
            after_time_list.append(tee_time_options_value)
        
        if is_tee_time_within_end_range:
            before_time_list.append(tee_time_options_value)
        
        if is_tee_time_within_start_range and is_tee_time_within_end_range:
            final_time_list.append(tee_time_options_value)

    logger.add_to_log(f"All tee time options after {start_tee_time_range}: {after_time_list}")
    logger.add_to_log(f"All tee time options before {end_tee_time_range}: {before_time_list}")
    logger.add_to_log(f"All tee time options matching both range {start_tee_time_range} and {end_tee_time_range}: {final_time_list}")

    # Retrieve the first tee time option which fits both start and end criteria
    try:
        first_tee_time_option_to_choose_from = final_time_list.pop(0)
    except IndexError:
        logger.add_to_log(f"No suitable tee time is found, exiting...")
        return

    # Use the suitable tee time slot
    try:
        tee_time_select.select_by_value(first_tee_time_option_to_choose_from)
    except NoSuchElementException as e:
        traceback.print_exc()

    # Start booking
    next_button = driver.find_element(by=By.ID, value="cpMain_btnNext")
    next_button.click()   

    # Confirm booking page 
    next_button = driver.find_element(by=By.ID, value="cpMain_btnNext")
    next_button.click()   

    start_time_terms_condition_checkbox = timer()

    # Confirm terms and condition
    driver.maximize_window()
    try:
        tnc_checkbox = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "cpMain_chkTerm"))
        )
        logger.add_to_log(f"Found checkbox")
    except Exception as e:
        logger.add_to_log(f"No checkbox are found!")
        raise e
    # tnc_checkbox = driver.find_element(by=By.ID, value="cpMain_chkTerm")
    tnc_checkbox.click()   

    logger.add_to_log(f"Time taken to tick terms and conditions checkbox - {timer() - start_time_terms_condition_checkbox}s") 

    # Confirm booking button
    confirm_button = driver.find_element(by=By.ID, value="cpMain_btnSave")
    if allow_booking:
        start_time_confirm_button_clicked = timer()
        logger.add_to_log(f"Current time before clicking confirm button is {datetime.now().strftime('%b %d %H:%M %S %f')}")
        confirm_button.click()
        logger.add_to_log(f"Time taken to for confirm button to complete - {timer() - start_time_confirm_button_clicked}s") 
        logger.add_to_log(f"Success!")
        screenshot_file_path = output_folder /  f"success-{day_name[raw_day_of_the_week]}.png"
    save_screenshot_fullscreen(driver, str(screenshot_file_path))
    
    html_file_path = output_folder /  f"success-{day_name[raw_day_of_the_week]}.html"
    save_html_fullscreen(driver, html_file_path)
    logger.add_to_log(f"Time taken to complete booking window - {timer() - start_time_booking_window}s") 

def driver_program(start_time_range:str, end_time_range:str, raw_day_of_the_week, day_to_book, session, allow_booking, log_output_path: Path, username, password):
    output_folder = Path(log_output_path)
    logger = CustomLogger(output_folder, f"{day_name[raw_day_of_the_week]}.log")
    logger.add_to_log("================================")
    logger.add_to_log(f"{day_to_book} {day_name[raw_day_of_the_week]} {start_time_range}-{end_time_range} {allow_booking}")
    logger.add_to_log("================================")
    logger.add_to_log(f"Current time is {datetime.now().strftime('%b %d %H:%M %S %f')}")

    start_time = timer()
    # Start up configuration of webdriver
    webdriver = start_up("https://www.kotapermaionline.com.my/", True, logger)
    try:
        main(webdriver, start_time_range, end_time_range, session, allow_booking, logger, day_to_book, username, password, output_folder, raw_day_of_the_week)
    except Exception as e:
        traceback.print_exc()
        screenshot_file_path = output_folder /  f"{day_name[raw_day_of_the_week]}.png"
        save_screenshot_fullscreen(webdriver, str(screenshot_file_path))
    
    time_taken_to_complete = timer() - start_time
    logger.add_to_log(f"Current time after ending program is {datetime.now().strftime('%b %d %H:%M %S %f')}")
    logger.add_to_log(f"Time taken to complete - {round(time_taken_to_complete, 2)}s") 
    

if __name__ == "__main__":
    # driver("08:40", TUESDAY, False)
    parser = argparse.ArgumentParser(description='Automate reservation')
    parser.add_argument('--start-time', help='start range of reservation time', required=True)
    parser.add_argument('--end-time', help='end range of reservation time', required=True)
    parser.add_argument('--session', help='reservation session', required=True, choices=['Morning', 'Afternoon'])
    parser.add_argument('--day', help='day of the week', required=True)
    parser.add_argument('--log', help='log output path')
    parser.add_argument('--booking', help='enable booking', action="store_true")

    args = parser.parse_args()

    allow_booking = True if args.booking else False
    log_output_path = args.log
    start_time_range = args.start_time
    end_time_range = args.end_time
    raw_day_of_the_week = int(args.day)
    session = args.session
    print(allow_booking, start_time_range, end_time_range, raw_day_of_the_week)

    # Get credentials from config file
    config = ConfigParser()
    config.read("etc/config.txt")
    credentials = config['credentials']
    username = credentials.get('username')
    password = credentials.get('password')

    day_to_book = dayOnNextWeek(raw_day_of_the_week)
    # day_to_book = dayOnThisWeek(raw_day_of_the_week)

    driver_program(start_time_range, end_time_range, raw_day_of_the_week, day_to_book, session, allow_booking, log_output_path, username, password)



