from parts.ChromeOpener import opener
from parts.firstTimeWait import FirstTimeWAit
from parts.DownloadModel import DownloadModel
from parts.ManageCollection import ManageCollection
from parts.CheckingFile import checkingFile


def main():
    checkingFile()
    driver = opener()
    driver.get("https://civitai.com/")

    FirstTimeWAit()
    
    CardData = ManageCollection(driver)
    
    DownloadModel(driver, CardData)
    
    
    print("done")
    
    driver.quit()
    checkingFile()
    



if __name__ == "__main__":
    main()
