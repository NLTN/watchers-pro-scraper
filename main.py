import time
import SeleniumHelper as SH
import MetamaskScript as MS
import WatchersProScript as WPS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

EXTENSION_PATH = '/Users/nguyen/Library/Application Support/Google/Chrome/Default/Extensions/nkbihfbeogaeaoehlefnkodbefgpgknn/10.22.2_0.crx'
opt = webdriver.ChromeOptions()
# opt.headless = True
# opt.add_argument('user-data-dir=env/userdata_sv')  #For cookies/session
opt.add_extension(EXTENSION_PATH)

driver = webdriver.Chrome(options=opt)

# Extensions will load first.
# time.sleep(10)
SH.switch_window(driver, 'MetaMask')
MS.metamask_login(driver)

# Open the website and login
SH.switch_window(driver, '') # switch to any tab. I don't care
driver.get('https://watchers.pro/')
# time.sleep(5)
WPS.watcherspro_connect_wallet(driver)
time.sleep(1)
SH.switch_window(driver, '')

####### Extract data from VC Watch page
driver.implicitly_wait(20)
driver.get('https://watchers.pro/#/vcWatch')
# time.sleep(5)
action = ActionChains(driver)
row_elems = driver.find_elements(By.XPATH, '//tr[@data-row-key]')
for row in row_elems:
    cells = row.find_elements(By.XPATH, './/td')
    # print(f'*************** {cells[1].get_attribute("innerText")} ***************')
    action.click(cells[2]).perform() # Open Address dialog box
    time.sleep(1)
    dialogbox_elem = driver.find_element(By.XPATH, '//div[@role="dialog"]')
    WPS.get_addresses_from_dialogbox(driver, dialogbox_elem)
    time.sleep(2)
    action.send_keys(Keys.ESCAPE).perform()

# time.sleep(300)