import os
import requests
import telebot
import urllib.parse

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"
        r = requests.get(url, timeout=10)
        return r.text
    except:
        return None

def ask_ai(question):
    try:
        q = urllib.parse.quote(question)
        url = f"https://text.pollinations.ai/{q}?system=You are a helpful assistant. Answer in Hindi if user speaks Hindi."
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🙏 Namaste! Main Smart Bot hu.\nMujhse kuch bhi pucho - Mausam, Padhai, Joke sab!")

@bot.message_handler(func=lambda m: True)
def all_reply(m):
    text = m.text
    lower = text.lower()

    if "mausam" in lower or "weather" in lower:
        city = "Indore"
        for w in text.split():
            if w.lower() not in ["ka","kya","hai","mausam","weather","batao","ka"]:
                if len(w) > 2:
                    city = w
        bot.send_chat_action(m.chat.id, 'typing')
        w = get_weather(city)
        bot.reply_to(m, f"🌤️ {city} ka mausam: {w}" if w else "City nahi mila")
        return

    bot.send_chat_action(m.chat.id, 'typing')
    ans = ask_ai(text)
    bot.reply_to(m, ans if ans else "Network issue hai, fir se pucho")

print("Bot Chal Raha Hai...")
bot.infinity_polling()