import base64
import logging
import mimetypes
from dataclasses import dataclass

import pandas as pd
from lxml import etree
from pandas import DataFrame, Series

logger = logging.getLogger(__name__)


@dataclass
class Book:
    title: str
    genre: str
    author_first_name: str
    author_second_name: str
    year_of_publication: str
    file_name: str
    image: base64
    image_type: mimetypes


def build_book(data: DataFrame, book_info: Book):
    NS_FB2 = "http://www.gribuser.ru/xml/fictionbook/2.0"
    NS_XLINK = "http://www.w3.org/1999/xlink"

    etree.register_namespace("l", NS_XLINK)
    root = etree.Element(
        "FictionBook",
        xmlns=NS_FB2,
        l = NS_XLINK
    )

    description = etree.SubElement(root, "description")
    title_info = etree.SubElement(description, "title-info")

    genre = etree.SubElement(title_info, "genre")
    genre.text = book_info.genre

    author = etree.SubElement(title_info, "author")
    first_name = etree.SubElement(author, "first-name")
    first_name.text = book_info.author_first_name

    book_title = etree.SubElement(title_info, "book-title")
    book_title.text = book_info.title

    date = etree.SubElement(title_info, "date")
    date.text = book_info.year_of_publication

    coverpage = etree.SubElement(title_info, "coverpage")
    etree.SubElement(coverpage, "image", attrib={"href": "#cover"})

    body = etree.SubElement(root, "body")
    for _, row in data.iterrows():
        section = etree.SubElement(body, "section")

        title = etree.SubElement(section, "title")
        title_p = etree.SubElement(title, "p")
        if not row["name"] or row["name"] is float:         # Назва глави
            title_p.text = row["number"]
        else:
            try:
                title_p.text = row["number"] + " - " + row["name"]
            except:
                pass


        for par in row["content"].split("\n"):
            text_p = etree.SubElement(section, "p")
            text_p.text = par

    if book_info.image and book_info.image_type:
        # Додаємо секцію <binary> з base64-обкладинкою
        binary = etree.SubElement(root, f"binary", attrib={
            "id": "cover",
            "content-type": book_info.image_type,
        })
        binary.text = book_info.image

    tree = etree.ElementTree(root)
    tree.write(f"books/{book_info.file_name}.fb2", encoding="utf-8", xml_declaration=True, pretty_print=True)

    logging.info(f"Книга '{book_info.title}' успішно створено!")


def get_volumes(chapters: Series) -> dict:
    """
    Приймає список глав і повертає словник у форматі volume:last_chapter
    Example:
        chapters = ["Том 1 Глава 1", "Том 1 Глава 2", ..., "Том 6 Глава 990"]
        volumes = {1: 109, 2: 263, 3: 494, 4: 735, 5: 884, 6: 990}
    """
    gaps = []
    volume = 1
    i = 0
    for i, chapter in enumerate(chapters):
        if f"Том {volume + 1}" in chapter:
            gaps.append(i)
            volume += 1
    gaps.append(i + 1)

    start = 0
    i = 0
    while i < len(gaps):
        if gaps[i] - start > 300:
            new_gap = (gaps[i] - start) // 2
            gaps = gaps[:i] + [gaps[i] - new_gap] + gaps[i:]
            i = 0
            start = 0
        else:
            start = gaps[i]
            i += 1

    return {i + 1:gap for i, gap in enumerate(gaps)}

def encode_image_to_base64(image_path):
    """Зчитує зображення, кодує у base64 і визначає MIME-тип."""
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError("Не вдалося визначити MIME-тип файлу")

    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")

    return encoded_string, mime_type


def generate_book(
        file_name: str,
        book_name: str,
        genre: str = "No genre",
        author: str = "No author",
        year_of_publication: str = "0000",
        image_path: str = None,
        volumes: dict = None,
):
    logging.info("Starting book generation")

    if not image_path:
        image_path = f"media/{file_name}_cover.jpg"
    try:
        image_data = encode_image_to_base64(image_path)
    except Exception as e:
        logging.error(f"Can`t set cover for this book. Error: {e}")
        image_data = (None, None)

    title = book_name + " "
    author_tmp = author.split()
    author_f = author_tmp[0]
    if len(author_tmp) == 1:
        author_s = ""
    else:
        author_s = author_tmp[1:]

    new_book = Book(
        title=title,
        genre=genre,
        author_first_name=author_f,
        author_second_name=author_s,
        year_of_publication=year_of_publication,
        file_name=title,
        image = image_data[0],
        image_type = image_data[1]
    )

    data_file = f"cache/{file_name}.csv"
    df = pd.read_csv(data_file)
    last_number = df['number'].iloc[-1]
    try:
        last_number = int(last_number.split()[-1])
    except Exception as e:
        logging.error(f"Can`t get last chapter number from df. Error: {e}")
        last_number = len(df)

    if not volumes:
        volumes = get_volumes(df["number"])

    first_chapter = 0
    for volume, last_chapter in volumes.items():
        if last_chapter > last_number:      # TODO break
            logging.info(f"Chapter {last_chapter} not in the csv file! Set {last_number} as last chapter.")
        new_book.title = title + " - " + str(volume)
        new_book.file_name = title + " - " + str(volume)
        build_book(df[first_chapter:last_chapter], new_book)
        first_chapter = last_chapter


if __name__ == "__main__":
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
    generate_book(
        "shadow-slave",
        "Shadow slave",
        "fantasy",
        "Guiltythree",
        "2022",
        volumes=volumes_ss,
    )
    # generate_book(
    #     "lord-of-the-mysteries-2",
    #     "Cycle of inevitability",
    #     "fantasy",
    #     "Cuttlefish That Loves Diving",
    #     "2023",
    #     image_path="media/circle_cover.jpg",
    #     volumes=volumes,
    # )
