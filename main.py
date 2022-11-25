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
opt.add_argument('user-data-dir=env/userdata_sv')  #For cookies/session
opt.add_extension(EXTENSION_PATH)

driver = webdriver.Chrome(options=opt)

###### MetaMask Login ######
SH.switch_window(driver, 'MetaMask')
MS.metamask_login(driver)

###### Watchers.pro Login ######
SH.switch_window(driver, '') # force switch to the 1st tab.
driver.get('https://watchers.pro/') # Open the website and login
WPS.watcherspro_connect_wallet(driver)
time.sleep(1)

####### Extract data from VC Watch page #######
SH.switch_window(driver, '') # force switch to the 1st tab.
WPS.scrape_vc_watch_overview(driver)

# time.sleep(300)