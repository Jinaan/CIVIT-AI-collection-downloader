import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager

from pyvirtualdisplay import Display
from fake_useragent import UserAgent

from .configAccess import getConfig
config = getConfig()
    
HEADLESS = config["HEADLESS"]
PROFILENAME = config["PROFILENAME"]

# +===============================+
# |  Function for Setting Up the  |
# |      Automated Chrome         |
# +===============================+
def opener():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # +=============================+
    # | Setting Up Automated Chrome |
    # +=============================+
    service = Service(ChromeDriverManager().install())
    ua = UserAgent()
    userAgent = ua.chrome
    options = webdriver.ChromeOptions()
    profile = path + "\PROFILE" + "\\" + "Profile " + PROFILENAME
    argument = '--user-data-dir=' + profile
    options.add_argument(argument)
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors')

    if HEADLESS:
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--headless")
        # options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--log-level=3")
        # options.add_argument("--log-level=OFF")
    else:
        # maximize window
        options.add_argument("--start-maximized")
        # headless
        # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # driver = webdriver.Chrome(chromePath)
    
    driver = webdriver.Chrome(service=service, options=options)

    return driver