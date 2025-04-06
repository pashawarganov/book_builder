import time

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

headers = {'User-Agent': 'Mozilla/5.0'}


def get_chapters_list(
        url: str,
) -> [BS]:
    chapters = []

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--kiosk-printing")

    print("Start scrapping")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)

        is_parce = True

        while is_parce:
            url = driver.current_url
            print(f"Getting soup from url: {url}")
            time.sleep(5)

            soup = BS(driver.page_source, "html.parser")

            name_tmp = soup.find("h1").text.split("-")
            content = [
                p.text
                for p in soup.find("div", class_="text-content").find_all("p")
            ]
            chapters.append(
                {
                    "number": name_tmp[0].strip(),
                    "name": name_tmp[1].strip(),
                    "content": "\n  ".join(content),
                    "url": url
                }
            )

            with open("last_parsed.html", "w") as f:
                f.write(soup.prettify())
                print("File was written")

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
                print("ERROR: More links then expected")

            if next_url:
                next_url.click()
            else:
                print("No more chapters.")
                print(f"Last url: {url}")
                is_parce = False

    return chapters


if __name__ == "__main__":
    ranobe_url = "https://ranobelib.me/ru/122448--shadow-slave/read/v3/c721?bid=13303&ui=4619610"
    file_name = ranobe_url.split("/")[4].split("--")[1]
    soups = get_chapters_list(ranobe_url)

    for soup in soups:
        print(soup)
