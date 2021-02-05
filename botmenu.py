from telebot import types
import config

textstatusnew = 'Нове замовлення*'

balance = 0
statusorder = 0

markadminmenu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markadminmenu.row("Отчет по пользователям")
markadminmenu.row("Отчет по заказам")
markadminmenu.row("Другие операции")
markadminmenu.row("🏠 В главное меню")

other_admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
other_admin_menu.row('Товары', 'Рассылка')
other_admin_menu.row('Изменить роль пользователя')
other_admin_menu.row('СМС Пользователю', 'Разделы')
other_admin_menu.row('Админ меню')

product_operations = types.InlineKeyboardMarkup()
add_product = types.InlineKeyboardButton(text='Добавить товар', 
callback_data='addnewitem')
edit_product = types.InlineKeyboardButton(text='Редактировать товар', 
callback_data='edititem')
delete_product = types.InlineKeyboardButton(text='Удалить товар', 
callback_data='deleteproduct')
get_excel = types.InlineKeyboardButton(text='Документ с товарами', 
callback_data='getexcel')
product_operations.row(add_product)
product_operations.row(edit_product)
product_operations.row(delete_product)
product_operations.row(get_excel)


ec_rozdel = types.InlineKeyboardMarkup()
about_ed = types.InlineKeyboardButton(text='О нас', 
callback_data='aboutd_ed')
sale_ed = types.InlineKeyboardButton(text='Акции', 
callback_data='sale_ed')
del_ed = types.InlineKeyboardButton(text='Доставка и оплата', 
callback_data='del_ed')
ec_rozdel.row(about_ed)
ec_rozdel.row(sale_ed)
ec_rozdel.row(del_ed)

#ed_prod_menu = types.InlineKeyboardMarkup()


edit_user_status = types.InlineKeyboardMarkup()
addadmin = types.InlineKeyboardButton(text='Администратор', 
callback_data='addadmin')
addcourier = types.InlineKeyboardButton(text='Курьер', 
callback_data='addcourier')
addmanager = types.InlineKeyboardButton(text='Менеджер', 
callback_data='addmanager')
adduser = types.InlineKeyboardButton(text='Пользователь', 
callback_data='addusers')
edit_user_status.row(addadmin)
edit_user_status.row(addcourier)
edit_user_status.row(addmanager)
edit_user_status.row(adduser)

marksendmess = types.ReplyKeyboardMarkup(resize_keyboard=True)
marksendmess.row("gotoap")
marksendmess.row("🏠 В главное меню")

basket_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
basket_menu.row('📋 Оформить', '🛒 Корзина')
basket_menu.row('🗂 К списку категорий')
basket_menu.row('🏠 В главное меню')

open_basket_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
open_basket_menu.row('📋 Оформить', "🛒 Корзина")
open_basket_menu.row('❌ Очистить корзину', '🔙 Назад')

markhomemenu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markhomemenu.row("📘 Каталог", "🏷 Акции")
markhomemenu.row("📦 Оплата  доставка")
markhomemenu.row("🎫 Мои данные", "📃 О нас")
markhomemenu.row("👥 Партнёрская программа")

delivery_menu = types.InlineKeyboardMarkup()
selfpickup = types.InlineKeyboardButton(text='Самовывоз', 
callback_data='selfpickup')
courier = types.InlineKeyboardButton(text='Курьер', 
callback_data='courier')
delivery_menu.row(selfpickup, courier)

orders_menu_onestep = types.ReplyKeyboardMarkup(resize_keyboard=True)
orders_menu_onestep.row('Использовать бонусы')
orders_menu_onestep.row('Оплата без бонусов')
orders_menu_onestep.row('🔙 Назад')

confirm_data = types.InlineKeyboardMarkup()
oc_data = types.InlineKeyboardButton(text='Подтвердить заказ', 
callback_data='oc_data')
edit_phone_confirm = types.InlineKeyboardButton(text='Изменить номер телефона', 
callback_data='edit_phone_confirm')
edit_address_confirm = types.InlineKeyboardButton(text='Изменить адрес', 
callback_data='edit_address_confirm')
confirm_data.row(oc_data)
confirm_data.row(edit_phone_confirm)
confirm_data.row(edit_address_confirm)


time_del_menu = types.InlineKeyboardMarkup()
speed_del = types.InlineKeyboardButton(text='Как можно быстрее', 
callback_data='speed_del')
set_dt = types.InlineKeyboardButton(text='Указать время', 
callback_data='set_dt')
#time_del_menu.row(speed_del)
time_del_menu.row(set_dt)

comment_button = types.InlineKeyboardButton(text='Добавить комментарий',
callback_data='comment')

am_menu = types.InlineKeyboardMarkup()
first_am = types.InlineKeyboardButton(text=config.am_elevent[0], 
callback_data='am-first')
second_am = types.InlineKeyboardButton(text=config.am_elevent[1], 
callback_data='am-second')
am_menu.row(first_am, second_am)
am_menu.row(comment_button)


pm_menu = types.InlineKeyboardMarkup()
pm_first = types.InlineKeyboardButton(text=config.pm_elevent[0], 
callback_data='pm-first')
pm_second = types.InlineKeyboardButton(text=config.pm_elevent[1], 
callback_data='pm-second')
pm_third = types.InlineKeyboardButton(text=config.pm_elevent[2], 
callback_data='pm-thrid')
pm_menu.row(pm_second, pm_third)
pm_menu.row(comment_button)

marknext = types.ReplyKeyboardMarkup(resize_keyboard=True)
marknext.row('Пропустить')

not_edit = types.ReplyKeyboardMarkup(resize_keyboard=True)
not_edit.row('Отмена')

