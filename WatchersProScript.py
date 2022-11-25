import time
import tkinter
import pandas as pd
import SeleniumHelper as SH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

def watcherspro_connect_wallet(driver: webdriver):
    time.sleep(2) # Important! Wait 2s to see if we get redirected to a login page.
    
    if 'login' in driver.current_url:
        driver.implicitly_wait(10)
        driver.find_element(By.CLASS_NAME, 'ant-checkbox-wrapper').click()
        driver.find_elements(By.XPATH, '//*[contains(text(), "Connect")]')[1].click()
        time.sleep(2) #Important wait!
        driver.find_element(By.CLASS_NAME, 'butLogo').click()
        
        ###############
        time.sleep(3) # Important! Wait for the window "MetaMask Notification" to open
        SH.switch_window(driver, 'MetaMask Notification')
        buttons = driver.find_elements(By.XPATH, '//button[text()="Next"]')
        if len(buttons):
            buttons[0].click()

        buttons = driver.find_elements(By.XPATH, '//button[text()="Connect"]')
        if len(buttons):
            buttons[0].click()

        buttons = driver.find_elements(By.XPATH, '//button[text()="Sign"]')
        if len(buttons):
            buttons[0].click()

def scrape_vc_watch_overview(driver: webdriver):
    driver.implicitly_wait(20)
    driver.get('https://watchers.pro/#/vcWatch')

    table = driver.find_element(By.XPATH, '//div[@class="ant-table-wrapper"]')
    print(get_current_page(table))
    print(get_page_count(table))
    for i in range(2, 9):
        jump_to_page(table, i)
        data = extract_data(driver, table)
        saveToCSV(data, f'vc_entities_page{i}.csv')

def extract_data(driver: webdriver, table:WebElement):
    time.sleep(3)
    result = []
    action = ActionChains(driver)
    row_elems = driver.find_elements(By.XPATH, '//tr[@data-row-key]')
    for row in row_elems:
        cells = row.find_elements(By.XPATH, './/td')
        action.click(cells[2]).perform() # Open Address dialog box
        time.sleep(1)
        dialogbox_elem = driver.find_element(By.XPATH, '//div[@role="dialog"]')
        result.extend(get_addresses_from_dialogbox(driver, dialogbox_elem))
        time.sleep(2)
        action.send_keys(Keys.ESCAPE).perform()
    
    return result


def get_pagination_buttons(table:WebElement):
    pagination_buttons = table.find_elements(By.XPATH, './/ul[contains(@class,"ant-pagination")]//li')
    return pagination_buttons if pagination_buttons else None

def get_current_page(table:WebElement):
    return int(table.find_element(By.XPATH, './/*[contains(@class, "ant-pagination-item-active")]').get_attribute('title'))

def get_page_count(table:WebElement, pagination_buttons:list[WebElement]=None):
    if pagination_buttons == None:
        pagination_buttons = get_pagination_buttons(table)

    if pagination_buttons:
        return int(pagination_buttons[len(pagination_buttons) - 2].text)
    
    return 1

def jump_to_page(table:WebElement, page_number:int):
    pagination_buttons = get_pagination_buttons(table)

    if pagination_buttons:
        page_count = get_page_count(table, pagination_buttons)
        if 0 < page_number <= page_count:
            current_page = get_current_page(table)
            if current_page > page_number:
                button_to_click = pagination_buttons[0] # Prev Button
            else:
                button_to_click = pagination_buttons[-1] # Next Button

            for _ in range(abs(page_number - current_page)):
                button_to_click.click()
    
def get_address(driver: webdriver, tk: tkinter.Tk, elem:WebElement):    
    action = ActionChains(driver)
    action.move_to_element(elem).perform()
    copy_button = elem.find_element(By.XPATH, './/span[@role="img"]')
    copy_button.click()
    return tk.clipboard_get()

def get_addresses_from_dialogbox(driver: webdriver, elem:WebElement):
    tk = tkinter.Tk()
    abbrv_addresses = elem.find_elements(By.CLASS_NAME, 'addressBox')
    tags = elem.find_elements(By.XPATH, './/div[@class="tableItem tag"]//span')
    
    result =[]
    for a, t in zip(abbrv_addresses, tags):
        try:
            full_address = get_address(driver, tk, a)
            splitted = t.text.split(':')
            result.append([splitted[0], full_address, splitted[1:]])
            print(result[-1])
        except Exception as e:
            print("ERROR: There are something wrong")
            print('abbrv_addresses =', a.get_attribute('innerHTML'))
            print('tag =', t.get_attribute('innerHTML'))
    return result

def saveToCSV(data, outputFilename):
    df = pd.DataFrame(data, columns = ['Entity', 'Address', 'Tags'])
    df.to_csv(outputFilename, index = False)
    return df