# from lib2to3.pgen2 import driver
from calendar import TUESDAY, Calendar, calendar, day_name
import numbers
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
from custom_logger import CustomLogger
from test_day_function import dayOnNextWeek
import argparse
from timeit import default_timer as timer
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main(raw_target_time:str, allow_booking:bool, logger:CustomLogger, raw_day_of_the_week):
    # Timer
    # start_time_main = timer()

    # Timer
    start_time_chrome = timer()

    # Launching reservation website
    # chrome_driver_path = Path.cwd() / 'bin/chromedriver.exe'
    website_link = "https://www.kotapermaionline.com.my/"

    options = Options()
    options.headless = True
    # driver = webdriver.Chrome(chrome_driver_path, options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(website_link)

    assert "Welcome to Kota Permai Golf and Country Club" in driver.title
    print(driver.title)

    # Timer
    logger.add_to_log(f"Time taken to start chrome - {timer() - start_time_chrome}s") 
    logger.add_to_log(f"Current time after starting chrome is {datetime.now().strftime('%b %d %H:%M %S %f')}")
    start_time_login_page = timer()

    # Proceed to Login page
    online_booking_radio_button = driver.find_element(
        by=By.ID, 
        value="cpMain_btnLogin")
    online_booking_radio_button.click()

    # Log on using credentials
    config = ConfigParser()
    config.read("etc/config.txt")
    credentials = config['credentials']
    username = credentials.get('username')
    password = credentials.get('password')

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
    all_tee_off_date_range = len(Select(driver.find_element(by=By.ID, value="cpMain_cboDate")).options)
    all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))

    # Select date for reservation
    day_to_book = dayOnNextWeek(raw_day_of_the_week)
    logger.add_to_log(f"Making reservation for - {day_to_book}")
    all_tee_off_date_select.select_by_value(day_to_book)

    # TODO: Create a function which returns driver if there exists an available tee time matching our criteria
       
    # Relocate element after selecting
    all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))
    selected_tee_off_date = all_tee_off_date_select.first_selected_option.get_attribute("value")
    logger.add_to_log(f"Currently selected date {selected_tee_off_date}")

    # Select only Morning session
    try:
        session_select = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cpMain_cboSession"))
        ))
        session_select.select_by_value("Morning")
    except NoSuchElementException as e:
        logger.add_to_log(f"No morning sessions are found for {selected_tee_off_date} -  \n{e}")

    # Select only tee time where it is earlier than 7.30am
    tee_time_select = Select(driver.find_element(by=By.ID, value="cpMain_cboTeeTime"))
    for tee_time in tee_time_select.options:
        # logger.add_to_log(f"Available tee time: {tee_time.get_attribute('text')}")

        # Retrieve date_time value from element value - 08:13 AM#@#10
        matched_date_time = re.match(r"(\d+:\d+)\s", tee_time.get_attribute('value'))[1]
        selected_tee_time: datetime.time = datetime.strptime(matched_date_time, "%H:%M").time()
        target_time: datetime.time = datetime.strptime(raw_target_time, "%H:%M").time()

        # Compare if selected tee time is earlier than target time

        is_available_tee_time: bool = selected_tee_time <= target_time
        logger.add_to_log(f"Selected tee time: {selected_tee_time} is earlier than target_time: {target_time} - {is_available_tee_time}")

        # Start booking
        if is_available_tee_time:
            next_button = driver.find_element(by=By.ID, value="cpMain_btnNext")
            next_button.click()   

            # Confirm booking page 
            next_button = driver.find_element(by=By.ID, value="cpMain_btnNext")
            next_button.click()   

            # Confirm terms and condition
            try:
                tnc_checkbox = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "cpMain_chkTerm"))
                )
                session_select.select_by_value("Morning")
            except NoSuchElementException as e:
                logger.add_to_log(f"No checkbox are found!")
            # tnc_checkbox = driver.find_element(by=By.ID, value="cpMain_chkTerm")
            tnc_checkbox.click()   

            # Confirm booking button
            confirm_button = driver.find_element(by=By.ID, value="cpMain_btnSave")
            if allow_booking:
                # confirm_button.click()
                logger.add_to_log(f"Success!")

                pass

    logger.add_to_log(f"Time taken to complete booking window - {timer() - start_time_booking_window}s") 

    # logger.add_to_log(f"Time taken to complete main - {timer() - start_time_main}s") 

    # Close window if no available time is availabe
    # driver.close()

    # Close original window
    # driver._switch_to.window(original_window)
    # driver.close()

def driver_program(raw_target_time:str, raw_day_of_the_week, allow_booking, log_output_path: Path):
    output_folder = log_output_path
    logger = CustomLogger(output_folder, f"{day_name[raw_day_of_the_week]}.log")
    logger.add_to_log("================================")
    logger.add_to_log(f"{day_name[raw_day_of_the_week]} {raw_target_time} {allow_booking}")
    logger.add_to_log("================================")
    logger.add_to_log(f"Current time is {datetime.now().strftime('%b %d %H:%M %S %f')}")

    start_time = timer()
    main(raw_target_time, allow_booking, logger, raw_day_of_the_week)
    time_taken_to_complete = timer() - start_time
    logger.add_to_log(f"Time taken to complete - {round(time_taken_to_complete, 2)}s") 
    

if __name__ == "__main__":
    # driver("08:40", TUESDAY, False)
    parser = argparse.ArgumentParser(description='Automate reservation')
    parser.add_argument('--time', help='reservation time', required=True)
    parser.add_argument('--day', help='day of the week', required=True)
    parser.add_argument('--log', help='log output path')
    parser.add_argument('--booking', help='enable booking', action="store_true")

    args = parser.parse_args()

    allow_booking = True if args.booking else False
    log_output_path = args.log
    raw_target_time = args.time
    raw_day_of_the_week = int(args.day)
    print(allow_booking, raw_target_time, raw_day_of_the_week)

    driver_program(raw_target_time, raw_day_of_the_week, allow_booking, log_output_path)



