from google.cloud import translate_v2 as google_translate
from groq import Groq

from settings import settings


client_google = google_translate.Client()
client_groq = Groq(api_key=settings.GROQ_API_KEY)


def translate_qroq(text):
    response = client_groq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":
                    f"""
                    That`s fiction web-novel on russian language. 
                    Translate it to Ukraine language:
                    {text} 
                    """
            }
        ],
        model="llama3-8b-8192"
    )

    return response.choices[0].message.content


def translate_google(text):
    result = client_google.translate(text, target_language="uk")
    return result["translatedText"]


if __name__ == "__main__":
    with open("t.txt", "r") as file:
        chapter1 = file.read()

    translated_chapter = translate_google(chapter1)
    with open("new.txt", "w") as file:
        file.write(translated_chapter)
        print("File 'new.txt' created successfully.'")
