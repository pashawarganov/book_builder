import os

import pandas as pd

from spider import get_ranobelib_chapters, get_jaomix_chapters
from fb2_builder import generate_book
import logging

logging.basicConfig(
    level=logging.INFO,  # або DEBUG, WARNING, ERROR, CRITICAL
    format='[%(asctime)s][%(levelname)-8s] %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler("scrapping.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Logger initialized")


def generate_csv(url: str, file_name: str) -> None:
    if os.path.exists(f"cache/{file_name}.csv"):
        logger.info(f"Found {file_name}.csv")
        old_df = pd.read_csv(f"cache/{file_name}.csv")

        last_chapter = old_df.iloc[-1]
        logger.info(f"Last scrapped chapter {last_chapter['number']}")
        url = last_chapter["url"]
    else:
        old_df = pd.DataFrame(columns=["number", "name", "content", "url"])

    if "ranobelib" in url:
        chapters = get_ranobelib_chapters(url)    # Grab from site
    elif "jaomix" in url:
        chapters = get_jaomix_chapters(url)
    else:
        logger.error(f"Wrong url!!! Scrapper don`t maintain url: {url}")
        return None
    new_df = pd.DataFrame(chapters)
    new_df = new_df[old_df.columns]

    chapters_df = pd.concat([old_df, new_df], ignore_index=True) # Forming into dataframe

    chapters_df = chapters_df.drop_duplicates(subset="number")

    chapters_df.to_csv(f"cache/{file_name}.csv", index=False)
    logger.info(f"CSV file {file_name} was written")


if __name__ == '__main__':
    # ranobe_url = "https://ranobelib.me/ru/150605--lord-of-the-mysteries-2/read/v1/c1?bid=18841&ui=4619610"
    ranobe_url = "https://jaomix.ru/tenevoj-rab/glava-1-koshmar-nachinaetsya/"
    file_name = "shadow-slave_2"
    # generate_csv(ranobe_url, file_name)

    volumes_ci = {
        "Nightmare": 109,
        "Lightseeker": 263,
        "Conspirer": 494,
        "Sinner": 735,
        "Demoness": 884,
        "Dreamweaver": 1034,
        "Second Law": 1115,
        "Eternal Aeon": 1179,
    }
    generate_book(
        "lord-of-the-mysteries-2",
        "Cycle of inevitability",
        "fantasy",
        "Cuttlefish That Loves Diving",
        "2023",
        volumes=volumes_ci,
        image_path="media/circle_cover.jpg"
    )

    volumes_ss = {
        "Child of Shadows": 95,
        "Demon of Change": 350,
        "Prince of Nothing": 600,
        "Chain Breaker": 750,
        "Dread Night": 1060,
        "All the Devils Are Here": 1230,
        "The Tomb of Ariel": 1590,
        "Lord of Shadows": 1840,
        "Throne of War": 2260,
    }
    # generate_book(
    #     "shadow-slave",
    #     "Shadow slave",
    #     "fantasy",
    #     "Guiltythree",
    #     "2022",
    #     volumes=volumes_ss,
    # )
