import os

import pandas as pd

from spider import get_chapters_list
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


def generate_csv(url):
    file_name = url.split("/")[4].split("--")[1]
    if os.path.exists(f"cache/{file_name}.csv"):
        logger.info(f"Found {file_name}.csv")
        old_df = pd.read_csv(f"cache/{file_name}.csv")

        last_chapter = old_df.iloc[-1]
        logger.info(f"Last scrapped chapter {last_chapter['number']}")
        url = last_chapter["url"]
    else:
        old_df = pd.DataFrame(columns=["number", "name", "content", "url"])

    chapters = get_chapters_list(url)    # Grab from site
    new_df = pd.DataFrame(chapters)
    new_df = new_df[old_df.columns]

    chapters_df = pd.concat([old_df, new_df], ignore_index=True) # Forming into dataframe

    chapters_df = chapters_df.drop_duplicates(subset="number")

    chapters_df.to_csv(f"cache/{file_name}.csv", index=False)
    logger.info(f"CSV file {file_name} was written")

    return file_name


def main():
    ranobe_url = "https://ranobelib.me/ru/122448--shadow-slave/read/v1/c1?bid=13947"
    file_name = generate_csv(ranobe_url)
    # generate_book(
    #     file_name,
    #     "fantasy",
    #     "Guiltythree",
    #     "2022"
    # )

if __name__ == '__main__':
    main()
