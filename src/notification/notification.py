import schedule
from time import sleep
from src.settings import settings


def main():
    print("Hello! every 5 secs.")


if __name__ == "__main__":
    print(settings.NOTIFICATION_TIME)
    schedule.every(5).seconds.do(main)
    # schedule.every().day.at(time_str=settings.NOTIFICATION_TIME).do(main)
    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        exit(0)
