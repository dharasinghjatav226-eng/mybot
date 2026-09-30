import os
import requests
import telebot
import threading
from flask import Flask
import urllib.parse

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot is running - ChatGPT Mode ON"

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"
        r = requests.get(url, timeout=10)
        return r.text
    except:
        return "Network slow hai"

def ask_ai(question):
    try:
        # Thoda smart prompt taaki {} na aaye
        full_q = f"Tum ek funny Hindi assistant ho. Sawal: {question}"
        encoded = urllib.parse.quote(full_q)
        url = f"https://text.pollinations.ai/{encoded}"
        r = requests.get(url, timeout=15)
        ans = r.text.strip()
        if not ans or ans == "{}" or len(ans) < 2:
            return "Hehe, ek aur suno: Ek aadmi doctor ke paas gaya, bola 'mujhe sab bhool jata hai', doctor bola 'kab se?', aadmi bola 'kab se kya?' 😂"
        return ans
    except:
        return "Thoda wait karo, network slow hai, fir se bolo..."

@bot.message_handler(func=lambda m: True)
def reply_all(message):
    text = message.text.lower()
    
    if "mausam" in text or "weather" in text:
        city = "Indore"
        w = get_weather(city)
        bot.reply_to(message, f"Indore ka mausam: {w} ☁️")
    else:
        ans = ask_ai(message.text)
        bot.reply_to(message, ans)
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()
print("Bot chal raha hai...")
bot.polling()