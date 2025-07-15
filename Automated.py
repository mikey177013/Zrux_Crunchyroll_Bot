# Author (C) @Not_Xyn_Xd
# Channel : https://t.me/GODXSTORRE

import telebot
from telebot import types
import time
import threading
from datetime import datetime, timedelta
import json

API_TOKEN = "7455908121:AAHq9TrEyF-q5x0wONoiVo71q1Q6cK2jSzc"  # Replace with your bot's API token
bot = telebot.TeleBot(API_TOKEN)

# Replace with your group chat ID
GROUP_CHAT_ID = 
ADMIN_USER_IDS = {7832123923}

# Sample data storage for user data
user_data = {}
total_users = set()
service_requests = {}
banned_users = set()

# Define the point cost for each service
service_points = {
    "PRIME VIDEO": 5,
    "Crunchyroll": 1,
}

# Global Channel List
REQUIRED_CHANNELS = ["@crunchyrollacc001"]

# Global variables
bonus_time = {}
previous_menu = {}
last_reminder_time = {}

# Correct Direct Image Link
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxp_4QFVHCBUJNazYfe5-zviUHIu7FvSyjgq7SD9_7LxbthgGKcTNdzTI&s=10"

# Function to check if a user is banned
def check_banned(chat_id):
    return chat_id in banned_users

# Function to create the main menu
def main_menu(chat_id, user_id):
    text = f"""
‍♂ Wᴇʟᴄᴏᴍᴇ  彡[NEW USER彡](tg://user?id={user_id})  
➖➖➖➖➖➖➖➖➖➖➖➖➖  
⌛ Jᴏɪɴ Aʟʟ Cʜᴀɴɴᴇʟs Aɴᴅ Cʟɪᴄᴋ Oɴ Jᴏɪɴᴇᴅ Tᴏ Sᴛᴀʀᴛ Oᴜʀ Bᴏᴛ  
➖➖➖➖➖➖➖➖➖➖➖➖➖  
"""

    markup = types.InlineKeyboardMarkup()
    join_buttons = [
        types.InlineKeyboardButton("Jᴏɪɴ", url="https://t.me/GODXSTORRE")
        
    ]
    joined_button = types.InlineKeyboardButton(" [ Jᴏɪɴᴇᴅ ] ", callback_data="joined")

    markup.add(*join_buttons)
    markup.add(joined_button)

    bot.send_photo(chat_id, IMAGE_URL, caption="Welcome Image")
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

