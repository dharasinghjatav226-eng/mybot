import os
import telebot
from flask import Flask
import threading
from google import genai

# --- CONFIG ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- BOT LOGIC ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello Gourav! Mai ON hu ✅ Bolo kya kaam hai?")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash"
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Thoda error aaya: {e}")

# --- START ---
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("ULTIMATE Super Agent ON hai...")
    bot.infinity_polling()
