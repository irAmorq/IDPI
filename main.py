import asyncio
from telethon import TelegramClient, events
import requests

# --- [ تنظیمات اصلی ] ---
API_ID = 32036978
API_HASH = 'a85f417595a666bd26b4b9b3f79b47d0'
PHONE = '+13035706862' 
# کلید جمینای خودت را اینجا بذار
GEMINI_API_KEY = "AIzaSyBE3d6HPzLO3ZhzsJx5zT-vzh5CplqPOS4"

client = TelegramClient('raha_session', API_ID, API_HASH)

def get_gemini_response(text):
    # آدرس مستقیم API جمینای گوگل
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"تو رها هستی؛ یه دختر تهرانی لوس، بامزه و صمیمی. خیلی کوتاه و بدون هیچ نقطه‌ای جواب بده. پیام کاربر اینه: {text}"
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            ans = result['candidates'][0]['content']['parts'][0]['text']
            # لوس‌سازی: حذف نقطه و علائم
            return ans.replace('.', '').replace('!', '').strip()
        else:
            print(f"Gemini Error: {response.status_code}")
            return "عزیزم مخم سوت کشید دوباره بگو"
    except:
        return "اینترنتم یجوریه فدات شم"

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    async with client.action(event.chat_id, 'typing'):
        answer = get_gemini_response(event.message.message)
        await event.reply(answer)

async def main():
    print("🚀 رها با مغز جمینای در حال بیدار شدن در کویب...")
    await client.start(phone=lambda: PHONE)
    print("✅ رها (Gemini) آنلاین شد!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
