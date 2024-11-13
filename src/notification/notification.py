import schedule
from time import sleep
from src.settings import NOTIFICATION_TIME


def main():
    print("Hello!")


if __name__ == "__main__":
    schedule.every().day.at(NOTIFICATION_TIME).do(main)
    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        exit(0)
