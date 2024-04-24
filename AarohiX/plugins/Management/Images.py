import requests
from requests import get 
from AarohiX import app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto

@app.on_message(filters.command(["صورة"], prefixes=["/", "!", "%", ",", "", ".", "@", "#", ""]))
async def pinterest(_, message):
     chat_id = message.chat.id

     try:
       query= message.text.split(None,1)[1]
     except:
         return await message.reply("**اعطيني اسم الصور ليم البحث عنها في PINTEREST 🔍**")

     images = get(f"https://pinterest-api-one.vercel.app/?q={query}").json()

     media_group = []
     count = 0

     msg = await message.reply(f"يتم البحث عن الصورة في بنترست...")
     for url in images["images"][:6]:
                  
          media_group.append(InputMediaPhoto(media=url))
          count += 1
          await msg.edit(f"=> تم ايجاد الصور يتم الأرسال {count}")

     try:
        
        await app.send_media_group(
                chat_id=chat_id, 
                media=media_group,
                reply_to_message_id=message.id)
        return await msg.delete()

     except Exception as e:
           await msg.delete()
           return await message.reply(f"خطأ : {e}")
