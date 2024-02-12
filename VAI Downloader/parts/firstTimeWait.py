from .configAccess import getConfig
config = getConfig()

FIRSTTIME = config["FIRST_TIME"]

def FirstTimeWAit():
    if FIRSTTIME:
        import time
        print("Please login to your account within 500 seconds")
        given_time = 500
        for i in range(given_time):
            time.sleep(1)
            countdown = str(given_time - i).zfill(3)
            print(countdown, end="\r")
        print("Time's up")
    return