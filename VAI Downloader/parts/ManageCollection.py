import os
import time
import fuzzywuzzy
import fuzzywuzzy.process
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, WebDriverException


from .configAccess import getConfig
config = getConfig()
    
    
    
COLLECTIONURL = config["COLLECTIONURL"]



# +===============================================+
# |     Function to Get All Models in Specified   |
# |                  Collection                   |
# +===============================================+
def ManageCollection(driver):
    driver.get(COLLECTIONURL)
    
    
    # +===================================+
    # | Wait for the Page to Fully Loaded |
    # +===================================+
    # Set the maximum time to wait for the element to appear
    timeout = 10  

    while True:
        try:
            # Wait for the element to be present
            cardContainer = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "mantine-17xdgp7"))
            )

            if cardContainer:
                print("Card container found")
                
            break
        except TimeoutException:
            print("Timed out waiting for the card container. Retrying...")
            driver.refresh()
        except WebDriverException as e:
            print(f"WebDriverException: {e}. Retrying...")
            driver.refresh()
            
    print("page loaded")
    
    
    
    
    # +=========================================+
    # | Define Variables for Card Counting      |
    # +=========================================+
    cardPointer = 0
    cardPointerCount = 0
    
    # +==================================+
    # | Load Up All Cards Before Listing |
    # +==================================+
    while True:
        try:
            time.sleep(10)
            cardLast = driver.find_elements(By.CLASS_NAME, "mantine-17xdgp7")
            if cardLast:
                print("card last found with position on list: " + str(len(cardLast)))
            cardLastPoin = cardLast[-1]
            cardPointer = len(cardLast)
            # move to element using javascript
            driver.execute_script("arguments[0].scrollIntoView();", cardLastPoin)
            print(cardPointerCount)
            if cardPointerCount >= 5:
                break
            
            if cardPointer == len(cardLast):
                cardPointerCount += 1
                
        except Exception as e:
            print(e)
            pass
    
    print("done preprocessing")
    
    # +======================+
    # | Tracing All Cards    |
    # +======================+
    cards = driver.find_elements(By.CLASS_NAME, "mantine-17xdgp7")
    print("cards collected")
    print("cards count: " + str(len(cards)))
    
    # +=======================+
    # | Reversing Card List   |
    # +=======================+
    cards.reverse()
    print("cards reversed")
    print("cards count: " + str(len(cards)))
    
    
    # +======================+
    # | Listing All Cards    |
    # +======================+
    CardData = []
    for iCard in cards:
        try:
            href = iCard.get_attribute("href")
            dataTemp = {
                "href": href
            }
            CardData.append(dataTemp)
        except Exception as e:
            print(e)
            pass
    print("cards data collected")
    
    return CardData