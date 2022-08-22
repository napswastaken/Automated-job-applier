import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select


def employer_questions(driver):
    print("questions")
    sleep(10)

    dropdowns = driver.find_elements_by_tag_name("select")

    for box in dropdowns:
        try:
            select = Select(box)
            select.select_by_visible_text('5 years')
        except:
            pass

    yesno = driver.find_elements_by_css_selector("[tabindex='0']")
    for item in yesno:
        try:
            item.click()
        except:
            pass


def continue_button(driver):
    sleep(2)
    driver.find_element_by_css_selector("[data-testid='continue-button']").click()
    print("continue")
    sleep(5)


def submit(driver):
    sleep(2)
    driver.find_element_by_css_selector("[data-testid='review-submit-application']").click()
    sleep(5)
    print("submitted")


def step(driver):
    # find which step of the application we are on, then fill in the correct data
    try:
        section = driver.find_element_by_css_selector("[aria-current='step']")
        option = section.get_attribute('data-testid')
        option = option.split(". ")[1]
        print(option)

        # loop through options for each step
        if option == "Answer employer questions":
            employer_questions(driver)
            continue_button(driver)
            step(driver)
        elif option == "Update SEEK Profile":
            continue_button(driver)
            step(driver)
        elif option == "Most recent role":
            continue_button(driver)
            step(driver)
        elif option == "Review and submit":
            submit(driver)
    except:
        sleep(2)
        print("crashed")
        return


def user_input(driver, el_id, text):
    # used for the login screen to enter username and password
    element = driver.find_element_by_id(el_id)
    element.clear()
    element.send_keys(text)


def seek_login(driver):
    # get login info from user
    email = input("enter your email: ")
    password = input("enter your password: ")

    # open login page, enter email and password
    driver.get("https://www.seek.com.au/oauth/login")
    sleep(1)
    user_input(driver, "emailAddress", email)
    user_input(driver, "password", password)

    # sign in
    # this shit changes often causing the script to break... thanks seek..
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/form/div/div[4]/div/div/div["
        "1]/button").click()


def seek_job_search(driver, page):
    # wait for login and open list of jobs
    sleep(5)
    driver.get(page)
    sleep(2)

    # get the ID from each job
    ids = driver.find_elements_by_css_selector("[data-automation='jobTitle']")
    results = []

    # append each id to the results list
    for i in ids:
        href = i.get_attribute('href')
        result = re.search('job/(.*)[?]type', href)
        print(result.groups()[0])
        results.append(result.groups()[0])

    return results


def apply(driver, links):
    for link in links:
        url = "https://www.seek.com.au/job/" + link + "/apply/"
        driver.get(url)
        sleep(2)

        if driver.current_url == url:

            # select upload cover letter and submit file
            driver.find_element_by_id("coverLetter_0").click()
            sleep(2)
            driver.find_element_by_css_selector("[data-testid='continue-button']").click()
            sleep(5)
            # complete each step of the application, looping until submission
            step(driver)


if __name__ == '__main__':
    # use Google Chrome as webdriver for this program, login to seek. Firefox driver is fucked.
    browser = webdriver.Chrome() #firefox??
    seek_login(browser)

    Page = 1
    while 1:
        Page += 1
        Query = "management"
        uri = "https://www.seek.com.au/" + Query + "jobs/in-All-Melbourne-VIC?page=" + str(Page) + "&sortmode" \
                                                                                                   "=ListedDate "
        list_of_IDs = seek_job_search(browser, uri)
        apply(browser, list_of_IDs)
        sleep(2)  # wait for next page to load
