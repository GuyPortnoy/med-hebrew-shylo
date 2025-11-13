from pathlib import Path
from dotenv import load_dotenv
import os
import requests
from supabase import create_client, Client

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

# --- Environment variables ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # channel username or ID

if not all([SUPABASE_URL, SUPABASE_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    raise ValueError("Missing environment variables.")


# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_word_of_the_day():
    """Fetch latest word from Supabase."""
    try:
        response = supabase.table("words").select("en, he, rus").order("id", desc=True).limit(1).execute()
        if response.data:
            return response.data[0]
        else:
            print("No data found in 'words' table.")
            return None
    except Exception as e:
        print("Error fetching word from Supabase:", e)
        return None


def send_to_telegram(message: str):
    """Send word to Telegram channel."""

    url = f"https://api.telegram.org/bot8169698787:AAEBNR3Sh5Jg_FBxkk7h5PaWUcEMDKLLlfg/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)
    print(response.json())


def main():
    word = get_word_of_the_day()

    if word is None:
        print("⚠️ No new word found.")
        return

    message = (
            "🗓 <b>Word of the Day</b>\n\n"
            f"🇬🇧 <b>English:</b> {word['en']}\n"
            f"🇮🇱 <b>Hebrew:</b> {word['he']}\n"
            f"🇷🇺 <b>Russian:</b> {word['rus']}"
    )
    send_to_telegram(message)

if __name__ == "__main__":
    main()