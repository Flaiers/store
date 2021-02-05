# -*- coding: utf8 -*-
import telebot
import config
import botmenu
import time
import logging
import dbprocessing
import telethon
import snd
import string
import random
import os
import csv
from threading import Thread
import datetime
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot(config.token, threaded=False)


@bot.message_handler(commands=['start'])
def start_message(message):
    userid = message.chat.id
    username = str(message.chat.username)
    firstnameuser = str(message.chat.first_name)
    rmessage = message.text
    refer = str(rmessage[6:])
    newuser = str(dbprocessing.checkunicusers(userid))  
    print(newuser)
    if len(newuser) < 3:
        dbprocessing.adduser(userid, username, firstnameuser)
        if refer != '':
            print(refer)
            msgid = refer[1:]
            try:
                dbprocessing.addUserToRefList(message.chat.id, refer)
                messagetoref = 'По вашей партнерской ссылке зарегистрировался пользователь ' + str(firstnameuser)
                bot.send_message(msgid, messagetoref)
            except Exception as e:
                print(e)
            bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=botmenu.markhomemenu)
        #dbprocessing.insert_dlv_type(message.chat.id)
        #enter_phone_num = 'Введите актуальный Номер Телефона для связи курьеру'
        #bot.send_message(message.chat.id, enter_phone_num, reply_markup=botmenu.marknext)
        #bot.register_next_step_handler(message, add_phone_number)
        else:
            bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=botmenu.markhomemenu)
    else:
        bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=botmenu.markhomemenu)


def add_phone_number(message):
    phone_number = message.text
    if phone_number != 'Пропустить' and phone_number.isdigit():
        dbprocessing.adduserphone(message.chat.id, phone_number)
        bot.send_message(message.chat.id, 'Отлично, теперь введи адресу доставки: ', reply_markup=botmenu.marknext)
        bot.register_next_step_handler(message, add_delivery_address)
    elif phone_number == 'Пропустить':
        bot.send_message(message.chat.id, 'Отлично, теперь введи адресу доставки: ', reply_markup=botmenu.marknext)
        bot.register_next_step_handler(message, add_delivery_address)
    else:
        bot.send_message(message.chat.id, 'Вы допустили ошибку при вводе, повторите попытку: ', reply_markup=botmenu.marknext)
        bot.register_next_step_handler(message, add_phone_number)

def add_delivery_address(message):
    address_delivery = str(message.text)
    user_chat_id = str(message.chat.id)
    if address_delivery != 'Пропустить':
        dbprocessing.update_user_address(user_chat_id, address_delivery)
        bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=botmenu.markhomemenu)
    else:
        bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=botmenu.markhomemenu)


