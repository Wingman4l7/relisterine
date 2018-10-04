# -*- coding: utf-8 -*-

import sys
import time
import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Style

init(autoreset=True)
opts = Options()  # options for chromedriver
opts.add_argument("--window-size=1000,1000")  # specifies window width,height
# opts.add_argument("headless")  # runs without the browser visible

# initialize chromedriver global variable.
chromedriver = None

# global font variables
bright_green = Fore.GREEN + Style.BRIGHT
bright_yellow = Fore.YELLOW + Style.BRIGHT
bright_magenta = Fore.MAGENTA + Style.BRIGHT
bright_cyan = Fore.CYAN + Style.BRIGHT
bright_red = Fore.RED + Style.BRIGHT
bright_white = Fore.WHITE + Style.BRIGHT


def countdown(seconds):
    # print '\n'
    for count in range(seconds, 0, -1):
        if(seconds > 3):
            print bright_yellow + '    **** Sleeping for %d seconds...\r' % count,
            sys.stdout.flush()
        time.sleep(1)


def login(email_handle, password):
    global chromedriver  # use the global chromedriver variable.
    print(bright_cyan + "\nLogging into Craigslist...")
    email_field = chromedriver.find_element_by_name('inputEmailHandle')
    email_field.send_keys(email_handle)
    password_field = chromedriver.find_element_by_name('inputPassword')
    password_field.send_keys(password)

    sign_in_submit = chromedriver.find_element_by_class_name('accountform-btn')
    sign_in_submit.click()
    countdown(5)

    # text of element: "Showing all recent postings"
    title_present = chromedriver.find_elements_by_class_name("postinglist_title")

    if len(title_present):  # element found
        print(bright_green + "Login Successful!  Continuing...")
        countdown(3)
    else:  # element not found
        print(bright_red + "Login Unsuccessful!  Exiting...")
        countdown(3)
        chromedriver.quit()
        exit(1)


def logout():
    global chromedriver  # use the global chromedriver variable.
    logout_link = chromedriver.find_element_by_link_text("log out")
    logout_link.click()
    # could also maybe just navigate directly to this link:  https://accounts.craigslist.org/logout
    print(bright_green + "Successfully logged out of Craigslist.")


def open_new_tab(link):
    global chromedriver  # use the global chromedriver variable.
    chromedriver.execute_script("window.open('');")
    chromedriver.switch_to.window(chromedriver.window_handles[1])
    chromedriver.get(link)
    countdown(5)


def check_for_renewals():
    global chromedriver  # use the global chromedriver variable.
    renew_links = chromedriver.find_elements_by_xpath("//input[contains(@class, 'managebtn') and contains(@value, 'renew')]")
    return renew_links


def click_renew_links(renew_links):
    global chromedriver  # use the global chromedriver variable.
    for link in renew_links:
        renew_URL = link.find_element_by_xpath("..").get_attribute('action')  # gets post URL from attribute in parent element
        open_new_tab(renew_URL)
        renew_button = chromedriver.find_element_by_xpath("//input[contains(@class, 'managebtn') and contains(@value, 'Renew this Posting')]")
        renew_button.click()
        countdown(3)
        renewed_text = chromedriver.find_elements_by_xpath("//*[contains(text(), 'This posting has been renewed.')]")
        if len(renewed_text):
            print(bright_green + "\n Listing renewed!")
        else:
            print(bright_red + "Listing possibly not renewed; something went wrong!")
        chromedriver.close()
        chromedriver.switch_to.window(chromedriver.window_handles[0])  # refocus on account listing tab
        countdown(3)


# main method
def main():
    global chromedriver  # use the global chromedriver variable.

    chromedriver = webdriver.Chrome('/Python27/selenium/webdriver/chromedriver', chrome_options=opts)
    chromedriver.get('https://accounts.craigslist.org/login/home')

    ### parse config file with login credentials ###
    config = ConfigParser.ConfigParser()
    config.read('relisterine_config.ini')
    email_handle = config.get('craigslist.org', 'EmailHandle')
    password = config.get('craigslist.org', 'Password')
    # print(bright_green + "Login credentials loaded from config file!")

    login(email_handle, password)  # uses config_file

    renew_links = check_for_renewals()
    if len(renew_links):  # renew links are present
        print(bright_green + "%d listings eligible for renewal have been found!") % len(renew_links)
        click_renew_links(renew_links)
    else:  # no renewal links at this time
        print(bright_yellow + "No listings to renew.  Exiting!")

    logout()

    print(bright_cyan + "\n Exiting script!")
    chromedriver.quit()  # comment out if you want to visually compare console results with actual results
    exit(0)


# process main method call
if __name__ == '__main__':
    main()
