import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random

# Load environment variables from .env file
load_dotenv()

# Your bot's token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FLASK_APP_URL = 'https://ecommm-lime.vercel.app'  # Your Flask app URL

# Print the token to verify it's being loaded
print("Bot Token:", TOKEN)




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
        await update.message.reply_text("Hey there, sport! I'm your friendly ol' bot, here to help with a dash of wisdom. Use /products to see what we've got, and /categories to see where everything fits in. Let's see what we can find together!")

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f'{FLASK_APP_URL}/products')
    products = response.json()
    if update.message:
        if products:
            message = "Well, well, let's see what we have here:\n\n"
            for product in products:
                joke = random.choice(PRODUCT_JOKES).format(name=product['name'])
                message += f"Name: {product['name']}\nPrice: ${product['price']}\nCategory: {product['category']}\n{joke}\n\n"
        else:
            message = "Looks like the shelves are empty, kiddo. Maybe it's time to dust off the ol' shopping list."
        await update.message.reply_text(message)

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f'{FLASK_APP_URL}/categories')
    categories = response.json()
    if update.message:
        if categories:
            message = "Ah, the categories. Here's what we used to call 'the essentials':\n\n"
            for category in categories:
                joke = random.choice(CATEGORY_JOKES).format(name=category['name'])
                message += f"Category: {category['name']}\n{joke}\n\n"
        else:
            message = "No categories? Back in my day, we had categories for everything! Guess we'll just have to use our imagination."
        await update.message.reply_text(message)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("products", products))
    application.add_handler(CommandHandler("categories", categories))

    application.run_polling()

if __name__ == '__main__':
    main()