# Function to check if the user has joined all required channels
def check_joined(chat_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, chat_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

def options_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Bᴀʟᴀɴᴄᴇ 💰", "Rᴇғᴇʀ 🥳")
    markup.add("Wɪᴛʜᴅʀᴀᴡ 📩")
    markup.add("Bᴏɴᴜs 🎁", "Sᴜᴘᴘᴏʀᴛ 🆘")
    markup.add("Mᴀɪɴ Mᴇɴᴜ")
    bot.send_message(chat_id, " Cʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ:", reply_markup=markup)
    bot.send_photo(chat_id, IMAGE_URL, caption="Option Image")

# Command handler for /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    main_menu(chat_id, user_id)

# Callback Handler for "Joined" Button
@bot.callback_query_handler(func=lambda call: call.data == "joined")
def joined_handler(call):
    chat_id = call.message.chat.id
    if check_joined(chat_id):
        bot.answer_callback_query(call.id, "✅ Yᴏᴜ ᴀʀᴇ ᴠᴇʀɪғɪᴇᴅ!", show_alert=True)
        bot.send_message(chat_id, " Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs! Yᴏᴜ ʜᴀᴠᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs.")
        bot.send_photo(chat_id, IMAGE_URL, caption="✅ Yᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴠᴇʀɪғɪᴇᴅ!")
        options_menu(chat_id)
    else:
        bot.answer_callback_query(call.id, " Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs!", show_alert=True)

# Function to send reminder to users
def send_reminder(chat_id):
    user = user_data.get(chat_id, {'balance': 0})
    reminder_message = (
        "💡 Rᴇᴍɪɴᴅᴇʀ: Dᴏɴ'ᴛ ғᴏʀɢᴇᴛ ᴛᴏ ᴄʟᴀɪᴍ ʏᴏᴜʀ ᴅᴀɪʟʏ ʙᴏɴᴜs ᴘᴏɪɴᴛs! 🎁\n\n"
        "🏆 Rᴇᴅᴇᴇᴍᴀʙʟᴇ Sᴇʀᴠɪᴄᴇs:\n"
    )
    for service, points in service_points.items():
        reminder_message += f"🔸 {service} - {points} ᴘᴏɪɴᴛs\n"
    bot.send_photo(chat_id, IMAGE_URL, caption=reminder_message)

# Function to check and send reminders
def check_and_send_reminders():
    while True:
        for chat_id in total_users:
            last_reminder = last_reminder_time.get(chat_id)
            if not last_reminder or datetime.now() - last_reminder >= timedelta(hours=24):
                send_reminder(chat_id)
                last_reminder_time[chat_id] = datetime.now()
        time.sleep(3600)

threading.Thread(target=check_and_send_reminders, daemon=True).start()

# Admin commands (ban, unban, delbalance)
@bot.message_handler(commands=['ban'])
def ban_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_message(message.chat.id, "⚠️ Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return
    msg = bot.send_message(message.chat.id, "🔹 Pʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴜsᴇʀ ID ᴛᴏ ʙᴀɴ:")
    bot.register_next_step_handler(msg, process_ban)

def process_ban(message):
    try:
        user_id = int(message.text.strip())
        banned_users.add(user_id)
        bot.send_photo(message.chat.id, IMAGE_URL, caption=f"✅ Uѕer `{user_id}` ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.")
        bot.send_photo(user_id, IMAGE_URL, caption="🚫 Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ.")
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Iɴᴠᴀʟɪᴅ ᴜsᴇʀ ID ғᴏʀᴍᴀᴛ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")

# ... (बाकी कोड जैसा है) ...

@bot.message_handler(commands=['unban'])
def unban_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_message(message.chat.id, "⚠️ Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return
    msg = bot.send_message(message.chat.id, "🔹 Pʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴜsᴇʀ ID ᴛᴏ ᴜɴʙᴀɴ:")
    bot.register_next_step_handler(msg, process_unban)

def process_unban(message):
    try:
        user_id = int(message.text.strip())
        if user_id in banned_users:
            banned_users.remove(user_id)
            bot.send_photo(message.chat.id, IMAGE_URL, caption=f"✅ User {user_id} has been unbanned.")
            bot.send_photo(user_id, IMAGE_URL, caption="🚀 You are back in the game!")
        else:
            bot.send_message(message.chat.id, "⚠️ User ID is not banned.")
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Invalid user ID format. Please try again.")

@bot.message_handler(commands=['delbalance'])
def delbalance_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_message(message.chat.id, "⚠️ You don't have permission to use this command.")
        return
    msg = bot.send_message(message.chat.id, "📛 Please enter the user ID to delete balance:")
    bot.register_next_step_handler(msg, process_delbalance)

def process_delbalance(message):
    try:
        user_id = int(message.text.strip())
        if user_id in user_data:
            user_data[user_id]['balance'] = 0
            bot.send_photo(message.chat.id, IMAGE_URL, caption=f"✅ Balance for user {user_id} has been deleted.")
            bot.send_photo(user_id, IMAGE_URL, caption="⚠️ Your balance has been reset to 0 by an admin.")
        else:
            bot.send_photo(message.chat.id, IMAGE_URL, caption=" User ID not found.")
    except ValueError:
        bot.send_photo(message.chat.id, IMAGE_URL, caption=" Invalid user ID format. Please try again.")

# Function to handle the Redeem button
@bot.message_handler(func=lambda message: message.text == "Wɪᴛʜᴅʀᴀᴡ 📩")
def redeem_handler(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'balance': 0})
    response = (
        "📨 You Can Exchange Your Points for Many Premium Accounts.\n\n"
        f"💰 Your Balance: {user['balance']} Points.\n\n"
        "🔄 Exchange Points for ~"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    service_buttons = [types.KeyboardButton(f"👉 {service} [ {points} Points ]") for service, points in service_points.items()]
    for i in range(0, len(service_buttons), 3):
        markup.add(*service_buttons[i:i+3])
    markup.add(types.KeyboardButton("Bᴀᴄᴋ ᴛᴏ Mᴇɴᴜ"))
    bot.send_photo(chat_id, IMAGE_URL, caption=response, reply_markup=markup)

# Function to handle service selection in the redeem section
@bot.message_handler(func=lambda message: any(service in message.text for service in service_points.keys()))
def service_handler(message):
    chat_id = message.chat.id
    service = next((s for s in service_points.keys() if s in message.text), None)
    if not service:
        bot.send_message(chat_id, "⚠️ Invalid service selection.")
        return
    required_points = service_points[service]
    user = user_data.get(chat_id, {'balance': 0})
    if user['balance'] >= required_points:
        user['balance'] -= required_points
        user_info = bot.get_chat(chat_id)
        username = user_info.username if user_info.username else "N/A"
        forwarded_message_text = f" 𝗨𝘀𝗲𝗿 𝗜𝗗: {chat_id}\n" \
                                f" 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{username}\n" \
                                f" 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱: {service}\n" \
                                f" 𝗣𝗼𝗶𝗻𝘁𝘀: {required_points}"
        sent_message = bot.send_message(GROUP_CHAT_ID, forwarded_message_text)
        service_requests[sent_message.message_id] = chat_id
        try:
            account = get_account(service)
            if account:
                bot.send_message(chat_id, f"✅ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝘆𝗼𝘂𝗿 {service} 𝗔𝗰𝗰𝗼𝘂𝗻𝘁:\n\n{account}\n\n𝗘𝗻𝗷𝗼𝘆! 🎉")
            else:
                bot.send_message(chat_id, f"🙇‍♂️ Nᴏ Mᴏʀᴇ {service} Aᴄᴄᴏᴜɴᴛ Aᴠᴀɪʟᴀʙʟᴇ Nᴏᴡ.\n⚠️ Wᴇ Wɪʟʟ Iɴғᴏʀᴍ Yᴏᴜ Wʜᴇɴ ɪᴛ ᴡɪʟʟ Cᴏᴍᴇ Bᴀᴄᴋ 🥺")
        except Exception as e:
            bot.send_message(chat_id, f"⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱 𝗱𝘂𝗿𝗶𝗻𝗴 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 𝗱𝗲𝗹𝗶𝘃𝗲𝗿𝘆. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝘀𝘂𝗽𝗽𝗼𝗿𝘁. {e}")
    else:
        bot.send_message(chat_id, f"⚠️ 𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 *{required_points} 𝗽𝗼𝗶𝗻𝘁𝘀* 𝘁𝗼 𝗿𝗲𝗱𝗲𝗲𝗺 *{service}*.\n 𝗬𝗼𝘂𝗿 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗯𝗮𝗹𝗮𝗻𝗰𝗲: *{user['balance']} 𝗽𝗼𝗶𝗻𝘁𝘀*.", parse_mode="Markdown")
    previous_menu[chat_id] = "withdraw"

# Function to get account from JSON files
def get_account(service):
    try:
        filename = f"{service.lower()}_accounts.json"
        with open(filename, "r") as f:
            accounts = json.load(f)
        if accounts:
            account = accounts.pop(0)
            with open(filename, "w") as f:
                json.dump(accounts, f)
            return account
        else:
            return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Function to handle the Back button in the withdraw section
@bot.message_handler(func=lambda message: message.text == "Bᴀᴄᴋ ᴛᴏ Mᴇɴᴜ")
def back_to_main_menu(message):
    chat_id = message.chat.id
    if previous_menu.get(chat_id) == "withdraw":
        options_menu(chat_id)
    else:
        bot.send_message(chat_id, "⚠️ Iɴᴠᴀʟɪᴅ ʙᴀᴄᴋ ʙᴜᴛᴛᴏɴ ᴄʟɪᴄᴋ.")

# Function to handle the Refer button
@bot.message_handler(func=lambda message: message.text and message.text.strip() == "Rᴇғᴇʀ 🥳")
def refer_handler(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'invited_users': 0})  # Ensure 'invited_users' exists
    user.setdefault('invited_users', 0) # Set default value 0 if 'invited_users' doesn't exist.
    invite_link = f"https://t.me/Zrux_Generator_bot?start=Bot{chat_id}"
    response = (
        f" <b>𝗧𝗼𝘁𝗮𝗹 𝗥𝗲𝗳𝗲𝗿𝘀:</b> {user['invited_users']} 𝗨𝘀𝗲𝗿(𝘀)\n\n"
        f" <b>𝗬𝗼𝘂𝗿 𝗜𝗻𝘃𝗶𝘁𝗲 𝗟𝗶𝗻𝗸:</b> <a href='{invite_link}'>{invite_link}</a>\n\n"
        f" <b>𝗘𝗮𝗿𝗻 𝟮 𝗣𝗼𝗶𝗻𝘁𝘀 𝗣𝗲𝗿 𝗜𝗻𝘃𝗶𝘁𝗲!</b>\n 𝗦𝗵𝗮𝗿𝗲 𝘄𝗶𝘁𝗵 𝗳𝗿𝗶𝗲𝗻𝗱𝘀 𝗻𝗼𝘄!"
    )
    bot.send_photo(chat_id, IMAGE_URL, caption=response, parse_mode="HTML")

# Function to handle daily bonus command
@bot.message_handler(func=lambda message: message.text and "Bᴏɴᴜs 🎁" in message.text.strip())
def bonus_handler(message):
    try:
        chat_id = message.chat.id
        user = user_data.get(chat_id, {'balance': 0})

        last_bonus_time = bonus_time.get(chat_id)
        if last_bonus_time and datetime.now() - last_bonus_time < timedelta(hours=24):
            time_remaining = timedelta(hours=24) - (datetime.now() - last_bonus_time)
            bot.send_message(chat_id, f"⚠️ You have already claimed your daily bonus. Please wait {time_remaining} before claiming again.")
            return

        bonus_points = 1
        user['balance'] += bonus_points
        user_data[chat_id] = user
        bonus_time[chat_id] = datetime.now()

        # स्टाइलिश संदेश और छवि एक साथ
        message_text = f" Cᴏɴɢʀᴀᴛs , Yᴏᴜ Rᴇᴄᴇɪᴠᴇᴅ {bonus_points} Pᴏɪɴᴛs\n\n Cʜᴇᴄᴋ Bᴀᴄᴋ Aғᴛᴇʀ 24 Hᴏᴜʀs"
        bot.send_photo(chat_id, IMAGE_URL, caption=message_text)

    except Exception as e:
        print(f"Error in bonus_handler: {e}")
        bot.send_message(message.chat.id, f"⚠️ An error occurred: {e}")

# Function to handle the Support button
@bot.message_handler(func=lambda message: message.text == "Sᴜᴘᴘᴏʀᴛ 🆘")
def support_handler(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    support_button = types.InlineKeyboardButton("🔹 Jᴏɪɴ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ 🔹", url="https://t.me/GODXSTORRE")
    markup.add(support_button)
    bot.send_photo(chat_id, IMAGE_URL, caption="🆘 **Hᴇʀᴇ ɪs ᴏᴜʀ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ. Jᴏɪɴ ғᴏʀ ᴀssɪsᴛᴀɴᴄᴇ!**", reply_markup=markup, parse_mode="Markdown")

# Function to handle the Balance button
@bot.message_handler(func=lambda message: message.text == "Bᴀʟᴀɴᴄᴇ 💰")
def balance_handler(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'balance': 0, 'invited_users': 0, 'bonus_claimed': False})
    response = f"""
📌 **Usᴇʀ:** 彡[{message.from_user.first_name}]彡
➖➖➖➖➖➖➖➖➖➖➖➖➖
💰 **Yᴏᴜʀ Bᴀʟᴀɴᴄᴇ:** `{user['balance']:.2f} ᴘᴏɪɴᴛs`
🆔 **Uꜱᴇʀ ɪᴅ:** `{chat_id}`
➖➖➖➖➖➖➖➖➖➖➖➖➖
📣 **Rᴇғᴇʀ Aɴᴅ Eᴀʀɴ Mᴏʀᴇ 📣**
➖➖➖➖➖➖➖➖➖➖➖➖➖
    """
    bot.send_photo(chat_id, IMAGE_URL, caption=response, parse_mode="Markdown")

# Admin command to add balance
@bot.message_handler(commands=['balanceadd'])
def balance_add_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_photo(message.chat.id, IMAGE_URL, caption="⚠️ **Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Uꜱᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ.**", parse_mode="Markdown")
        return
    msg = bot.send_photo(message.chat.id, IMAGE_URL, caption="📝 **Pʟᴇᴀsᴇ Eɴᴛᴇʀ Tʜᴇ Aᴍᴏᴜɴᴛ ᴏғ Pᴏɪɴᴛs ᴀɴᴅ Uꜱᴇʀ ID ɪɴ ᴛʜɪs Fᴏʀᴍᴀᴛ:**\n\n```points user_id```", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_balance_add)

def process_balance_add(message):
    try:
        points, user_id = map(str.strip, message.text.split())
        points = int(points)
        user_id = int(user_id)
        if user_id not in user_data:
            user_data[user_id] = {'balance': 0, 'invited_users': 0, 'bonus_claimed': False}
        user_data[user_id]['balance'] += points
        bot.send_photo(message.chat.id, IMAGE_URL, caption=f"✅ **Sᴜᴄᴄᴇssғᴜʟʟʏ Aᴅᴅᴇᴅ `{points}` Pᴏɪɴᴛs ᴛᴏ Uꜱᴇʀ `{user_id}`'s Bᴀʟᴀɴᴄᴇ.**", parse_mode="Markdown")
        bot.send_photo(user_id, IMAGE_URL, caption=f"🎉 **Yᴏᴜ Hᴀᴠᴇ Rᴇᴄᴇɪᴠᴇᴅ `{points}` Pᴏɪɴᴛs!**\n💰 **Nᴇᴡ Bᴀʟᴀɴᴄᴇ:** `{user_data[user_id]['balance']}` **ᴘᴏɪɴᴛs**", parse_mode="Markdown")
    except ValueError:
        bot.send_photo(message.chat.id, IMAGE_URL, caption="⚠️ **Iɴᴠᴀʟɪᴅ Iɴᴘᴜᴛ Fᴏʀᴍᴀᴛ!**\nPʟᴇᴀsᴇ Uꜱᴇ:\n```points user_id```\n\n**Eᴢ.** `10 123456789`", parse_mode="Markdown")
    except Exception as e:
        bot.send_photo(message.chat.id, IMAGE_URL, caption=f"⚠️ **Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ:**\n```{e}```", parse_mode="Markdown")

# Admin command to broadcast a message
@bot.message_handler(commands=['broadcast'])
def broadcast_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_photo(message.chat.id, IMAGE_URL, caption="⚠️ **Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Uꜱᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ.**", parse_mode="Markdown")
        return
    msg = bot.send_message(message.chat.id, "Please enter the message or send the file to broadcast.")
    bot.register_next_step_handler(msg, lambda m: process_broadcast(m, message.chat.id))

def process_broadcast(message, admin_chat_id):
    failed_users = 0
    for user_id in total_users:
        try:
            if message.content_type == 'text':
                bot.send_photo(user_id, IMAGE_URL, caption=message.text)
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'document':
                bot.send_document(user_id, message.document.file_id, caption=message.caption)
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id, caption=message.caption)
        except Exception as e:
            failed_users += 1
            print(f"❌ Could not send message to {user_id}: {e}")
    bot.send_photo(admin_chat_id, IMAGE_URL, caption=f"✅ **Broadcast Completed!**\n🔹 **Failed Users:** `{failed_users}`", parse_mode="Markdown")

# Admin Reply Handler (For Group Replies)
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.chat.id == GROUP_CHAT_ID)
def admin_reply_handler(message):
    if message.reply_to_message and message.reply_to_message.text and message.reply_to_message.text.startswith("User ID:"):
        user_chat_id_str = message.reply_to_message.text.split(":")[1].strip().split("\n")[0]
        try:
            user_chat_id = int(user_chat_id_str)
            bot.send_photo(user_chat_id, IMAGE_URL, caption=f"💬 **Aᴅᴍɪɴ Rᴇᴘʟɪᴇᴅ:**\n\n{message.text}", parse_mode="Markdown")
        except ValueError as e:
            print(f"Error converting user ID to int: {e}")

