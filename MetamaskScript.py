import time
import SeleniumHelper as SH
from selenium import webdriver
from selenium.webdriver.common.by import By

def metamask_login(driver: webdriver):
    SH.switch_window(driver, 'MetaMask')
    if '#unlock' in driver.current_url:
        metamask_quick_login(driver)
    else:
        metamask_full_login(driver)

def metamask_quick_login(driver: webdriver):
    inputs = driver.find_elements(By.XPATH, '//input')
    if len(inputs):
        inputs[0].send_keys('Y7E5HQVLJRDnMVb')
        # driver.find_element(By.ID, 'password').send_keys('Y7E5HQVLJRDnMVb')
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[text()="Unlock"]').click()
        time.sleep(1)
        driver.close()

def metamask_full_login(driver: webdriver):
    driver.find_element(By.XPATH, '//button[text()="Get started"]').click()
    driver.find_element(By.XPATH, '//button[text()="No thanks"]').click()
    driver.find_element(By.XPATH, '//button[text()="Import wallet"]').click()

    inputs = driver.find_elements(By.XPATH, '//input')
    inputs[0].send_keys('nasty\t\tstreet\t\tvague\t\tvoice\t\tcoil\t\twish\t\ttonight\t\tenlist\t\tgentle\t\tconnect\t\tlumber\t\tswear')
    driver.find_element(By.ID, 'password').send_keys('Y7E5HQVLJRDnMVb')
    driver.find_element(By.ID, 'confirm-password').send_keys('Y7E5HQVLJRDnMVb')

    driver.find_element(By.ID, 'create-new-vault__terms-checkbox').click()

    driver.find_element(By.XPATH, '//form').submit()
    time.sleep(3)
    driver.find_element(By.XPATH, '//button').click()
    time.sleep(3)
    print(driver.get_cookies())
    driver.close()