from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def menu_user_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("О нас", callback_data="about"),
        InlineKeyboardButton("Каталог", url="https://www.medsmart.pro/"),
        InlineKeyboardButton("Обучение", callback_data="education"),
        )
    markup.row_width = 1
    markup.add(    
        InlineKeyboardButton("Сервис оборудования", callback_data="service_oborudovanie"),
        InlineKeyboardButton("Сервис наконечников", callback_data="service_nakone4nik"),
    )
    markup.row_width = 2
    markup.add(  
        InlineKeyboardButton("Отзывы", callback_data="otziv"),
        InlineKeyboardButton("FAQ", callback_data="faq"),
        InlineKeyboardButton("Контакты", callback_data="contacts"),
        InlineKeyboardButton("Помощь", url ="https://t.me/Andrew_Vasyukov"),
      

    )

    return markup


def admin_menu_start():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("отчет", callback_data="report"),        
        InlineKeyboardButton("рассылка по всем", callback_data="push_all"),        
    )

    return markup


def back():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("Назад", callback_data="back"),
    )
    return markup