from selenium import webdriver

def print_all_tab_title(driver: webdriver):
    for e in driver.window_handles:
        driver.switch_to.window(e)
        print(driver.title)

def switch_window(driver: webdriver, title:str):
    driver.switch_to.window(driver.window_handles[0])
    i = 1
    n = len(driver.window_handles)

    while i < n and driver.title != title:
        driver.switch_to.window(driver.window_handles[i])
        i += 1
    