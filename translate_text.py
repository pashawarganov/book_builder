from groq import Groq

from settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)
model1 = "llama3-8b-8192"

def translate(text):
    response = client.chat.completions.create(
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
        model=model1
    )

    return response.choices[0].message.content
# g-mini

if __name__ == "__main__":
    with open("t.txt", "r") as file:
        chapter1 = file.read()
    print(translate(chapter1))
