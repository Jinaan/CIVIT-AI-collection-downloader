import os
import time
import fuzzywuzzy
import fuzzywuzzy.process
from selenium.webdriver.common.by import By

from .filterBaseModel import CategorizeModelBase
from .saveModel import saveModel

from .configAccess import getConfig
config = getConfig()
    
A1111_PATH = config["A1111_PATH"]

# Dictionary of model paths
MODELPATH = {
    "LORA": A1111_PATH + "\stable-diffusion-webui\models\Lora",
    "CHECKPOINT": A1111_PATH + "\stable-diffusion-webui\models\Stable-diffusion",
    "HYPERNETWORK": A1111_PATH + "\stable-diffusion-webui\models\hypernetworks",
    "EMBEDDING": A1111_PATH + "\stable-diffusion-webui\embeddings"
}

# FILTERTYPE = ["lora"]  # filter type of models to download. Example: ["lora", "checkpoint", "hypernetwork", "embedding"]	
FILTERTYPE = config.get("FILTERTYPE",[])

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
                
            
            
            # +========================+
            # | Get Model Type         |
            # +========================+
            baseModel = driver.find_elements(By.CSS_SELECTOR, "tr.mantine-1avyp1d")
            print(len(baseModel))
            for iBaseModel in baseModel:
                # print(iBaseModel.text)
                if "Base Model" in iBaseModel.text:
                    # remove the "Base Model" text from the string
                    model = iBaseModel.text.replace("Base Model", "")
                    model = CategorizeModelBase(model)
                if "Trigger Words" in iBaseModel.text:
                    triggerWords = iBaseModel.text.replace("Trigger Words", "")
                    triggerWords = triggerWords.split("\n")
                    triggerWords = [i.strip() for i in triggerWords]
                    # if found empty string, remove it
                    triggerWords = list(filter(None, triggerWords))
                    # combine the trigger words into one string with comma
                    triggerWords = ", ".join(triggerWords)
            
            
            # time.sleep(1000)
            
                
                
            # +============================+
            # | Checking Similarities      |
            # | with FILTER                |
            # +============================+
            print("Checking Model Type of " + modelType.text)
            
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
            dataToSave = {
                "URL": downloadLink,
                "Name": modelTitle.text,
                "model": model,
                "trigger": triggerWords
            }
            saveModel(ParentSave, dataToSave)
            
            continue
        
        except Exception as e:
            print(e)
            # +===========================+
            # | Log the Error             |
            # +===========================+
            with open("error.txt", "a", encoding="utf-8") as f:
                f.write(str(e) + "\n")
            pass
