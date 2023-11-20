from pinscrape import pinscrape


class Scrapper:
    def upload_new_batch_pictures(key_word, dir_path, threads, batch_size) -> bool:
        details = pinscrape.scraper.scrape(key_word, dir_path, {}, threads, batch_size)
        return details["isDownloaded"]

    def clean_up_pictures(self):
        pass
