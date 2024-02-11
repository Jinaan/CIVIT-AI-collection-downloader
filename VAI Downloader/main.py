from parts.ChromeOpener import opener
from parts.ManageCollection import ManageCollection
from parts.DownloadModel import DownloadModel
from parts.configAccess import getConfig
config = getConfig()

FIRSTTIME = config["FIRST_TIME"]

def main():
    driver = opener()
    driver.get("https://civitai.com/")

    if FIRSTTIME:
        import time
        print("Please login to your account within 500 seconds")
        given_time = 500
        for i in range(given_time):
            time.sleep(1)
            countdown = str(given_time - i).zfill(3)
            print(countdown, end="\r")
        print("Time's up")
    CardData = ManageCollection(driver)
    
    DownloadModel(driver, CardData)
    
    
    print("done")
    
    driver.quit()



if __name__ == "__main__":
    main()
