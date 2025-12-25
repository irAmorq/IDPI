import asyncio
import os
from telethon import TelegramClient, events
import requests
from flask import Flask
from threading import Thread

# سایت الکی برای زنده نگه داشتن سرور
app = Flask('')
@app.route('/')
def home(): return "Raha is Alive!"
def run():
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

# تنظیمات تلگرام
API_ID = 32036978
API_HASH = 'a85f417595a666bd26b4b9b3f79b47d0'
PHONE = '+13035706862' 
GEMINI_API_KEY = "AIzaSyBE3d6HPzLO3ZhzsJx5zT-vzh5CplqPOS4" # کلیدت رو اینجا بذار

client = TelegramClient('raha_session', API_ID, API_HASH)

async def main():
    print("🚀 رها استارت شد. منتظر دریافت کد تایید...")
    
    # اگر فایل سشن نباشد، تلگرام کد می‌فرستد
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        print("⚠️ کد تایید به تلگرامت فرستاده شد.")
        print("🔴 کد رو همین‌جا توی لاگ‌ها تایپ کن (اگه می‌تونی)")
        
        # این بخش بهت اجازه میده کد رو دستی وارد کنی (اگه کنسول اجازه بده)
        try:
            code = input("Enter the code: ")
            await client.sign_in(PHONE, code)
        except:
            print("❌ نمی‌تونم مستقیم کد رو بگیرم. باید فایل سشن رو آپلود کنی.")
            return

    print("✅ رها با موفقیت آنلاین شد!")
    
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def handler(event):
        # هوش مصنوعی جمینای اینجا صدا زده می‌شود
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": f"تو رها هستی؛ یه دختر لوس تهرانی. پیام: {event.message.message}"}]}]}
        try:
            res = requests.post(url, json=payload, timeout=15).json()
            ans = res['candidates'][0]['content']['parts'][0]['text'].replace('.', '')
            await event.reply(ans)
        except:
            await event.reply("مخم تیر کشید")

    await client.run_until_disconnected()

if __name__ == '__main__':
    Thread(target=run).start()
    asyncio.run(main())
