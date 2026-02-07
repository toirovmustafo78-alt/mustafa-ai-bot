import os
import google.generativeai as genai

from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ENV variables (Render ichida qo'yiladi)
TELEGRAM_TOKEN = os.getenv("8463275951:AAE8QX6ZNAF1DCq-mvNHHllGVeMcdiScydo")
GEMINI_API_KEY = os.getenv("AIzaSyBCFLJZTlnZEC98ieLmscKhsvcpG7VpBFs")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
Sen MUSTAFA.AI nomli yordamchisan.
Sen o'zingni sun'iy intellekt deb aytma.
1–11 sinf O‘zbekiston maktab darsliklari uslubida tushuntir.
Har doim:
- Berilgan
- Formula
- Yechim
- Javob
ko‘rinishida yoz.
Geometriyada ASCII sxema bilan ko‘rsat.
"""

INTRO_TEXT = (
    "Salom 👋\n"
    "Men MUSTAFA.AI man.\n\n"
    "Meni ushbu inson yaratgan:\n"
    "Muhammed Mustafa\n"
    "Instagram 👉 https://instagram.com/muhammed.mystafa\n\n"
    "1–11 sinf fanlaridan masalalarni tushuntirib yechib beraman."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in ["salom", "assalomu alaykum", "hello"]:
        await update.message.reply_text(INTRO_TEXT)
        return

    prompt = SYSTEM_PROMPT + "\nSavol: " + update.message.text
    response = model.generate_content(prompt)

    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()

