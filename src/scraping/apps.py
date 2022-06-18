from django.apps import AppConfig


class ScrapingConfig(AppConfig):
    name = 'scraping'
    verbose_name = 'Scraping App'

    def ready(self):
        from scraping import updater
        updater.start()
