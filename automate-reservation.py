# from lib2to3.pgen2 import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from pathlib import Path
import time

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
username = "Ig10587-0"
password = "br1271@sn"

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
for handle in driver.window_handles:
    driver.switch_to.window(handle)

# Find all Tee Off Date
all_tee_off_date_range = len(Select(driver.find_element(by=By.ID, value="cpMain_cboDate")).options)
all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))

for index in range(all_tee_off_date_range):
    # Select by index
    all_tee_off_date_select.select_by_index(index)

    # Relocate element after selecting
    all_tee_off_date_select = Select(driver.find_element(by=By.ID, value="cpMain_cboDate"))
    selected_option_value = all_tee_off_date_select.first_selected_option.get_attribute("value")
    print("Currently selected date", selected_option_value)

    # Select only Morning session
    session_select = Select(driver.find_element(by=By.ID, value="cpMain_cboSession"))
    session_select.select_by_value("Morning")

    # Select only tee time where it is earlier than 7.30am
    tee_time_select = Select(driver.find_element(by=By.ID, value="cpMain_cboTeeTime"))
    for tee_time in tee_time_select.options:
        print(f"Available tee time at {selected_option_value}: {tee_time.get_attribute('text')}")

        # Get time and date and compare

# Find all Morning Sessions

# Find all Available Tee Time


# time.sleep(5)
# driver.close()
