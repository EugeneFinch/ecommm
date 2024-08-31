import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Your bot's token and Flask app URL
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Store your token in an environment variable
API_URL = 'https://ecommm.vercel.app'    # Replace with your actual Vercel URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I can help you manage products.')

async def get_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f'{API_URL}/products')
    if response.status_code == 200:
        products = response.json()
        if products:
            message = "Products:\n"
            for product in products:
                message += f"- {product['name']} (${product['price']}) in {product['category']}\n"
        else:
            message = "No products available."
        await update.message.reply_text(message)
    else:
        await update.message.reply_text('Failed to retrieve products.')

async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) != 3:
        await update.message.reply_text('Usage: /add_product <name> <price> <category>')
        return

    product = {
        'name': args[0],
        'price': float(args[1]),
        'category': args[2]
    }

    response = requests.post(f'{API_URL}/add_product', json=product)
    if response.status_code == 201:
        await update.message.reply_text(f"Product '{product['name']}' added successfully!")
    else:
        await update.message.reply_text('Failed to add product.')

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_products", get_products))
    application.add_handler(CommandHandler("add_product", add_product))

    application.run_polling()

if __name__ == '__main__':
    main()

