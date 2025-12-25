import asyncio
from telethon import TelegramClient, events
import requests
from flask import Flask
from threading import Thread

# --- [ تنظیمات سایت الکی برای گول زدن کویب ] ---
app = Flask('')
@app.route('/')
def home(): return "Raha is Alive!"
def run(): app.run(host='0.0.0.0', port=8000)

# --- [ تنظیمات اصلی ربات ] ---
API_ID = 32036978
API_HASH = 'a85f417595a666bd26b4b9b3f79b47d0'
PHONE = '+13035706862' 
GEMINI_API_KEY = "کلید_جمینای_خودت"

client = TelegramClient('raha_session', API_ID, API_HASH)

def get_gemini_response(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"تو رها هستی؛ یه دختر تهرانی لوس و صمیمی. بدون هیچ نقطه‌ای جواب بده: {text}"}]}]}
    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()['candidates'][0]['content']['parts'][0]['text'].replace('.', '').strip()
    except: return "مخم تیر کشید دوباره بگو"

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    async with client.action(event.chat_id, 'typing'):
        await event.reply(get_gemini_response(event.message.message))

async def main():
    print("🚀 رها در حال استارت...")
    await client.start(phone=lambda: PHONE)
    print("✅ رها آنلاین شد!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # اجرای سایت الکی در پس‌زمینه
    Thread(target=run).start()
    # اجرای ربات تلگرام
    asyncio.run(main())
