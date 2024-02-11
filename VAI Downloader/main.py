from parts.ChromeOpener import opener
from parts.ManageCollection import ManageCollection
from parts.DownloadModel import DownloadModel


def main():
    driver = opener()
    driver.get("https://civitai.com/")

    CardData = ManageCollection(driver)
    
    DownloadModel(driver, CardData)
    
    
    print("done")
    
    driver.quit()



if __name__ == "__main__":
    main()
