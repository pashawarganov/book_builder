# 📚 Novel Scraper & FB2 Converter 🚀

This project consists of a web scraper built with Scrapy to collect novel chapters and save them into a CSV file. The collected chapters are then used to generate an FB2 e-book. Additionally, a script is included to translate specific chapters using GroqAI or Google Translate.

## 🌟 Features
- 🕵️ Scrapes novel chapters from a specified website.
- 📝 Saves the collected data in a CSV file with columns `chapter` (chapter number) and `text` (chapter content).
- 📖 Converts the CSV data into an FB2 e-book.
- 🌍 Supports translation of individual chapters.

## 📂 Project Structure
```
project_root/
│── spiders/
│   └── ranobelib.py  # 🕷️ Scrapy spider for novel scraping
│── fb2_builder.py    # 📚 Converts CSV data into an FB2 file
│── translate.py      # 🌎 Translates chapters using GroqAI or Google Translate
│── requirements.txt  # 📦 Required dependencies
│── ranobelib.csv     # 📄 Output CSV file with scraped chapters
│── README.md         # 📘 This file
```

## 🛠️ Setup
### 1️⃣ Install Dependencies
Ensure you have Python installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure the Scraper
- Open `spiders/ranobelib.py` and insert the link to the first chapter of the novel.
- Adjust settings as needed.

### 3️⃣ Configure FB2 Metadata
- Open `fb2_builder.py` and set the book details (title, author, etc.).

### 4️⃣ Run the Scraper
Execute the following command to start scraping and save the results to `ranobelib.csv`:
```bash
scrapy crawl ranobelib -O ranobelib.csv
```

### 5️⃣ Convert to FB2
Once the data is scraped, generate an FB2 e-book:
```bash
python fb2_builder.py
```

### 6️⃣ Translate Chapters (Optional)
Use `translate.py` to translate specific chapters:
```bash
python translate.py
```

## 🔎 Notes
- 🔗 The scraper starts from the URL specified in `spiders/ranobelib.py`.
- 📂 The FB2 generator reads `ranobelib.csv` to create an e-book.
- ⚙️ Translation requires configuring Google Cloud Translation API or GroqAI.

## 📜 License
This project is open-source and can be modified as needed.

