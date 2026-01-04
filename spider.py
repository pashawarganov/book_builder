import logging
import time

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)
headers = {'User-Agent': 'Mozilla/5.0'}

def get_ranobelib_chapters(
        url: str,
) -> [dict]:
    chapters = []

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--kiosk-printing")

    logging.info("Start scrapping")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)

        is_parce = True

        try:
            while is_parce:
                url = driver.current_url
                logger.info(f"Getting soup from url: {url}")
                time.sleep(3)

                buttons = driver.find_elements(By.CSS_SELECTOR, "button.is-outline")
                if len(buttons) == 2:
                    logger.info("Closing cookie window")
                    buttons[1].click()
                    time.sleep(2)

                soup = BS(driver.page_source, "html.parser")

                name_tmp = soup.find("h1").text.split("-")
                if len(name_tmp) == 2:
                    name = name_tmp[1].strip()
                else:
                    name = ""
                content = [
                    p.text
                    for p in soup.find("div", class_="text-content").find_all("p")
                ]
                chapters.append(
                    {
                        "number": name_tmp[0].strip(),
                        "name": name,
                        "content": "\n  ".join(content),
                        "url": url
                    }
                )
                logger.info(f"Chapter '{'-'.join(name_tmp)}' was added")

                with open("last_parsed.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())

                next_url = [
                    link
                    for link in driver.find_elements(By.CSS_SELECTOR, "a.btn")
                    if "впер" in link.text.lower()
                ]
                if len(next_url) == 1:
                    next_url = next_url[0]
                elif not next_url:
                    pass
                else:
                    next_url = None
                    logger.error("ERROR: More links then expected")

                if next_url:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    next_url.click()
                else:
                    logger.info("No more chapters.")
                    logger.info(f"Last url: {url}")
                    is_parce = False

        except KeyboardInterrupt:
            logger.info("Scraping interrupted manually. Saving what we have...")
        except Exception as e:
            logger.info(f"Error while scraping: {e}")
        finally:
            return chapters


if __name__ == "__main__":
    ranobe_url = "https://ranobelib.me/ru/122448--shadow-slave/read/v1/c1?bid=13947"
    result = get_ranobelib_chapters(ranobe_url)
