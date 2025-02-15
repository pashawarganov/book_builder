import base64
import mimetypes
from dataclasses import dataclass

import pandas as pd
from lxml import etree
from pandas import DataFrame


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
        title_p.text = row["chapter"]  # Назва глави


        for par in row["text"].split("\n"):
            text_p = etree.SubElement(section, "p")
            text_p.text = par

    # Додаємо секцію <binary> з base64-обкладинкою
    binary = etree.SubElement(root, f"binary", attrib={
        "id": "cover",
        "content-type": book_info.image_type,
    })
    binary.text = book_info.image

    tree = etree.ElementTree(root)
    tree.write(f"books/{book_info.file_name}.fb2", encoding="utf-8", xml_declaration=True, pretty_print=True)

    print(f"Книга '{book_info.title}' успішно створено!")


def get_volumes(chapters) -> dict:
    """Приймає список глав і повертає словник у форматі volume:last_chapter"""
    gaps = []
    volume = 1
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


def main():
    data_file = "ranobelib.csv"
    image_file = "shadow_slave_cover.jpg"
    image_data = encode_image_to_base64(image_file)
    title = "Shadow slave "
    new_book = Book(
        title=title,
        genre="fantasy",
        author_first_name="Guiltythree",
        author_second_name="",
        year_of_publication="2022",
        file_name=title,
        image = image_data[0],
        image_type = image_data[1]
    )

    df = pd.read_csv(data_file)

    volumes = get_volumes(df["chapter"])

    first_chapter = 0
    for volume, last_chapter in volumes.items():
        new_book.title = title + str(volume)
        new_book.file_name = title + str(volume)
        build_book(df[first_chapter:last_chapter], new_book)
        first_chapter = last_chapter


if __name__ == "__main__":
    main()
