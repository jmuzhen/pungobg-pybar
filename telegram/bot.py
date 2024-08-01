import os
from datetime import datetime

# Telegram API modules
import telebot
from dotenv import load_dotenv

# Google Gemini API modules
from gemini_api.gemini import Chat, Gemini
from .helpers import *

# optional
from .keep_alive import keep_alive


# Initialisation
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

gemini = Gemini()

rate_limit_users = {}
rate_limit_time = datetime.now()
rate_limit_duration = 60 * 3
rate_limit_count = 10  # per user

KEEP_ALIVE = True  # requires flask to be installed

ensure_history_dir_exists()


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to NUSH! How can I help you today?")


@bot.message_handler(commands=['clear', 'restart'])
def clear(message):
    """Restarts a conversation with the bot, i.e. clears the chat history."""
    user_id = message.from_user.id
    clear_history(user_id)
    bot.reply_to(message, "Chat history cleared. How can I help you today?")


# This is the main function that handles all messages
@bot.message_handler(func=lambda msg: True)
def message_handler(message):
    print(f"{datetime.now()}: Received message: {message.text[:100]}")
    
    # Initialise
    user_id = message.from_user.id
    user_message = {"role": "user", "content": message.text}
    
    # Rate limiting
    global rate_limit_users, rate_limit_time
    if rate_limit_users.get(user_id, 0) >= rate_limit_count:
        bot.reply_to(message, "You are sending too many messages. Please wait a while before retrying.")
        print(f"Rate limit exceeded for user {user_id}")
        return
    
    # get history from storage
    messages = get_history(user_id)
    messages.append(user_message)
    context = Chat(messages)
    gemini.set_context(context)
    
    # cosmetic: set typing status
    bot.send_chat_action(message.chat.id, "typing")
    
    # get response from Gemini
    response = gemini.generate(message.text)
    
    bot.reply_to(message, response)
    
    # update history
    add_to_history(user_id, user_message)
    add_to_history(user_id, {"role": "model", "content": response})
    
    # Update rate limits
    rate_limit_users[user_id] = rate_limit_users.get(user_id, 0) + 1
    if (datetime.now() - rate_limit_time).seconds > rate_limit_duration:
        rate_limit_time = datetime.now()
        rate_limit_users = {}


def run():
    if KEEP_ALIVE:
        keep_alive()
    print("Bot is running")
    bot.infinity_polling()
