import telebot
import config

bot = telebot.TeleBot(config.token, threaded=False)

def snd_admins(msg):
    admin_list = []
    courier_list = []
    manager_list = []
    for admin in admin_list:
        bot.send_message(admin, msg)
    for corier in courier_list:
        bot.send_message(corier, msg)
    for manager in manager_list:
        bot.send_message(manager, msg)