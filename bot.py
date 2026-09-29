import os
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        r = requests.get(url, timeout=10)
        return r.text
    except:
        return None

def ask_ai(question):
    try:
        # Ye FREE ChatGPT jaisa API hai
        url = f"https://text.pollinations.ai/{question}"
        r = requests.get(url, timeout=15)
        return r.text
    except:
        return "Thoda wait karo, soch raha hu..."

@bot.message_handler(func=lambda m: True)
def reply_all(message):
    text = message.text.lower()
    
    # Agar mausam pucha to mausam
    if "mausam" in text or "weather" in text:
        city = message.text.split()[-1]
        if city.lower() in ["mausam","weather"]: city = "Indore"
        w = get_weather(city)
        bot.reply_to(message, f"{city} ka mausam: {w}")
    else:
        # Baki sab sawal ChatGPT ki tarah
        ans = ask_ai(message.text)
        bot.reply_to(message, ans)

print("Bot chal raha hai...")
bot.infinity_polling()