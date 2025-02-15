import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROJECT_NAME: str = "Book Builder"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")


settings = Settings()
