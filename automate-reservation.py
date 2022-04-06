# from lib2to3.pgen2 import driver
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

def main(raw_target_time:str, allow_booking:bool=False):
    start_time = datetime.now()

    # Launching reservation website
    chrome_driver_path = Path.cwd() / 'bin/chromedriver.exe'
    website_link = "https://www.kotapermaionline.com.my/"

    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(website_link)

    assert "Welcome to Kota Permai Golf and Country Club" in driver.title
    print(driver.title)

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

    # Start booking
    click_here_button = driver.find_element(by=By.CLASS_NAME, value="btn-success")
    click_here_button.click()

    # Switch to new Booking Window
    original_window = driver.current_window_handle

    for handle in driver.window_handles:
        driver.switch_to.window(handle)

    # Find all Tee Off Date
    all_tee_off_date_range = len(Select(driver.find_element(by=By.ID, value="cpMain_cboDate")).options)
    all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))

    # TODO: Create a function which returns driver if there exists an available tee time matching our criteria
    
    for index in range(all_tee_off_date_range):
        # Select by index
        all_tee_off_date_select.select_by_index(index)

        # Relocate element after selecting
        all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))
        selected_tee_off_date = all_tee_off_date_select.first_selected_option.get_attribute("value")
        print("Currently selected date", selected_tee_off_date)

        # Select only Morning session
        try:
            session_select = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cpMain_cboSession"))
            ))
            session_select.select_by_value("Morning")
        except NoSuchElementException as e:
            print(f"No morning sessions are found for {selected_tee_off_date} -  \n{e}")
        
        # Select only tee time where it is earlier than 7.30am
        tee_time_select = Select(driver.find_element(by=By.ID, value="cpMain_cboTeeTime"))
        for tee_time in tee_time_select.options:
            print(f"Available tee time at {selected_tee_off_date}: {tee_time.get_attribute('text')}")

            # Retrieve date_time value from element value - 08:13 AM#@#10
            matched_date_time = re.match(r"(\d+:\d+)\s", tee_time.get_attribute('value'))[1]
            selected_tee_time: datetime = datetime.strptime(matched_date_time, "%H:%M")
            target_time: datetime = datetime.strptime(raw_target_time, "%H:%M")

            # Compare if selected tee time is earlier than target time
            is_available_tee_time: bool = selected_tee_time <= target_time
            print(f"Selected tee time: {selected_tee_time} is earlier than target_time: {target_time} - {is_available_tee_time}")

            # Start booking
            if is_available_tee_time:
                next_button = driver.find_element(by=By.ID, value="cpMain_btnNext")
                next_button.click()   

                # Confirm booking page 
                next_button = driver.find_element(by=By.ID, value="cpMain_btnNext")
                next_button.click()   

                # Confirm terms and condition - cpMain_chkTerm
                tnc_checkbox = driver.find_element(by=By.ID, value="cpMain_chkTerm")
                tnc_checkbox.click()   

                # Confirm booking button
                # confirm_button = driver.find_element(by=By.ID, value="cpMain_btnSave")
                # if allow_booking:
                #     confirm_button.click()

                print(f"Time taken to complete - {datetime.now() -  start_time}")

                driver.close()

    # Close window if no available time is availabe
    driver.close()

    # Close original window
    # driver._switch_to.window(original_window)
    # driver.close()
    print("Hello")
    time.sleep(100)

if __name__ == "__main__":
    main("07:30", False)