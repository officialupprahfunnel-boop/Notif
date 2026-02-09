import os
import time
import threading
from flask import Flask
import telebot
from telebot.apihelper import ApiTelegramException

# --- CONFIGURATION ---
# These will be set in Render's Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MESSAGE = "Don't procrastinate and don't be lazy! You have a lot to achieve in 2026! 🚀"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- KEEP-ALIVE WEB SERVER ---
@app.route('/')
def home():
    return "Bot is running!", 200

def run_flask():
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- NOTIFICATION LOGIC ---
def send_reminders():
    print("Reminder thread started...")
    while True:
        try:
            bot.send_message(CHAT_ID, MESSAGE)
            print("Reminder sent successfully.")
        except ApiTelegramException as e:
            print(f"Error sending message: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        # Wait for 30 minutes (1800 seconds)
        time.sleep(1800)

if __name__ == "__main__":
    if not TOKEN or not CHAT_ID:
        print("ERROR: BOT_TOKEN or CHAT_ID not found in environment variables.")
    else:
        # Start the reminder loop in a background thread
        reminder_thread = threading.Thread(target=send_reminders, daemon=True)
        reminder_thread.start()
        
        # Start the Flask server (This blocks the main thread and keeps the container alive)
        run_flask()
