import requests
import os
import time
import json
import fuzzywuzzy
import fuzzywuzzy.process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager

from pyvirtualdisplay import Display
from fake_useragent import UserAgent

from dotenv import load_dotenv
load_dotenv()

A1111_PATH = os.getenv("A1111_PATH")

# Dictionary of model paths
MODELPATH = {
    "LORA": A1111_PATH + "\stable-diffusion-webui\models\Lora",
    "CHECKPOINT": A1111_PATH + "\stable-diffusion-webui\models\Stable-diffusion",
    "HYPERNETWORK": A1111_PATH + "\stable-diffusion-webui\models\hypernetworks",
    "EMBEDDING": A1111_PATH + "\stable-diffusion-webui\embeddings"
}

COLLECTIONURL = os.getenv("COLLECTIONURL")

HEADLESS = True        # True for headless, False for not headless
PROFILENAME = "2"       # profile name to use for the browser

PATH = os.path.dirname(__file__)


FILTERTYPE = ["lora"]  # filter type of models to download. Example: ["lora", "checkpoint", "hypernetwork", "embedding"]	



# +===============================================+
# |     Define a Custom Scoring Function for      |
# |                Partial Ratio                  |
# +===============================================+
# def custom_scorer(query, choices):
#     return [(fuzzywuzzy.fuzz.partial_ratio(query, choice), choice) for choice in choices]
def custom_scorer(query, choices):
    return [(fuzzywuzzy.fuzz.partial_ratio(query, choice), choice) for choice in choices]


# +===============================+
# |  Function for Setting Up the  |
# |      Automated Chrome         |
# +===============================+
def opener(name, path):
    # +=============================+
    # | Setting Up Automated Chrome |
    # +=============================+
    service = Service(ChromeDriverManager().install())
    ua = UserAgent()
    userAgent = ua.chrome
    options = webdriver.ChromeOptions()
    profile = path + "\PROFILE" + "\\" + "Profile " + name
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

# +===============================================+
# |     Function to Get All Models in Specified   |
# |                  Collection                   |
# +===============================================+
def ManageCollection(driver, url):
    driver.get(url)
    
    
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

# +==============================+
# |  Function to Manage the      |
# |  Downloading of Models       |
# +==============================+
def DownloadModel(driver, CardData):
    for iCardData in CardData:
        try:
            driver.get(iCardData["href"])
            
            while "503 Service Temporarily Unavailable" in driver.page_source:
                driver.refresh()
            
            
            # +========================+
            # | Get Model Name         |
            # +========================+
            while True:
                try:
                    time.sleep(1)
                    modelTitle = driver.find_element(By.CLASS_NAME, "mantine-1uncs0m")
                    break
                except:
                    pass
            print("Trying: " + modelTitle.text)
            
            
            # +========================+
            # | Get Model Type         |
            # +========================+
            while True:
                try:
                    time.sleep(1)
                    modelType = driver.find_element(By.CLASS_NAME, "mantine-1cvam8p")
                    break
                except:
                    pass
                
                
            # +============================+
            # | Checking Similarities      |
            # | with FILTER                |
            # +============================+
            print("Checking Model Type of " + modelType.text)
            
            # result = fuzzywuzzy.process.extractOne(modelType.text.lower(), FILTERTYPE, scorer=custom_scorer)
            result = fuzzywuzzy.process.extractOne(modelType.text.lower(), FILTERTYPE)
            # Check if a matching filter was found with sufficient similarity
            if result[1] is not None and result[1] > 80:
                # ParentSave was MODELPATH that was contain similarity minimum 80% with modelType.text
                ParentSave = MODELPATH[result[0].upper()]
            else:
                continue
            
            
            # +==============================+
            # | Skip Download if File Exists |
            # +==============================+
            if os.path.exists(os.path.join(ParentSave, modelTitle.text + ".safetensors")):
                continue
                
                
                
            downloadLink = None
            
            # +=======================================+
            # | First Attempt to Get Download Link    |
            # +=======================================+
            tryCount = 0
            while True:
                try:
                    time.sleep(1)
                    downloadButton = driver.find_element(By.CLASS_NAME, "mantine-1hmczuy")
                    downloadLink = downloadButton.get_attribute("href")
                    break
                except:
                    tryCount += 1
                    print("Try count Value: " + str(tryCount))
                    if tryCount >= 5:
                        break
                    pass
                
            # +=======================================+
            # | Second Attempt to Get Download Link   |
            # +=======================================+
            if downloadLink == None:
                tryCount = 0
                while True:
                    try:
                        time.sleep(1)
                        downloadButton = driver.find_element(By.CLASS_NAME, "mantine-rm-target").click()
                    except Exception as e:
                        # print(e)
                        continue
                    try:
                        time.sleep(2)
                        downloadButton = driver.find_element(By.CLASS_NAME, "mantine-mlp7hg")
                        time.sleep(2000)
                        downloadLink = downloadButton.get_attribute("href")
                        break
                    except Exception as e:
                        print(e)
                        time.sleep(5)
                        tryCount += 1
                        if tryCount >= 5:
                            break
                        pass
                    
            # +====================================+
            # | Gave Up on Finding Download Link   |
            # +====================================+
            if downloadLink == None:
                continue
            
            # +===========================+
            # | Downloading the Model     |
            # +===========================+
            saveModel(ParentSave, modelTitle.text, downloadLink)
            
            continue
        
        except Exception as e:
            print(e)
            # +===========================+
            # | Log the Error             |
            # +===========================+
            with open("error.txt", "a", encoding="utf-8") as f:
                f.write(str(e) + "\n")
            pass

# +===============================+
# |   Function to Download and    |
# |        Save the Model         |
# +===============================+
def saveModel(PathSave, name, downloadUrl):
    print("Saving Model: " + name)
    modelName = name
    # +==================================+
    # | Removing Unnecessary Symbols     |
    # | on the Model Name                |
    # +==================================+
    modelName = modelName.replace("/", " ")
    modelName = modelName.replace("\\", " ")
    modelName = modelName.replace("|", " ")
    modelFormat = ".safetensors"
    
    modelFolder = PathSave
    # +===========================+
    # | Downloading the Model     |
    # +===========================+
    rs = requests.get(downloadUrl)
        
    # +===========================+
    # | Saving the Model          |
    # +===========================+
    with open(os.path.join(modelFolder, modelName + modelFormat), "wb") as f:
        f.write(rs.content)




def main():
    driver = opener(PROFILENAME, PATH)
    driver.get("https://civitai.com/")

    CardData = ManageCollection(driver, COLLECTIONURL)
    
    DownloadModel(driver, CardData)
    
    
    print("done")
    
    driver.quit()



if __name__ == "__main__":
    main()