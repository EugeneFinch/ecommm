import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random

# Your bot's token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Flask API URL
FLASK_APP_URL = 'https://ecommm-lime.vercel.app'

# Grandpa Joe Biden-inspired responses
PRODUCT_JOKES = [
    "Well, you know, back in my day, a {name} was a luxury. We made do with a good ol' piece of string!",
    "Ah, {name}, I remember when these first came out. We thought it was the future, and you know what? It still is.",
    "Now listen here, champ. You can't go wrong with a {name}. Trust your ol' grandpa on this one."
]

CATEGORY_JOKES = [
    "Categories? Well, back in the day, we just called it 'stuff.' But let me tell ya, this {name} stuff is top-notch.",
    "The {name} category, huh? Reminds me of the time we had to make do with just a stick and some imagination.",
    "Now, {name} is what the cool kids are into these days, I hear. Not that I know what that means, but it sounds pretty neat."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Hey there, sport! I'm your friendly ol' bot, here to help with a dash of wisdom. Use /products to see what we've got, /categories to see where everything fits in, and /help if you need a bit of guidance. Let's see what we can find together!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Here's what I can help you with, kiddo:\n"
                                        "- /products: List all the products we have in store.\n"
                                        "- /categories: Show you the different categories of products.\n"
                                        "Just pick one and ol' Grandpa Joe will tell you all about it!")

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(f'{FLASK_APP_URL}/products')
        response.raise_for_status()  # Raise an error for bad status codes
        products = response.json()

        if products:
            message = "Well, well, let's see what we have here:\n\n"
            for product in products:
                joke = random.choice(PRODUCT_JOKES).format(name=product['name'])
                message += f"Name: {product['name']}\nPrice: ${product['price']}\nCategory: {product['category']}\n{joke}\n\n"
        else:
            message = "Looks like the shelves are empty, kiddo. Maybe it's time to dust off the ol' shopping list."

    except requests.RequestException as e:
        message = "Ah, looks like we're having some technical difficulties, kiddo. Maybe try again in a bit."
        print(f"Error fetching products: {e}")

    if update.message:
        await update.message.reply_text(message)

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(f'{FLASK_APP_URL}/categories')
        response.raise_for_status()  # Raise an error for bad status codes
        categories = response.json()

        if categories:
            message = "Ah, the categories. Here's what we used to call 'the essentials':\n\n"
            for category in categories:
                joke = random.choice(CATEGORY_JOKES).format(name=category['name'])
                message += f"Category: {category['name']}\n{joke}\n\n"
        else:
            message = "No categories? Back in my day, we had categories for everything! Guess we'll just have to use our imagination."

    except requests.RequestException as e:
        message = "Well, looks like the wires got crossed somewhere, champ. Can't get the categories right now."
        print(f"Error fetching categories: {e}")

    if update.message:
        await update.message.reply_text(message)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("products", products))
    application.add_handler(CommandHandler("categories", categories))

    application.run_polling()

if __name__ == '__main__':
    main()
