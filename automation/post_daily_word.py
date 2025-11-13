from dotenv import load_dotenv
import os
import requests
from supabase import create_client, Client

load_dotenv()

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
    response = (
        supabase
        .from_("words")
        .select("he, en")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        word = response.data[0]
        return word["he"], word["en"]
    
    return None, None


def send_to_telegram(hebrew, english):
    """Send word to Telegram channel."""
    message = f" *Word of the Day*\n\n🇮🇱 {hebrew}\n🇬🇧 {english}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    requests.post(url, json=payload)


def main():
    he, en = get_word_of_the_day()

    if he:
        send_to_telegram(he, en)
        print(f"✅ Posted: {he} - {en}")
    else:
        print("⚠️ No new word found.")


if __name__ == "__main__":
    main()