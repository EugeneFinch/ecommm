import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Your bot's token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Flask API URL
FLASK_APP_URL = 'https://ecommm-lime.vercel.app'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /products to see all products and /categories to see all categories.')

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f'{FLASK_APP_URL}/products')
    products = response.json()
    if products:
        message = "Here are the available products:\n\n"
        for product in products:
            message += f"Name: {product['name']}\nPrice: ${product['price']}\nCategory: {product['category']}\n\n"
    else:
        message = "No products available."
    await update.message.reply_text(message)

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f'{FLASK_APP_URL}/categories')
    categories = response.json()
    if categories:
        message = "Here are the available categories:\n\n"
        for category in categories:
            message += f"Category: {category['name']}\n"
    else:
        message = "No categories available."
    await update.message.reply_text(message)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("products", products))
    application.add_handler(CommandHandler("categories", categories))

    application.run_polling()

if __name__ == '__main__':
    main()

