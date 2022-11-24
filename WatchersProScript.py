import time
import tkinter
import SeleniumHelper as SH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

def watcherspro_connect_wallet(driver: webdriver):
    time.sleep(5)
    elems = driver.find_elements(By.CLASS_NAME, 'ant-checkbox-wrapper')
    if len(elems):
        elems[0].click()
        time.sleep(.5)
        driver.find_elements(By.XPATH, '//*[contains(text(), "Connect")]')[1].click()
        time.sleep(.5)
        driver.find_elements(By.CLASS_NAME, 'butLogo')[0].click()
        time.sleep(1)
        
        ###############
        SH.switch_window(driver, 'MetaMask Notification')
        buttons = driver.find_elements(By.XPATH, '//button[text()="Next"]')
        if len(buttons):
            buttons[0].click()
            time.sleep(1)

        buttons = driver.find_elements(By.XPATH, '//button[text()="Connect"]')
        if len(buttons):
            buttons[0].click()
            time.sleep(4)

        buttons = driver.find_elements(By.XPATH, '//button[text()="Sign"]')
        if len(buttons):
            buttons[0].click()
            time.sleep(1)

def get_address(driver: webdriver, tk: tkinter.Tk, elem:WebElement):    
    action = ActionChains(driver)
    action.move_to_element(elem).perform()
    copy_button = elem.find_element(By.XPATH, './/span[@role="img"]')
    # action.click(copy_button).perform()
    copy_button.click()
    return tk.clipboard_get()

def get_addresses_from_dialogbox(driver: webdriver, elem:WebElement):
    tk = tkinter.Tk()
    abbrv_addresses = elem.find_elements(By.CLASS_NAME, 'addressBox')
    tags = elem.find_elements(By.XPATH, './/div[@class="tableItem tag"]//span')
    
    for a, t in zip(abbrv_addresses, tags):
        full_address = get_address(driver, tk, a)
        print(full_address, ' | ', t.get_attribute('innerText'))
    
    return []

    