# Auto Image Handler (Har message ke saath image)
@bot.message_handler(func=lambda message: True)
def auto_image_response(message):
    try:
        bot.send_photo(message.chat.id, IMAGE_URL, caption=message.text)
    except Exception as e:
        print(f"Error sending auto image: {e}")

# Admin command to add stock
@bot.message_handler(commands=['add_stock'])
def add_stock_handler(message):
    try:
        if message.from_user.id not in ADMIN_USER_IDS:
            bot.send_photo(message.chat.id, IMAGE_URL, caption="⚠️ You are not authorized to use this command.")
            return

        input_text = message.text.strip().split(' ', 1)

        if len(input_text) != 2:
            bot.send_photo(message.chat.id, IMAGE_URL, caption="⚠️ Invalid format. Please use /add_stock service email:pass.")
            return

        service, account_data = input_text

        service = service.replace('/add_stock', '').strip().upper()

        if service not in ["CRUNCHYROLL", "PRIME VIDEO"]:
            bot.send_photo(message.chat.id, IMAGE_URL, caption="⚠️ Invalid service name. Please use Crunchyroll or Prime Video.")
            return

        filename = f"{service.lower()}_accounts.json"
        try:
            with open(filename, "r") as f:
                existing_accounts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_accounts = []

        existing_accounts.append(account_data)

        with open(filename, "w") as f:
            json.dump(existing_accounts, f)

        bot.send_photo(message.chat.id, IMAGE_URL, caption=f"✅ Account successfully added for {service}.")

    except Exception as e:
        print(f"Error in add_stock_handler: {e}")
        bot.send_photo(message.chat.id, IMAGE_URL, caption=f"⚠️ An error occurred: {e}")

# Start polling for updates
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)