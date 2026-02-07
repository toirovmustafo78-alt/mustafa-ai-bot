import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Sozlamalar ---
# Render.com saytidagi "Environment" bo'limiga o'ting va
# TELEGRAM_TOKEN hamda GOOGLE_API_KEY o'zgaruvchilarini qo'shing.
try:
    TELEGRAM_TOKEN = os.environ['8463275951:AAE8QX6ZNAF1DCq-mvNHHllGVeMcdiScydo']
    GOOGLE_API_KEY = os.environ['AIzaSyBCFLJZTlnZEC98ieLmscKhsvcpG7VpBFs']
except KeyError:
    print("Xatolik: Muhit o'zgaruvchilari (Environment Variables) topilmadi!")
    print("Render.com da TELEGRAM_TOKEN va GOOGLE_API_KEY ni sozlaganingizga ishonch hosil qiling.")
    exit()

# Google AI ni sozlash
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- Funksiyalar ---

# /start buyrug'i uchun javob
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Assalomu alaykum, {user_name}!\n\n"
        f"Men MUSTAFA.AI men. "
        f"Menga istalgan savolingizni yozishingiz mumkin."
    )

# Oddiy matnli xabarlar uchun javob
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Foydalanuvchiga "yozmoqda..." statusini ko'rsatish
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # Gemini AI ga so'rov yuborish
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        await update.message.reply_text(
            "Kechirasiz, hozirda savolingizga javob bera olmayman. "
            "Iltimos, birozdan so'ng qayta urinib ko'ring."
        )

# --- Botni ishga tushirish ---
def main():
    print("Bot ishga tushirilmoqda...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda.")
    application.run_polling()

if __name__ == '__main__':
    main()
