from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from run_scraping import run_scraping


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scraping, 'interval', minutes=360)
    scheduler.start()