edit_profile_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
edit_profile_menu.row("📞 Изменить номер телефона")
edit_profile_menu.row("🚛 Изменить адрес доставки")
edit_profile_menu.row("🏠 В главное меню", "🛒 Корзина")

category_menu = types.InlineKeyboardMarkup()
diapers_category = types.InlineKeyboardButton(text='Подгузники', 
callback_data='diapers')
wetwipes_category = types.InlineKeyboardButton(text='Влажные салфетки', 
callback_data='wetwipes')
developmenttoys_category = types.InlineKeyboardButton(text='Все для развития', 
callback_data='developmenttoys')
breastpumps_category = types.InlineKeyboardButton(text='Разное', 
callback_data='breastpumps_category')
category_menu.row(wetwipes_category, diapers_category)
category_menu.row(developmenttoys_category, breastpumps_category)


sender_admin_menu = types.InlineKeyboardMarkup()
add_new_sender = types.InlineKeyboardButton(text='Начать рассылку', 
callback_data='send_add_new')
draft = types.InlineKeyboardButton(text='Добавить в черновик', 
callback_data='send_darf')
sdraf = types.InlineKeyboardButton(text='Смотреть черновик', 
callback_data='show_draf')
sent = types.InlineKeyboardButton(text='Отправленные', 
callback_data='send_send')
sender_admin_menu.row(add_new_sender)
sender_admin_menu.row(draft)
sender_admin_menu.row(sdraf)
sender_admin_menu.row(sent)


item_menu = types.InlineKeyboardMarkup()
add_to_basket = types.InlineKeyboardButton(text='Добавить в корзину', 
callback_data='add_to_basket')
item_menu.row(add_to_basket)

edit_product_menu = types.InlineKeyboardMarkup()
edit_add_img = types.InlineKeyboardButton(text='Изменить/добавить картинку', 
callback_data='edit_add_img')
edit_add_nam = types.InlineKeyboardButton(text='Изменить название', 
callback_data='edit_add_nam')
edit_add_des = types.InlineKeyboardButton(text='Изменить описание', 
callback_data='edit_add_des')
edit_add_cat = types.InlineKeyboardButton(text='Изменить категорию', 
callback_data='edit_add_cat')
edit_add_prc = types.InlineKeyboardButton(text='Изменить цену', 
callback_data='edit_add_prc')
edit_add_brn = types.InlineKeyboardButton(text='Изменить бренд', 
callback_data='edit_add_brn')
edit_add_avi = types.InlineKeyboardButton(text='Изменить наличие', 
callback_data='edit_add_avi')
edit_product_menu.row(edit_add_img)
edit_product_menu.row(edit_add_nam)
edit_product_menu.row(edit_add_des)
edit_product_menu.row(edit_add_cat)
edit_product_menu.row(edit_add_prc)
edit_product_menu.row(edit_add_brn)
edit_product_menu.row(edit_add_avi)

draf_sender_menu = types.InlineKeyboardMarkup()
draf_remove = types.InlineKeyboardButton(text='Удалить из черновика', 
callback_data='rm_draf')
draf_sender_menu.row(add_new_sender)
draf_sender_menu.row(draf_remove)

sender_send_menu = types.InlineKeyboardMarkup()
send_remove = types.InlineKeyboardButton(text='Удалить из списка', 
callback_data='rm_send')
sender_send_menu.row(add_new_sender)
sender_send_menu.row(draf_remove)

buy_history_menu = types.InlineKeyboardMarkup()
send_history = types.InlineKeyboardButton(text='История покупок', 
callback_data='send_history')
buy_history_menu.row(send_history)

markorder = types.ReplyKeyboardMarkup(resize_keyboard=True)
markorder.row("📝 Оформить", "❌ Очистить корзину")
markorder.row("📘 Продолжить покупки", "🛒 Корзина")
markorder.row("🏠 В главное меню")

#Операції із замовленням
opetatorinlinemenu = types.InlineKeyboardMarkup()
processed = types.InlineKeyboardButton(text='Принять заказ', 
callback_data='processed')
canceled = types.InlineKeyboardButton(text='Отклонить заказ', 
callback_data='canceled')
opetatorinlinemenu.row(processed, canceled)


courier_menu = types.InlineKeyboardMarkup()
cr_start = types.InlineKeyboardButton(text='Отправляюсь доставлять', 
callback_data='cr_start')
cr_end_nal = types.InlineKeyboardButton(text='Наличными', 
callback_data='cr_end_nal')
cr_end_beznal = types.InlineKeyboardButton(text='Безнал', 
callback_data='cr_end_beznal')
cr_canceled = types.InlineKeyboardButton(text='Отклонить заказ', 
callback_data='cr_canceled')
courier_menu.row(cr_start)
courier_menu.row(cr_end_nal, cr_end_beznal)
courier_menu.row(cr_canceled)

about_menu = types.InlineKeyboardMarkup()
manage_chat = types.InlineKeyboardButton(text='Чат с менеджером', 
url='https://t.me/bopeboo')
instagram_button = types.InlineKeyboardButton(text='Наш инстаграм',
url='https://www.instagram.com/bopeboo/')
whatsapp_button = types.InlineKeyboardButton(text='Whats App', 
url='https://api.whatsapp.com/send?phone=+77771567072')
call_button = types.InlineKeyboardButton(text='Позвонить',
callback_data='cell_phone')
about_menu.row(manage_chat, whatsapp_button)
about_menu.row(instagram_button, call_button)

elevent_sixteen = types.InlineKeyboardMarkup()
elevent_sixteen.row(pm_first)
elevent_sixteen.row(pm_second)