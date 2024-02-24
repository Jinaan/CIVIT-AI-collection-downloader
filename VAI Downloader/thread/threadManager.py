import threading
import time
import os

# this part is used to manage the thread, the thread will take a queue of the link data and download it

class threadManager:
    def __init__(self, driver, CardData):
        self.driver = driver
        self.CardData = CardData
        self.threadList = []
        self.threadLock = threading.Lock()
        self.threadCount = 0