#region admin
@bot.message_handler(func=lambda message: message.text == "gotoap")
def gotoap(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin' or get_status == 'manager':
        bot.send_message(message.chat.id, 'Вы в панели администратора', reply_markup=botmenu.markadminmenu)

@bot.message_handler(func=lambda message: message.text == "Админ меню")
def go_to_adminmenu(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        bot.send_message(message.chat.id, 'Меню администратора', reply_markup=botmenu.markadminmenu)

@bot.message_handler(func=lambda message: message.text == "Отчет по пользователям")
def user_stat(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        stat_message = str(dbprocessing.get_stat())
        print(stat_message)
        bot.send_message(message.chat.id, stat_message, reply_markup=botmenu.markadminmenu)

@bot.message_handler(func=lambda message: message.text == "Отчет по заказам")
def orders_stat(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        try:
            money = dbprocessing.day_orders_summ()
            msg_text = 'Отчет по заказам: \nЗаказов сегодня: ' + str(dbprocessing.day_orders_count()) + \
                '\nНа сумму: %.2f' % money
            bot.send_message(message.chat.id, msg_text)
        except:
            msg_text = 'Отчет по заказам: \nЗаказов сегодня: 0\nНа сумму: 0'
            bot.send_message(message.chat.id, msg_text)

@bot.message_handler(func=lambda message: message.text == "Другие операции")
def other_operation(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        bot.send_message(message.chat.id, 'Выбери операцию', reply_markup=botmenu.other_admin_menu)

@bot.message_handler(func=lambda message: message.text == "Изменить роль пользователя")
def edit_user_status(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        bot.send_message(message.chat.id, 'Введите id пользователя (попросити его написать боту \'my_chatid\':')
        bot.register_next_step_handler(message, conf_user_status_edit)

def conf_user_status_edit(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        user_id = message.text
        bot.send_message(message.chat.id, 'Выберите новою роль пользователя')
        bot.send_message(message.chat.id, str(user_id), reply_markup=botmenu.edit_user_status)

@bot.message_handler(func=lambda message: message.text == "Рассылка")
def sender(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        bot.send_message(message.chat.id, 'Введите текст:')
        bot.register_next_step_handler(message, sender_menu)

def sender_menu(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        text_message = message.text
        bot.send_message(message.chat.id, text_message, reply_markup=botmenu.sender_admin_menu)

@bot.message_handler(func=lambda message: message.text == "СМС Пользователю")
def send_user(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        bot.send_message(message.chat.id, "Введите chatid: ",  reply_markup=botmenu.markadminmenu)
        bot.register_next_step_handler(message, tochatid)

def tochatid(message):
    config.usersmschatid = message.text
    bot.send_message(message.chat.id, "Тепер введите текст: ")
    bot.register_next_step_handler(message, smstouser)

def smstouser(message):
    messagetext = message.text
    bot.send_message(config.usersmschatid, messagetext)

@bot.message_handler(func=lambda message: message.text == "Товары")
def product_oper(message):
    msg_id = message.chat.id
    get_status = dbprocessing.check_to_admin(msg_id)
    if get_status == 'admin':
        bot.send_message(message.chat.id, "Выберите операцию с товарами",  reply_markup=botmenu.product_operations)

#endregion


@bot.message_handler(func=lambda message: message.text in dbprocessing.get_br())
def mello_brand(message):
    brand_name = message.text
    asotriment_menu = telebot.types.InlineKeyboardMarkup()
    item_list = dbprocessing.print_item(brand_name)
    for test in item_list:
        prod_name = str(test[0])
        print(prod_name)
        qavi = int(dbprocessing.get_aviable_product(brand_name, test[0]))
        qbasket = str(dbprocessing.get_count_item(message.chat.id, test[0]))
        namebutton = telebot.types.InlineKeyboardButton(text=test[0], callback_data='name')
        plus_callback = 'plus' + str(test[0])
        plusbutton = telebot.types.InlineKeyboardButton(text='➕', callback_data=plus_callback)
        qbutton = telebot.types.InlineKeyboardButton(text=qbasket, callback_data='qantity')
        minus_callback = 'mnus' + str(test[0])
        minusbutton = telebot.types.InlineKeyboardButton(text='➖', callback_data=minus_callback)
        if  qavi > 0:
            asotriment_menu.row(namebutton, plusbutton, qbutton, minusbutton)
    photo_name = 'product_image/' + str(brand_name) + '.png'
    cat_name = str(dbprocessing.get_category_name(brand_name))
    msg_text = cat_name + ' ' + brand_name
    try:
        photo = open(photo_name, 'rb')
        bot.send_photo(message.chat.id, photo, caption=msg_text, reply_markup=asotriment_menu)
        photo.close()
        bot.send_message(message.chat.id, 'Выставляя количество вы добавляете товары в корзину', reply_markup=botmenu.open_basket_menu)
    except:
        bot.send_message(message.chat.id, msg_text, reply_markup=asotriment_menu)
        bot.send_message(message.chat.id, 'Выставляя количество вы добавляете товары в корзину', reply_markup=botmenu.open_basket_menu)
#region user
@bot.message_handler(func=lambda message: message.text == "📘 Каталог")
def product_catalog(message):
    bot.send_message(message.chat.id, 'Вы в каталоге товаров, выберите категорию которая вам интерестна: ', reply_markup=botmenu.category_menu)

@bot.message_handler(func=lambda message: message.text == "🏠 В главное меню")
def general_menu(message):
    bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=botmenu.markhomemenu)

@bot.message_handler(func=lambda message: message.text == "📦 Оплата  доставка")
def delivery_pay(message):
    message_text = dbprocessing.select_cat('Доставка')
    bot.send_message(message.chat.id, message_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🎫 Мои данные")
def personal_info(message):
    get_data = dbprocessing.get_user_info(message.chat.id)
    msg_text = '*Имя: *' + str(get_data[0][0]) + '\n*Номер телефона: *' + str(get_data[0][1]) + '\n*Адреса доставки: *' + str(get_data[0][2]) + '\n*Бонусный баланс: *' + str(get_data[0][3])
    bot.send_message(message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.edit_profile_menu)


@bot.message_handler(func=lambda message: message.text == "📞 Изменить номер телефона")
def edit_profile_phone(message):
    bot.send_message(message.chat.id, 'Введи новый номер телефона: ')
    bot.register_next_step_handler(message, new_phone_edit)

def new_phone_edit(message):
    phone_number = message.text
    if phone_number.isdigit():
        dbprocessing.adduserphone(message.chat.id, phone_number)
        bot.send_message(message.chat.id, 'Отлично, номер изменен', reply_markup=botmenu.edit_profile_menu)
    elif phone_number == 'Отмена':
        bot.send_message(message.chat.id, 'Изменения отменены', reply_markup=botmenu.edit_profile_menu)
    else:
        bot.send_message(message.chat.id, 'Вы допустили ошибку при вводе, повторите попытку: ')
        bot.register_next_step_handler(message, add_phone_number)

@bot.message_handler(func=lambda message: message.text == "🚛 Изменить адрес доставки")
def edit_profile_address(message):
    bot.send_message(message.chat.id, 'Введи новый адрес: ')
    bot.register_next_step_handler(message, new_delivery_address)

def new_delivery_address(message):
    address_delivery = str(message.text)
    user_chat_id = str(message.chat.id)
    if address_delivery != 'Отмена':
        dbprocessing.update_user_address(user_chat_id, address_delivery)
        bot.send_message(message.chat.id, 'Адрес доставки изменен', reply_markup=botmenu.edit_profile_menu)
    else:
        bot.send_message(message.chat.id, 'Изменения отменены', reply_markup=botmenu.edit_profile_menu)

@bot.message_handler(func=lambda message: message.text == "👥 Партнёрская программа")
def partner_link(message):
    users_friend = dbprocessing.get_user_ref(message.chat.id)
    balance_friend = dbprocessing.getuserbalance(message.chat.id)
    msg_text = '*Партнёрская программа * 👬 \n\nПриглашено: {0} 👥\nБыло получено: {1} 💵 \n\n📎 Твоя реферальная ссылка: \n\n💰 Мы платим за кождую покупку приглашенного тобой пользователя.'.format(str(users_friend), str(balance_friend))
    shared_deep_link_menu = telebot.types.InlineKeyboardMarkup()
    startlitegame = telebot.types.InlineKeyboardButton(text='📣 Отправить приглашение',
    callback_data='sharedlinkfriends')
    shared_deep_link_menu.add(startlitegame)
    photo = open('product_image/friends.png', 'rb')
    bot.send_message(message.chat.id, msg_text, parse_mode='Markdown', reply_markup=shared_deep_link_menu)
    photo.close()
@bot.message_handler(func=lambda message: message.text == "📃 О нас")
def about(message):
    about_msg = dbprocessing.select_cat('О нас')
    bot.send_message(message.chat.id, about_msg, reply_markup=botmenu.about_menu)

@bot.message_handler(func=lambda message: message.text == "🏷 Акции")
def promo(message):
    promo_msg = dbprocessing.select_cat('Акции')
    bot.send_message(message.chat.id, promo_msg)

@bot.message_handler(func=lambda message: message.text == "🗂 К списку категорий")
def back_to_category(message):
    bot.send_message(message.chat.id, 'Вы в списке категорий', reply_markup=botmenu.category_menu)

@bot.message_handler(func=lambda message: message.text == "🛒 Корзина")
def get_item_basket(message):
    dbprocessing.operation_bonus(message.chat.id)
    basket = str(dbprocessing.getbasketlist(message.chat.id))
    allprice = str(dbprocessing.selectallprice(message.chat.id))
    msg_text = '*Корзина*' + basket + '\n\nВсего - ' + allprice
    bot.send_message(message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.open_basket_menu)


@bot.message_handler(func=lambda message: message.text == "📋 Оформить")
def create_order_onestep(message):
    try:
        dbprocessing.operation_bonus(message.chat.id)
        dbprocessing.operation_bonus(message.chat.id)
        allprice = str(dbprocessing.selectallprice(message.chat.id))    
        if float(allprice) > 1:
            get_bonus_ballance = dbprocessing.getuserbalance(message.chat.id)
            address = str(dbprocessing.get_address_user(message.chat.id))
            phone = str(dbprocessing.get_phone_user(message.chat.id))
            if address == 'Не указан' or phone == 'Не указан':
                bot.send_message(message.chat.id, 'Вы не указали номер телефона или адрес доставки. Без этого оформление не возможно.', reply_markup=botmenu.edit_profile_menu)
                get_data = dbprocessing.get_user_info(message.chat.id)
                msg_text = '*Имя: *' + str(get_data[0][0]) + '\n*Номер телефона: *' + str(get_data[0][1]) + '\n*Адреса доставки: *' + str(get_data[0][2]) + '\n*Бонусный баланс: *' + str(get_data[0][3])
                bot.send_message(message.chat.id, msg_text, parse_mode='Markdown')
            else:
                if get_bonus_ballance > 1:
                    basket = str(dbprocessing.getbasketlist(message.chat.id))
                    msg_text = '*Корзина*\nВы накопили: ' + str(get_bonus_ballance) + ' 💎\n' + basket + '\n\nВсего - ' + allprice
                    get_bonus_ballance = dbprocessing.getuserbalance(message.chat.id)                
                    bot.send_message(message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.orders_menu_onestep)
                else:
                    basket = str(dbprocessing.getbasketlist(message.chat.id))
                    msg_text = '*Корзина* ' + basket + '\n\nВсего - ' + allprice
                    bot.send_message(message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.delivery_menu)
            
        else:
            bot.send_message(message.chat.id, 'Для заказа корзина не должна быть пуста')
    except Exception as e:
        print(e)

@bot.message_handler(func=lambda message: message.text == "Использовать бонусы")
def create_order_bonus_step(message):
    print('step 1')
    dbprocessing.addbasketbonus(message.chat.id)
    print('step 2')
    basket = str(dbprocessing.getbasketlist(message.chat.id))
    print('step 3')
    allprice = str(dbprocessing.selectallprice(message.chat.id))
    print('step 4')
    msg_text = '*Корзина*\n' + basket + '\n\nВсего - ' + allprice
    print('step 5')
    bot.send_message(message.chat.id, msg_text, parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Выберите способ доставки: ', reply_markup=botmenu.delivery_menu)

@bot.message_handler(func=lambda message: message.text == "Оплата без бонусов")
def create_order_notbonus_step(message):
    bot.send_message(message.chat.id, 'Выберите способ доставки: ', reply_markup=botmenu.delivery_menu)


@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_basket_menu(message):
    end_menu = str(dbprocessing.select_endmenu(message.chat.id))
    if end_menu == 'diapers':
        dbprocessing.insert_endmenu(message.chat.id, 'diapers')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Подгузники')
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
    elif end_menu == 'wetwipes':
        dbprocessing.insert_endmenu(message.chat.id, 'wetwipes')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Влажные салфетки')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
    elif end_menu == 'developmenttoys':
        dbprocessing.insert_endmenu(message.chat.id, 'developmenttoys')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Все для развития')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
    elif end_menu == 'breastpumps_category':
        dbprocessing.insert_endmenu(message.chat.id, 'breastpumps_category')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Разное')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)

@bot.message_handler(func=lambda message: message.text == "Разделы")
def cat_bot_edit(message):
    bot.send_message(message.chat.id, 'Вы в меню редактирования текстов розделов. Выберите раздел для редактирования', reply_markup=botmenu.ec_rozdel)

@bot.message_handler(func=lambda message: message.text == "❌ Очистить корзину")
def clear_basket(message):
    dbprocessing.clearbasket(message.chat.id)
    bot.send_message(message.chat.id, 'Корзина пуста', reply_markup=botmenu.basket_menu)

@bot.message_handler(func=lambda message: message.text == "my_chatid")
def send_chatid(message):
    bot.send_message(message.chat.id, str(message.chat.id))
#endregion

#region Order
def edit_conf_ph(message):
    phone_number = message.text
    if phone_number.isdigit():
        dbprocessing.adduserphone(message.chat.id, phone_number)
        bot.send_message(message.chat.id, 'Отлично, номер изменен')
        type_delivery = 'Доставка по адресу'
        user_id = message.chat.id
        product_basket = dbprocessing.getbasketlist(user_id)
        user_info = dbprocessing.get_user_info(user_id)
        update_user_info = 'Имя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
            + '\nАдрес: ' + str(user_info[0][2])
        user_msg_text = 'Новый заказ!\n\nЗаказ: ' + str(product_basket) \
            + '\n\nИнформация о клиенте:\n' + str(update_user_info) \
                 + '\n\nТип доставки: ' + str(type_delivery)
        bot.send_message(user_id, user_msg_text, reply_markup=botmenu.confirm_data)
    elif phone_number == 'Отмена':
        bot.send_message(message.chat.id, 'Изменения отменены', reply_markup=botmenu.not_edit)
    else:
        bot.send_message(message.chat.id, 'Вы допустили ошибку при вводе, повторите попытку: ')
        bot.register_next_step_handler(message, edit_conf_ph)

def edit_conf_adrs(message):
    address_delivery = str(message.text)
    user_chat_id = str(message.chat.id)
    if address_delivery != 'Отмена':
        dbprocessing.update_user_address(user_chat_id, address_delivery)
        bot.send_message(message.chat.id, 'Адрес доставки изменен')
        type_delivery = 'Доставка по адресу'
        user_id = message.chat.id
        product_basket = dbprocessing.getbasketlist(user_id)
        user_info = dbprocessing.get_user_info(user_id)
        update_user_info = 'Имя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
            + '\nАдрес: ' + str(user_info[0][2])
        user_msg_text = 'Новый заказ!\n\nЗаказ: ' + str(product_basket) \
            + '\n\nИнформация о клиенте:\n' + str(update_user_info) \
                 + '\n\nТип доставки: ' + str(type_delivery)
        bot.send_message(user_id, user_msg_text, reply_markup=botmenu.confirm_data)
    else:
        bot.send_message(message.chat.id, 'Изменения отменены')
#endregion

#region product
def add_item(message):
    new_item_list = str(message.text).split(';')
    item_list = []
    for item in new_item_list:
        item_list.append(item.strip())
    try:
        dbprocessing.add_item_db(str(item_list[0]), str(item_list[1]), str(item_list[2]), str(item_list[3]), str(item_list[4]), item_list[5])
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Товар добавлен в базу данных и уже доступен пользователям для заказа.\nЧтобы добавить фото - перейдите к редактирования товаров')

def product_edits(message):
    product_info = dbprocessing.get_product_info_id(message.text)
    config.edit_photo_id = int(message.text)
    msg_text = 'Название: ' + str(product_info[0]) + '\nОписание: ' + str(product_info[1]) + \
        '\nЦена: ' + str(product_info[2]) + '\nКатегория: ' + str(product_info[4]) + '\nИзображение: ' + str(product_info[3]) + \
            '\nid product: ' + str(product_info[5]) + '\nНаличие: ' + str(product_info[6])
    bot.send_message(message.chat.id, msg_text, reply_markup=botmenu.edit_product_menu)

def product_delete(message):
    product_id = message.text
    dbprocessing.delete_product(product_id)
    msg_text = 'Товар удален'
    bot.send_message(message.chat.id, msg_text)

def edit_photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)

    start_name = ''.join(random.choice(chars) for x in range(size))

    img_patch = 'product_image/'
    img_name = str(start_name) + '.png'

    finish_img = img_patch + img_name

    with open(finish_img, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    print(str(config.edit_photo_id), 'product_img', str(img_name))
    dbprocessing.edit_product(str(config.edit_photo_id), 'product_img', str(img_name))
    bot.send_message(message.chat.id, 'Фотография товара успешно зменена')

def edit_product_name(message):
    val = str(message.text)
    dbprocessing.edit_product(str(config.edit_photo_id), 'product_name', str(val))
    bot.send_message(message.chat.id, 'Изминения успешно внесены')

def edit_product_desc(message):
    val = str(message.text)
    dbprocessing.edit_product(str(config.edit_photo_id), 'product_desc', str(val))
    bot.send_message(message.chat.id, 'Изминения успешно внесены')

def edit_product_cat(message):
    val = str(message.text)
    dbprocessing.edit_product(str(config.edit_photo_id), 'product_category', str(val))
    bot.send_message(message.chat.id, 'Изминения успешно внесены')

def edit_product_price(message):
    val = str(message.text)
    dbprocessing.edit_product(str(config.edit_photo_id), 'product_price', str(val))
    bot.send_message(message.chat.id, 'Изминения успешно внесены')

def edit_product_brand(message):
    val = str(message.text)
    dbprocessing.edit_product(str(config.edit_photo_id), 'product_brand', str(val))
    bot.send_message(message.chat.id, 'Изминения успешно внесены')

def edit_product_aviable(message):
    value = message.text
    dbprocessing.add_to_aviable(config.edit_photo_id, str(value))
    bot.send_message(message.chat.id, 'Наличие изменено')

def create_excel():
    data = ['id', 'name', 'desc', 'img', 'price', 'category', 'brand', 'aviable']
    with open('.csv', 'a', newline='', encoding='utf-8') as fl:
        writer = csv.writer(fl)
        writer.writerow(data)

def seve_excel():
    p_id = dbprocessing.get_id_pd()
    name = dbprocessing.get_name_pd()
    desc = dbprocessing.get_desc_pd()
    price = dbprocessing.get_price_pd()
    category = dbprocessing.get_category_pd()
    brand = dbprocessing.get_brand_pd()
    aviable = dbprocessing.get_aviable_pd()

    df = pd.DataFrame({'id': p_id,
        'name': name,
        'desc': desc,
        'price': price,
        'category': category,
        'brand': brand,
        'aviable': aviable,
    })
    writer = pd.ExcelWriter('product.xlsx', engine='xlsxwriter')# pylint: disable=abstract-class-instantiated 
    df.to_excel(writer, sheet_name='Sheet1')    
    writer.save()

def edit_text_about(message):
    try:
        text = message.text
        cat = 'О нас'
        dbprocessing.update_cat(str(cat), str(text))
        bot.send_message(message.chat.id, 'Изменения успешно применены, и доступны пользователям')
    except Exception as e:
        print(e)

def edit_text_sale(message):
    text = message.text
    cat = 'Акции'
    dbprocessing.update_cat(cat, text)
    bot.send_message(message.chat.id, 'Изменения успешно применены, и доступны пользователям')

def edit_text_del(message):
    text = message.text
    cat = 'Доставка'
    dbprocessing.update_cat(cat, text)
    bot.send_message(message.chat.id, 'Изменения успешно применены, и доступны пользователям')
#endregion


#region Sender
def start_sender(text):
    user_list = dbprocessing.select_users()
    get_len_user = len(user_list)
    for i in range(get_len_user):
        try:
            user_id = user_list[i][0]
            bot.send_message(user_id, str(text))
        except:
            dbprocessing.blockedsenderadd(user_id)
    
def add_draf(text):
    status = 'Черновик'
    dbprocessing.add_sender(text, status)

def send_admin(text, menu):
    try:
        admin_list = dbprocessing.select_admin()
        for i in range(len(admin_list)):
            user_id = str(admin_list[i][0])
            try:
                msg_id = dbprocessing.select_end_msgid(user_id)
                if menu == 'yes':
                    bot.edit_message_text(text, chat_id=user_id, message_id=msg_id, reply_markup=botmenu.opetatorinlinemenu)
                    #bot.send_message(user_id, text, reply_markup=botmenu.opetatorinlinemenu)
                else:
                    bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
            except Exception as e:
                print('error send admin code: ', e)
                if menu == 'yes':
                    #bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
                    bot.send_message(user_id, text, reply_markup=botmenu.opetatorinlinemenu)
                else:
                    bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
    except Exception as e:
        print('send admin error code: ', e)

def send_manager(text, menu):
    try:
        admin_list = dbprocessing.select_man()
        for i in range(len(admin_list)):
            user_id = str(admin_list[i][0])
            try:
                msg_id = dbprocessing.select_end_msgid(user_id)
                if menu == 'yes':
                    bot.edit_message_text(text, chat_id=user_id, message_id=msg_id, reply_markup=botmenu.opetatorinlinemenu)
                    #bot.send_message(user_id, text, reply_markup=botmenu.opetatorinlinemenu)
                else:
                    bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
            except Exception as e:
                print('error send admin code: ', e)
                if menu == 'yes':
                    #bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
                    bot.send_message(user_id, text, reply_markup=botmenu.opetatorinlinemenu)
                else:
                    bot.edit_message_text(text, chat_id=user_id, message_id=msg_id)
    except Exception as e:
        print('eroor send_manager: ', e)

def send_courier(text, menu, chatid):
    try:
        if menu == 'yes':
            bot.send_message(chatid, text, reply_markup=botmenu.courier_menu)
        else:
            bot.send_message(chatid, text)
    except:
        print('error courier')

def send_user_status(text, status):
    get_user_id = text.split('user_id: ')
    user_id = get_user_id[1]
    bot.send_message(user_id, str(status))

def get_user_send_id(text):
    get_user_id = text.split('user_id: ')
    user_id_sms = get_user_id[1]
    get_id_text = user_id_sms.split('Имя')
    user_id = get_id_text[0]
    result = user_id.replace('\n', '')
    return result


def get_price(text):
    get_user_id = text.split('Имя:')
    user_id = get_user_id[0]
    return user_id

def add_to_money(userid):
    try:
        user_father = dbprocessing.select_friend_user(userid)
        user_father_id = user_father.strip()
        print(user_father_id)
        dbprocessing.addToMoney(user_father)
        msg_text = 'Приглашенный вами пользователь совершил покупку, на ваш балланс зачислено 30 💎.'
        bot.send_message(user_father_id, msg_text)
    except Exception as e:
        print('error add money')
        print(e)

def comment_user(message):
    try:
        dbprocessing.delete_comment(message.chat.id)
        comment = message.text
        print(comment)    
        dbprocessing.insert_comment(message.chat.id, comment)
        bot.send_message(message.chat.id, 'Теперь выберите время доставки: ', reply_markup=botmenu.time_del_menu)
    except Exception as e:
        print(e)


def courier_del(message):
    date_del = message.text
    type_delivery = 'Доставка по адресу'
    user_id = message.chat.id
    dbprocessing.update_dlv_type(user_id, type_delivery)
    product_basket = dbprocessing.getbasketlist(user_id)
    user_info = dbprocessing.get_user_info(user_id)
    app_price = dbprocessing.selectallprice(user_id)
    id_o = dbprocessing.select_end_oid()
    update_user_info = 'user_id: ' + str(user_id) + '\nИмя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
        + '\nАдрес: ' + str(user_info[0][2])
    user_msg_text = 'Заказ №' + str(id_o) + '\n\nЗаказ: ' + str(product_basket) + '\nВсего цена: ' + str(app_price) \
        + '\n\nИнформация о клиенте:\n' + str(update_user_info) \
                + '\n\nТип доставки: ' + str(type_delivery) + '\nКомментарий: ' + str(date_del)
    send_admin(user_msg_text, 'yes')
    item_name = dbprocessing.get_basket_name(user_id)
    for item in item_name:
        dbprocessing.aviable_minus(item)
    dbprocessing.addorders(user_id, app_price, 'В обработке')
    dbprocessing.clearbasket(user_id)
    send_manager(user_msg_text, 'yes')
    send_user_status(user_msg_text, 'В обработке')
    user_id = get_user_send_id(user_msg_text)
    dbprocessing.update_orders_status(user_id, 'Обработан')
#endregion


#region CallBack
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'diapers':
        dbprocessing.insert_endmenu(call.message.chat.id, 'diapers')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Подгузники')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(call.message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
#        item_list = dbprocessing.print_item('Подгузники')
#        for item in item_list:
#            print(item)
#            if item[3] == 'none':
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_message(call.message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
#            else:
#                img_patch = 'product_image/' + str(item[3])
#                img = open(img_patch, 'rb')
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_photo(call.message.chat.id, img, caption=msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
    elif call.data == 'wetwipes':
        dbprocessing.insert_endmenu(call.message.chat.id, 'wetwipes')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Влажные салфетки')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(call.message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
#        item_list = dbprocessing.print_item('Влажные салфетки')
#        for item in item_list:
#            print(item)
#            if item[3] == 'none':
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_message(call.message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
#            else:
#                img_patch = 'product_image/' + str(item[3])
#                img = open(img_patch, 'rb')
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_photo(call.message.chat.id, img, caption=msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
    elif call.data == 'developmenttoys':
        dbprocessing.insert_endmenu(call.message.chat.id, 'developmenttoys')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Все для развития')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(call.message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
#        item_list = dbprocessing.print_item('Игрушки-развивашки')
#        for item in item_list:
#            print(item)
#            if item[3] == 'none':
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_message(call.message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
#            else:
#                img_patch = 'product_image/' + str(item[3])
#                img = open(img_patch, 'rb')
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_photo(call.message.chat.id, img, caption=msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
    elif call.data == 'breastpumps_category':
        dbprocessing.insert_endmenu(call.message.chat.id, 'breastpumps_category')
        brand_list = []
        podguzniki_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        get_all_brand = dbprocessing.get_all_brand('Разное')
        print(get_all_brand)
        getlen = len(get_all_brand)
        if getlen % 2 != 0:
            newline = 'none'
            get_all_brand.append(newline)
        for i in range(getlen):
            if get_all_brand[i][0] not in brand_list and get_all_brand[i+1][0]:
                brand_one = get_all_brand[i][0]
                brand_two = get_all_brand[i+1][0]
                print(brand_one, brand_two)
                if brand_two == 'n':
                    podguzniki_menu.row(brand_one)
                else:    
                    podguzniki_menu.row(brand_one, brand_two)
                    brand_list.append(brand_one)
                    brand_list.append(brand_two)
                i += 1
            else:
                i += 1
        podguzniki_menu.row("🏠 В главное меню")
        bot.send_message(call.message.chat.id, 'Выберите бренд', reply_markup=podguzniki_menu)
#        item_list = dbprocessing.print_item('Молокоотсосы')
#        for item in item_list:
#            print(item)
#            if item[3] == 'none':
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_message(call.message.chat.id, msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)
#            else:
#                img_patch = 'product_image/' + str(item[3])
#                img = open(img_patch, 'rb')
#                msg_text = '*' + item[1] + '*\n\n' + item[2] + '\n*Цена: *' + str(item[4]) + '\nКод товара: ' + str(item[0])
#                bot.send_photo(call.message.chat.id, img, caption=msg_text, parse_mode='Markdown', reply_markup=botmenu.item_menu)

    elif call.data == 'add_to_basket':
        if call.message.text:
            item_info = call.message.text
            get_product_code = item_info.split('Код товара: ')
            dbprocessing.addbasket(call.message.chat.id, get_product_code[1])
            bot.send_message(call.message.chat.id, 'Товар добавлен в корзину')
        else:
            msg_data = str(call.message).split('caption\': \'')
            list_msg_data = str(msg_data[2].split('\', \''))
            get_product_info = str(list_msg_data).split('Код товара: ')
            get_code = str(get_product_info[1]).split('\', "')
            dbprocessing.addbasket(call.message.chat.id, get_code[0])
            bot.send_message(call.message.chat.id, 'Товар добавлен в корзину')
    elif call.data == 'selfpickup':
        type_delivery = 'Самовывоз'
        user_id = call.message.chat.id
        dbprocessing.update_dlv_type(user_id, type_delivery)
        product_basket = dbprocessing.getbasketlist(user_id)
        user_info = dbprocessing.get_user_info(user_id)
        all_price = dbprocessing.selectallprice(user_id)
        dbprocessing.insert_id_order()
        orders_id = int(dbprocessing.select_end_oid())
        update_user_info = 'Имя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
            + '\nАдрес: ' + str(user_info[0][2])
        msg_text = 'Заказ №' + str(orders_id) + '\n\nЗаказ:\n' + str(product_basket)  + '\nВсего: ' + str(all_price)\
            + '\n\nИнформация о клиенте:\n' + str(update_user_info) + '\nuser_id: ' \
                + str(user_id) + '\n\nТип доставки: ' + str(type_delivery)
        msg_id = call.message.message_id
        bot.edit_message_reply_markup(call.message.chat.id, msg_id, reply_markup=None)
        send_admin(msg_text, 'yes')
        dbprocessing.addorders(user_id, all_price, 'В обработке')
        send_manager(msg_text, 'yes')
        item_name = dbprocessing.get_basket_name(user_id)
        for item in item_name:
            dbprocessing.aviable_minus(item)
        dbprocessing.clearbasket(user_id)
        send_user_status(msg_text, 'Ваш заказ отправлен в обработку')
        user_id = get_user_send_id(msg_text)
        dbprocessing.update_orders_status(user_id, 'Обработан')
    elif call.data == 'courier':
        msg_text = 'Отлично, теперь выбери удобное время доставки: '
        msg_id = call.message.message_id
        bot.send_message(call.message.chat.id, msg_text, reply_markup=botmenu.time_del_menu)
        bot.edit_message_reply_markup(call.message.chat.id, msg_id, reply_markup=None)
    elif call.data == 'speed_del':
        try:
            type_delivery = 'Доставка по адресу'
            user_id = call.message.chat.id
            product_basket = dbprocessing.getbasketlist(user_id)
            user_info = dbprocessing.get_user_info(user_id)
            app_price = dbprocessing.selectallprice(user_id)
            dbprocessing.insert_id_order()
            id_o = dbprocessing.select_end_oid()
            update_user_info = 'user_id: ' + str(user_id) + '\nИмя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
                + '\nАдрес: ' + str(user_info[0][2])
            user_msg_text = 'Заказ №' + str(id_o) + '!\n\nЗаказ: ' + str(product_basket) + '\nВсего цена: ' + str(app_price)\
                + '\n\nИнформация о клиенте:\n' + str(update_user_info) \
                    + '\n\nТип доставки: ' + str(type_delivery) + '\nВремя доставки: Как можно быстрее'
            dbprocessing.addorders(user_id, app_price, 'В обработке')        
            send_admin(user_msg_text, 'yes')
            item_name = dbprocessing.get_basket_name(user_id)
            for item in item_name:
                dbprocessing.aviable_minus(item)
            dbprocessing.clearbasket(user_id)
            send_manager(user_msg_text, 'yes')
            msg_id = call.message.message_id
            bot.edit_message_reply_markup(call.message.chat.id, msg_id, reply_markup=None)
        except Exception as e:
            print('error code: ', e)
    elif call.data == 'set_dt':
        try:
            now_date = datetime.datetime.now().strftime('%H')
            print(now_date)
            if int(now_date) < 11:
                bot.send_message(call.message.chat.id, 'Отлично, теперь укажите удобное время, когда хотели бы получить свой заказ: ', reply_markup=botmenu.am_menu)
            elif int(now_date) > 11 and int(now_date) < 16:
                bot.send_message(call.message.chat.id, 'Отлично, теперь укажите удобное время, когда хотели бы получить свой заказ: ', reply_markup=botmenu.elevent_sixteen)
            else:
                bot.send_message(call.message.chat.id, 'Отлично, теперь укажите удобное время, когда хотели бы получить свой заказ: ', reply_markup=botmenu.pm_menu)
            bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        except Exception as e:
            print(e)
    elif call.data == 'edit_phone_confirm':
        bot.send_message(call.message.chat.id, 'Введите новый номер телефона: ')
        bot.register_next_step_handler(call.message, edit_conf_ph)
    elif call.data == 'edit_address_confirm':
        bot.send_message(call.message.chat.id, 'Введите новый адрес: ')
        bot.register_next_step_handler(call.message, edit_conf_adrs)
    elif call.data == 'oc_data':
        user_id = call.message.chat.id
        type_delivery = dbprocessing.get_dlv_type(user_id)
        dbprocessing.update_dlv_type(user_id, type_delivery)
        product_basket = dbprocessing.getbasketlist(user_id)
        user_info = dbprocessing.get_user_info(user_id)
        all_price = dbprocessing.selectallprice(user_id)
        dbprocessing.insert_id_order()
        id_o = dbprocessing.select_end_oid()
        update_user_info = 'user_id: ' + str(user_id) + '\nИмя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
            + '\nАдрес: ' + str(user_info[0][2])
        msg_text = '*Заказ №*' + str(id_o) + '\n\nЗаказ:\n-----\n' + str(product_basket) + '\nВсего: ' + str(all_price) \
            + '\n\n*Информация о клиенте:*\n----\n' + str(update_user_info) + '\nuser_id: ' \
                + str(user_id) + '\n\n*Тип доставки: *' + str(type_delivery)
        dbprocessing.addorders(user_id, all_price, 'В обработке')      
        item_name = dbprocessing.get_basket_name(user_id)
        for item in item_name:
            dbprocessing.aviable_minus(item)  
        dbprocessing.clearbasket(user_id)
    elif call.data == 'addadmin':
        user_id = call.message.chat.id
        user_status = call.message.text
        dbprocessing.edit_user_status(user_status, 'admin')
        msg_text = 'Статус пользователя ' + str(user_status) + ' изменен на \'Администратор\''
        bot.send_message(user_id, msg_text)
        bot.send_message(user_status, 'Ваш статус изменен на \'Администратор\'')
    elif call.data == 'addcourier':
        user_id = call.message.chat.id
        user_status = call.message.text
        dbprocessing.edit_user_status(user_status, 'courier')
        msg_text = 'Статус пользователя ' + str(user_status) + ' изменен на \'Курьер\''
        bot.send_message(user_id, msg_text)
        bot.send_message(user_status, 'Ваш статус изменен на \'Курьер\'')
    elif call.data == 'addmanager':
        user_id = call.message.chat.id
        user_status = call.message.text
        dbprocessing.edit_user_status(user_status, 'manager')
        msg_text = 'Статус пользователя ' + str(user_status) + ' изменен на \'Менеджер\''
        bot.send_message(user_id, msg_text)
        bot.send_message(user_status, 'Ваш статус изменен на \'Менеджер\'')
    elif call.data == 'addusers':
        user_id = call.message.chat.id
        user_status = call.message.text
        dbprocessing.edit_user_status(user_status, 'user')
        msg_text = 'Статус пользователя ' + str(user_status) + ' изменен на \'Клиент\''
        bot.send_message(user_id, msg_text)
        bot.send_message(user_status, 'Ваш статус изменен на \'Клиент\'')
    elif call.data == 'addnewitem':
        user_id = call.message.chat.id
        msg_text = 'Введите данные товара в таком же порядке через розделитель \';\'\nназвание;описание;цена;категория;бренд;налицие(цыфра)'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, add_item)
    elif call.data == 'edititem':
        user_id = call.message.chat.id
        msg_text = 'Введите id товара. У последнего добавленого товара id - ' + str(dbprocessing.count_item())
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, product_edits)
    elif call.data == 'edit_add_img':
        user_id = call.message.chat.id
        msg_text = 'Пришли мне в ответ фотографию товара'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_photo)
    elif call.data == 'edit_add_nam':
        user_id = call.message.chat.id
        msg_text = 'Пришли новое название'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_product_name)
    elif call.data == 'edit_add_des':
        user_id = call.message.chat.id
        msg_text = 'Пришли новое описание'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_product_desc)
    elif call.data == 'edit_add_cat':
        user_id = call.message.chat.id
        msg_text = 'Пришли новое название категории'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_product_cat)
    elif call.data == 'edit_add_prc':
        user_id = call.message.chat.id
        msg_text = 'Пришли новую цену'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_product_price)
    elif call.data == 'edit_add_brn':
        user_id = call.message.chat.id
        msg_text = 'Пришли новое название бренда'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_product_brand)
    elif call.data == 'edit_add_avi':
        user_id = call.message.chat.id
        msg_text = 'Пришли новое количество'
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, edit_product_aviable)
    elif call.data == 'getexcel':
        seve_excel()
        doc = open('product.xlsx', 'rb')
        bot.send_document(call.message.chat.id, doc)  
        doc.close()      
        os.remove('product.xlsx')

    elif call.data == 'aboutd_ed':
        bot.send_message(call.message.chat.id, 'Введите текст: ')
        bot.register_next_step_handler(call.message, edit_text_about)
    elif call.data == 'sale_ed':
        bot.send_message(call.message.chat.id, 'Введите текст: ')
        bot.register_next_step_handler(call.message, edit_text_sale)
    elif call.data == 'del_ed':
        bot.send_message(call.message.chat.id, 'Введите текст: ')
        bot.register_next_step_handler(call.message, edit_text_del)
    elif call.data == 'send_add_new':
        get_message_text = call.message.text
        start_sender(get_message_text)
    elif call.data == 'send_darf':
        get_message_text = call.message.text
        print(get_message_text)
        add_draf(get_message_text)
        bot.send_message(call.message.chat.id, 'Успешно добавлено')
    elif call.data == 'show_draf':
        list_text_draf = dbprocessing.select_draf()
        for i in range(len(list_text_draf)):
            bot.send_message(call.message.chat.id, list_text_draf[i][1], reply_markup=botmenu.draf_sender_menu)
    elif call.data == 'send_send':
        list_ok_send = dbprocessing.select_send()
        for i in range(len(list_ok_send)):
            msg_text = str(list_ok_send[i][1])
            bot.send_message(call.message.chat.id, msg_text, reply_markup=botmenu.sender_send_menu)
    elif call.data == 'rm_draf':
        get_message_text = call.message.text
        dbprocessing.delete_draf(get_message_text)
        bot.send_message(call.message.chat.id, 'Успешно удалено')
    elif call.data == 'rm_send':
        get_message_text = call.message.text
        dbprocessing.delete_send(get_message_text)
        bot.send_message(call.message.chat.id, 'Успешно удалено')
    elif call.data == 'processed':
        try:
            text_data = call.message.text
            msg_text = 'Заказ принят\n' + str(text_data)
            send_manager(msg_text, 'no')
            courier_list_menu = telebot.types.InlineKeyboardMarkup()
            corier_list_val = dbprocessing.courier_list()
            len_cr = len(corier_list_val) - 1
            for i in range(len_cr):
                cr_id = corier_list_val[i]
                name_cr = corier_list_val[i+1]
                if cr_id.isdigit():
                    courier_button = telebot.types.InlineKeyboardButton(text=name_cr,
                    callback_data=cr_id)
                    courier_list_menu.row(courier_button)
                i += 1
            msg_id = call.message.message_id
            bot.edit_message_reply_markup(call.message.chat.id, msg_id, reply_markup=courier_list_menu)
            tested = dbprocessing.select_end_msgid(call.message.chat.id)
            if tested == 'none':
                dbprocessing.insert_msgid(call.message.chat.id, msg_id)
        except Exception as e:
            print(e)
    elif call.data == 'canceled':
        text_data = call.message.text
        msg_text = 'Заказ отменен!\n' + str(text_data)
        send_admin(msg_text, 'no')
        send_manager(msg_text, 'no')
        send_user_status(text_data, 'Ваш заказ отменён')
        msg_id = call.message.message_id
        bot.edit_message_reply_markup(call.message.chat.id, msg_id, reply_markup=None)
    elif call.data == 'cr_start':
        try:
            text_msg = call.message.text
            send_user_status(text_msg, 'Курьер уже выехал к вам')
            send_admin('Курьер доставляет заказ\n' + str(text_msg), 'no')
            send_manager('Курьер доставляет заказ\n' + str(text_msg), 'no')
            send_courier('Доставляется', 'no', call.message.chat.id)
        except Exception as e:
            print(e)
    elif call.data == 'cr_end_nal':
        try:
            text_msg = call.message.text
            send_user_status(text_msg, 'Ваш заказ успешно доставлен')
            send_admin('Заказ успешно доставлен\n\nТип оплаты: Наличными\n' + str(text_msg), 'no')
            send_manager('Заказ успешно доставлен\n\nТип оплаты: Наличными\n' + str(text_msg), 'no')
            msg_id = call.message.message_id
            user_id = get_user_send_id(text_msg)
            add_to_money(user_id)
            send_courier('Доставлено', 'no', call.message.chat.id)
            dbprocessing.update_orders_status(user_id, 'Доставлено')
            bot.delete_message(call.message.chat.id, msg_id)
        except Exception as e:
            print(e)
    elif call.data == 'cr_end_beznal':
        try:
            text_msg = call.message.text
            send_user_status(text_msg, 'Ваш заказ успешно доставлен')
            send_admin('Заказ успешно доставлен\n\nТип оплаты: Безнал\n' + str(text_msg), 'no')
            send_manager('Заказ успешно доставлен\n\nТип оплаты: Безнал\n' + str(text_msg), 'no')
            msg_id = call.message.message_id
            user_id = get_user_send_id(text_msg)
            add_to_money(user_id)
            send_courier('Доставлено', 'no', call.message.chat.id)
            dbprocessing.update_orders_status(user_id, 'Доставлено')
            bot.delete_message(call.message.chat.id, msg_id)
        except Exception as e:
            print(e)
    elif call.data == 'cr_canceled':
        text_msg = call.message.text
        send_user_status(text_msg, 'Ваш заказ отменен курьером')
        msg_id = call.message.message_id
        bot.delete_message(call.message.chat.id, msg_id)
        send_courier('Заказ отменен', 'no', call.message.chat.id)
        send_admin('Заказ отменен курьером\n' + str(text_msg), 'no')
        send_manager('Заказ отменен курьером\n' + str(text_msg), 'no')
        send_user('Ваш заказ отменен курьером')     
    elif str(call.data)[:4] == 'plus':
        try:
            data_result = str(call.data).replace('plus', '')
            dbprocessing.addbasket(call.message.chat.id, data_result)
            brand = dbprocessing.get_brand_name(data_result)
            new_item_list = dbprocessing.print_item(brand)
            asotriment_menu = telebot.types.InlineKeyboardMarkup()
            for test in new_item_list:
                qbasket = str(dbprocessing.get_count_item(call.message.chat.id, test[0]))
                print(qbasket)
                namebutton = telebot.types.InlineKeyboardButton(text=test[0], callback_data='name')
                plus_callback = 'plus' + str(test[0])
                plusbutton = telebot.types.InlineKeyboardButton(text='➕', callback_data=plus_callback)
                qbutton = telebot.types.InlineKeyboardButton(text=qbasket, callback_data='qantity')
                minus_callback = 'mnus' + str(test[0])
                minusbutton = telebot.types.InlineKeyboardButton(text='➖', callback_data=minus_callback)
                asotriment_menu.row(namebutton, plusbutton, qbutton, minusbutton)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=asotriment_menu)
        except Exception as e:
            print(e)
    elif str(call.data)[:4] == 'mnus':
        data_result = str(call.data).replace('mnus', '')
        dbprocessing.rmbasket(call.message.chat.id, data_result)
        brand = dbprocessing.get_brand_name(data_result)
        new_item_list = dbprocessing.print_item(brand)
        asotriment_menu = telebot.types.InlineKeyboardMarkup()
        for test in new_item_list:
            qbasket = str(dbprocessing.get_count_item(call.message.chat.id, test[0]))
            namebutton = telebot.types.InlineKeyboardButton(text=test[0], callback_data='name')
            plus_callback = 'plus' + str(test[0])
            plusbutton = telebot.types.InlineKeyboardButton(text='➕', callback_data=plus_callback)
            qbutton = telebot.types.InlineKeyboardButton(text=qbasket, callback_data='qantity')
            minus_callback = 'mnus' + str(test[0])
            minusbutton = telebot.types.InlineKeyboardButton(text='➖', callback_data=minus_callback)
            asotriment_menu.row(namebutton, plusbutton, qbutton, minusbutton)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=asotriment_menu)
    elif call.data == 'sharedlinkfriends':
        shared_link = 'http://t.me/nwbazalbot?start=' + str(call.message.chat.id)
        mark_friend = telebot.types.InlineKeyboardMarkup()
        gogogo = telebot.types.InlineKeyboardButton(text='Подписаться', url=shared_link)
        mark_friend.row(gogogo)
        msg_text = 'Привет, присоединяйся к лучшему магазину!'
        photo = open('product_image/friends.png', 'rb')
        bot.send_message(call.message.chat.id, 'Отправь другу приглашение ниже')
        bot.send_photo(call.message.chat.id, photo=photo, caption=msg_text, reply_markup=mark_friend)
        photo.close()        
    elif call.data == 'deleteproduct':
        user_id = call.message.chat.id
        msg_text = 'Введите id товара. У последнего добавленого товара id - ' + str(dbprocessing.count_item())
        bot.send_message(user_id, msg_text)
        bot.register_next_step_handler(call.message, product_delete)
    elif call.data == 'cell_phone':
        phonenum = '+77771567072'
        bot.send_contact(call.message.chat.id, phone_number=phonenum, first_name='BOPEboo')
    elif call.data in dbprocessing.courier_list():
        cr_id = call.data
        msg_text = call.message.text
        msg_id = call.message.message_id
        send_courier(msg_text, 'yes', cr_id)
        bot.edit_message_reply_markup(call.message.chat.id, msg_id, reply_markup=None)
        new_text = 'Отправлено курьеру\n' + str(msg_text)
        bot.edit_message_text(new_text, call.message.chat.id, msg_id)
        #bot.edit_message_text(call.message.chat.id, new_text, msg_id, reply_markup=None)
        #bot.send_message(call.message.chat.id, 'Отправлено курьеру')
    elif call.data in config.all_time_list:
        print('start')
        print(call.data)
        time_temp = call.data
        msd_id = call.message.message_id
        bot.edit_message_reply_markup(call.message.chat.id, message_id=msd_id, reply_markup=None)
        print('start if')
        if time_temp == 'am-first':
            date_del = str(config.am_elevent[0])
        elif time_temp == 'am-second':
            date_del = str(config.am_elevent[1])
        elif time_temp == 'pm-first':
            date_del = str(config.pm_elevent[0])
        elif time_temp == 'pm-second':
            date_del = str(config.pm_elevent[1])
        elif time_temp == 'pm-thrid':
            date_del = str(config.pm_elevent[2])
        print('end if')
        type_delivery = 'Доставка по адресу'
        user_id = call.message.chat.id
        dbprocessing.update_dlv_type(user_id, type_delivery)
        product_basket = dbprocessing.getbasketlist(user_id)
        user_info = dbprocessing.get_user_info(user_id)
        app_price = dbprocessing.selectallprice(user_id)
        print('message generate')
        id_o = dbprocessing.select_end_oid()
        update_user_info = 'user_id: ' + str(user_id) + '\nИмя: ' + str(user_info[0][0]) + '\nНомер телефона: ' + str(user_info[0][1]) \
            + '\nАдрес: ' + str(user_info[0][2])
        user_msg_text = 'Заказ №' + str(id_o) + '\n\nЗаказ: ' + str(product_basket) + '\nВсего цена: ' + str(app_price) \
            + '\n\nИнформация о клиенте:\n' + str(update_user_info) \
                    + '\n\nТип доставки: ' + str(type_delivery) + '\nВремя доставки: ' + str(date_del) + \
                        '\n\nКомментарий: ' + str(dbprocessing.select_comment(call.message.chat.id))
        send_admin(user_msg_text, 'yes')
        item_name = dbprocessing.get_basket_name(user_id)
        for item in item_name:
            dbprocessing.aviable_minus(item)
        dbprocessing.addorders(user_id, app_price, 'В обработке')
        dbprocessing.clearbasket(user_id)
        send_manager(user_msg_text, 'yes')
        send_user_status(user_msg_text, 'В обработке')
        user_id = get_user_send_id(user_msg_text)
        dbprocessing.update_orders_status(user_id, 'Обработан')
    elif call.data == 'comment':
        bot.send_message(call.message.chat.id, 'Введите коментарий: ')
        try:
            bot.register_next_step_handler(call.message, comment_user)
        except Exception as e:
            print('error code next step', e)
#endregion


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=123)