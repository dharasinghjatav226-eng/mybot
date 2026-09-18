from flask import Flask
import threading
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running - Indore"

def run_web():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_web).start()
import telebot
import google.generativeai as genai
import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_live_weather(city="Indore"):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo = requests.get(geo_url, timeout=10).json()
        if 'results' not in geo: return None
        lat = geo['results'][0]['latitude']
        lon = geo['results'][0]['longitude']
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m"
        w = requests.get(weather_url, timeout=10).json()
        temp = w['current']['temperature_2m']
        wind = w['current']['wind_speed_10m']
        hum = w['current']['relative_humidity_2m']
        return f"{city} ka LIVE Mausam: {temp}°C, Hawa {wind} km/h, Humidity {hum}%"
    except:
        return None

@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        text = message.text.lower()
        if "mausam" in text or "mousam" in text or "weather" in text or "tapman" in text:
            city = "Indore"
            match = re.search(r"(\w+)\s+ka\s+(mausam|mousam|weather|tapman)", text)
            if match:
                city = match.group(1)
            elif "morena" in text: city = "Morena"
            elif "gwalior" in text: city = "Gwalior"
            weather_info = get_live_weather(city.capitalize())
            if weather_info:
                bot.reply_to(message, weather_info)
                return
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

print("ULTIMATE Super Agent ON hai...")
bot.infinity_pollimg() 
