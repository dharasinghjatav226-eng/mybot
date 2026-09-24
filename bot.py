import os
import telebot
import threading
from flask import Flask
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi! Main ChatGPT jaisa bot hu, kuch bhi pucho!")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

threading.Thread(target=run_flask).start()
bot.infinity_polling()
