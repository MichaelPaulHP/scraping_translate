from models.GoogleTranslate import GoogleTranslate
from models.TranslationScraper import TranslationScraper
from models.definitions.DefinitionsScraper import DefinitionScraper


class GoogleScraper:
    def scraping(self, text: str) -> GoogleTranslate:
        from bs4 import BeautifulSoup
        from selenium import webdriver

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException

        url = "https://translate.google.com/?sl=en&tl=es&op=translate&text=" + text
        browser = webdriver.PhantomJS()
        browser.get(url)
        delay = 2  # seconds
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'Dwvecf')))
            print("Page is ready!")
            print(myElem)
        except TimeoutException:
            print("Loading took too much time!")

        html = browser.page_source
        soup = BeautifulSoup(html)

        a = soup.find_all('div', class_="Dwvecf")
        print(len(a))
        googleTranslate = GoogleTranslate()
        # soup.find_all("div",clashs_="J0lOec") first and last
        principal = soup.find_all("span", class_="VIiyi")
        principal = list(map(lambda t: t.get_text("|"), principal))
        principal = list(map(lambda t: t.split("|")[0], principal))

        googleTranslate.principal = ", ".join(principal)
        for index in range(len(a)):
            option = a[index]
            title = option.h3.get_text()
            if "Translations" in title:
                translation = TranslationScraper.scraping(a[index])
                googleTranslate.translations = translation
            if "Definitions" in title:
                definitions = DefinitionScraper.scraping(a[index])
                googleTranslate.definitions = definitions
        return googleTranslate
