# -*- coding: utf-8 -*-
import telebot
from telebot import types, logger
import sys
import logging
import msg
import os
import keybords
from config import TOKEN, ADMIN
from sqliteormmagic import SQLiteDB
import datetime
import pytz
import pandas as pd
import time
import sqliteormmagic as som


def get_msk_time() -> datetime:
    time_now = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
    time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return time_now

def push_msg(message):

        if message.from_user.id == ADMIN:
            connection = som.create_connection('users.db')
            query = f"""
            SELECT from_user_id FROM users 
            """
            
            all_records_users = pd.read_sql_query(query, connection)
            print(all_records_users)
            connection.close()
            list_of_users = []
            for i in all_records_users['from_user_id']:
                list_of_users.append(i)
            print(list_of_users)
            for user_id in list_of_users:
                try:
                    bot.send_message(chat_id=user_id, text=message.text)
                    time.sleep(0.1)
                except Exception as ex:
                    
                    bot.send_message(chat_id=ADMIN, text=f"{user_id} failed")
                    time.sleep(0.1)  
            bot.send_message(chat_id=message.from_user.id, text=f'Отправлено {len(list_of_users)} сообщений', reply_markup=keybords.admin_menu_start())
db_users = SQLiteDB('users.db')
bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True, disable_web_page_preview=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
    ],)


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):

        db_users.create_table('users', [
        ("from_user_id", 'INTEGER UNIQUE'), 
        ("from_user_username", 'TEXT'), 
        ("reg_time", 'TEXT'), 
        ("about_time", 'TEXT'),   
        ("education_time", 'TEXT'),          
        ("service_oborudovanie_time", 'TEXT'),        
        ("service_nakone4nik_time", 'TEXT'),                  
        ("otziv_time", 'TEXT'), 
        ("faq_time", 'TEXT'), 
        ("contacts_time", 'TEXT'), 
         ])
        
        db_users.ins_unique_row('users', [
            ("from_user_id", message.from_user.id), 
            ("from_user_username", message.from_user.username), 
            ("reg_time", get_msk_time()),                 
            ("about_time", '0'),   
            ("education_time", '0'),          
            ("service_oborudovanie_time", '0'),        
            ("service_nakone4nik_time", '0'),                  
            ("otziv_time", '0'), 
            ("faq_time", '0'), 
            ("contacts_time", '0'), 
       
            ])
        with open('promo_start.mp4', 'rb') as promo_start:
            bot.send_video(chat_id=message.from_user.id, video=promo_start, caption=msg.start_msg.format(username=message.from_user.first_name),reply_markup=keybords.menu_user_main())


    @bot.message_handler(commands=['admin'])
    def get_admin(message):

        if message.from_user.id == ADMIN:
            print(f"message {message.text}")
            bot.send_message(chat_id=message.from_user.id, text=f'Приветствую тебя хозяин-{message.from_user.first_name}!',reply_markup=keybords.admin_menu_start())

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'about':
            print('about', call.data)
            
            with open('about.jpg', 'rb') as foto:
                bot.send_photo(chat_id=call.from_user.id, photo=foto, caption=msg.about_msg, reply_markup=keybords.back())
            db_users.upd_element_in_column(table_name='users', upd_par_name='about_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)

        elif call.data == 'education':
            print('education', call.data)
            with open('education.jpg', 'rb') as foto:
                bot.send_photo(chat_id=call.from_user.id, photo=foto,caption=msg.education_msg, reply_markup=keybords.back()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='education_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)                

        elif call.data == 'service_oborudovanie':
            print('service_oborudovanie', call.data)            
            bot.send_message(chat_id=call.from_user.id, text=msg.service_oborudovanie_msg, reply_markup=keybords.back()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='service_oborudovanie_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)                

        elif call.data == 'service_nakone4nik':
            print('service_nakone4nik', call.data)
            # bot.send_message(chat_id=call.from_user.id, text=msg.service_nakone4nik_msg, reply_markup=keybords.back()) 
            with open(file='nakone4.jpg', mode='rb') as nakone4:
                bot.send_photo(chat_id=call.from_user.id, photo=nakone4, caption=msg.service_nakone4nik_msg, reply_markup=keybords.back())
            db_users.upd_element_in_column(table_name='users', upd_par_name='service_nakone4nik_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)                

        elif call.data == 'otziv':
            print('otziv', call.data)
            bot.send_message(chat_id=call.from_user.id, text=msg.otziv_msg, reply_markup=keybords.back()) 
            db_users.upd_element_in_column(table_name='users', upd_par_name='otziv_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)                

        elif call.data == 'faq':
            print('faq', call.data)
            bot.send_message(chat_id=call.from_user.id, text=msg.faq_msg, reply_markup=keybords.back())   
            db_users.upd_element_in_column(table_name='users', upd_par_name='faq_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)                         

        elif call.data == 'contacts':
            print('contacts', call.data)
            with open('map.png', 'rb') as foto:
                bot.send_photo(chat_id=call.from_user.id, photo=foto, caption=msg.contacts_msg, reply_markup=keybords.back())
            db_users.upd_element_in_column(table_name='users', upd_par_name='contacts_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)                         

        elif call.data == 'back':
            with open('promo_start.mp4', 'rb') as promo_start:
                bot.send_video(chat_id=call.from_user.id, video=promo_start, caption=msg.start_msg.format(username=call.from_user.first_name),reply_markup=keybords.menu_user_main())
        
        #админская часть
        elif call.data == 'push_all':
            print('contacts', call.data)
            m = bot.send_message(chat_id=call.from_user.id, text='Введите текст сообщения для рассылки')
            bot.register_next_step_handler(m, push_msg)

        elif call.data == 'report':
            print('contacts', call.data)
            connection = som.create_connection('users.db')

            query = f"""SELECT * 
                FROM users
                """ 
            print(query)
            all_users = pd.read_sql_query(query, connection)
            all_users.to_excel('report.xlsx',index=False)
            connection.close()
            with open(file='report.xlsx', mode='rb') as ot4et:
                bot.send_document(chat_id=call.from_user.id, document=ot4et, caption='Отчет по пользователям в прикрепленном файле', reply_markup=keybords.admin_menu_start())
            connection.close()

    bot.infinity_polling()

if __name__ == "__main__":
    main()

    