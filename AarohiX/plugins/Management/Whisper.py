#تعديل كامل ابو عبيدة @AA37A 
from AarohiX import app as bot
from config import BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("●ᥫᩣ أرسال همسة", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="⦿ همسة ⦿",
                description=f"@{BOT_USERNAME} [ معرف او ايدي ] [ النص ]",
                input_message_content=InputTextMessageContent(f"⦿ الأستخدام:\n\n@{BOT_USERNAME} [ المعرف او الايدي ] [ النص ]"),
                thumb_url="https://graph.org/file/865d7c00a11daae5185fc.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = data.split()[0]
            msg = data.split(None, 1)[1]
            user = await _.get_users(user_id)
            
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("❥ همسة", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("☞ همسة وقتية(مرة واحدة) ", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            
            mm = [
                InlineQueryResultArticle(
                    title="⦿ همسة ⦿",
                    description=f"ارسال الهمسة الى {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"⦿ تم ارسال همسة للحلو  {user.first_name}.\n  💬لأرسال همسة اكتب معرف البوت ثم معرف الشخص ثم (الهمسة) \n ."),
                    thumb_url="https://graph.org/file/865d7c00a11daae5185fc.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="➤ همسة وقتية",
                    description=f"ارسل همسة  وقتية الى  {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"☞ همسة وقتية للحلو  {user.first_name}.\nاكتب النص او الرسالة بشكل سري."),
                    thumb_url="https://graph.org/file/865d7c00a11daae5185fc.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
            
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except Exception as e:
            mm = [
                InlineQueryResultArticle(
                    title="⦿ همسة ⦿",
                    description="خطأ بالمعرف او الايدي!",
                    input_message_content=InputTextMessageContent("خطأ في المعرف اكتب معرف الشخص ثم الهمسة ✨!"),
                    thumb_url="https://graph.org/file/865d7c00a11daae5185fc.jpg",
                    reply_markup=switch_btn
                )
            ]
    
    results.append(mm)
    return results



@bot.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id
    
    if user_id not in [from_user, to_user, 5465943450]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} Is Tʀʏɪɴɢ Tᴏ Oᴘᴇɴ Uʀ Wʜɪsᴘᴇʀ.")
        except Unauthorized:
            pass
        
        return await query.answer(" هاي الهمسة مو الك   𖣘︎", show_alert=True)
    
    search_msg = f"{from_user}_{to_user}"
    
    try:
        msg = whisper_db[search_msg]
    except:
        msg = "𖣘︎ خطأ!\n\nالهمسة تم حذفها من قاعدة البيانات !"
    
    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("أرسل همسة ➻", switch_inline_query_current_chat="")]])
    
    await query.answer(msg, show_alert=True)
    
    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("➤ الهسة  شفتها !\n\nاضغط  على الزر لترسل همسة !", reply_markup=SWITCH)


async def in_help():
    answers = [
        InlineQueryResultArticle(
            title="⦿ همسة سرية ⦿",
            description=f"همسة اكتب  [المعرف او الايدي] [النص]",
            input_message_content=InputTextMessageContent(f"**❍ الأستخدام:**\n\nفقط لمرة واحدة (اكتب معرف الشخص او الأيدي ) (الهمسة).\n\n**استخدام:**\nلمرة واحدة @المعرف  "),
            thumb_url="https://graph.org/file/865d7c00a11daae5185fc.jpg",
            reply_markup=switch_btn
        )
    ]
    return answers


@bot.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    else:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
                                               
