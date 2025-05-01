import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from flask import Flask
import threading

# Telegram Bot API Token
API_TOKEN = os.getenv('API_TOKEN')

# Flask Dummy Server (Render Port Binding Fix)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# Start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send any text to generate a logo.")

# Function to generate logo
def generate_logo(update: Update, context: CallbackContext):
    user_text = update.message.text
    chat_id = update.message.chat.id
    
    # Sending action to let user know that the bot is processing
    context.bot.send_chat_action(chat_id=chat_id, action="upload_photo")
    
    # Theme URL for text design
    theme = 'https://textpro.me/create-light-glow-sliced-text-effect-online-1068.html'

    # Sending request to the API for logo generation
    response = requests.post(
        url='https://textpro.vercel.app/api',
        json={'text': user_text, 'theme': theme},
        headers={"Authorization": "TechnoStone"}
    )
    
    if response.status_code == 200:
        result = response.json()
        status = result.get('status', False)
        
        if status:
            logo = result.get('logo', '')
            if logo:
                context.bot.send_photo(
                    chat_id=chat_id,
                    photo=logo,
                    caption="<b>Your Logo Generated</b>",
                    parse_mode="HTML"
                )
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="No logo generated. Please try again.",
                    parse_mode="HTML"
                )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="There was an issue with generating the logo. Please try again later.",
                parse_mode="HTML"
            )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Failed to connect to the API. Please try again later.",
            parse_mode="HTML"
        )

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_logo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    # Start the Flask dummy server
    threading.Thread(target=run).start()
    
    # Run the Telegram bot
    main()