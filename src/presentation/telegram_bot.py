from email import message_from_string
from types import NoneType

import telebot
from button_texts import *
from message_texts import *
from test_data import *
from telebot import types
import re

bot = telebot.TeleBot('7370956091:AAHbL15SauJFpQFz_YrpYNWDlCgQf6ckkGM')

event_name = 'AI Product Hack'

back_button = types.KeyboardButton(back_text)
cancel_button = types.KeyboardButton(cancel_text)
go_to_main_page_button = types.KeyboardButton(go_to_main_page_text)
repeat_button = types.KeyboardButton(try_again_text)

yes_button = types.KeyboardButton(yes_text)
no_button = types.KeyboardButton(no_text)

join_event_button = types.KeyboardButton(join_event_text)

create_event_button = types.KeyboardButton(create_event_text)
open_event_list_button = types.KeyboardButton(open_event_list_text)
open_profile_list_button = types.KeyboardButton(open_profile_list_text)
go_to_save_profiles_button = types.KeyboardButton(go_to_save_profiles_text)

add_data_button = types.KeyboardButton(add_data_text)
delete_data_button = types.KeyboardButton(delete_data_text)
start_dialog_button = types.KeyboardButton(start_dialog_text)

like_button = types.KeyboardButton(like_text)
dislike_button = types.KeyboardButton(dislike_text)

saved_users_list_button = types.KeyboardButton(saved_users_list_text)

cancel_markup = types.ReplyKeyboardMarkup()
cancel_markup.add(cancel_button)

people_list_markup = types.ReplyKeyboardMarkup()
people_list_markup.add(back_button)
people_list_markup.add(go_to_main_page_button)

def open_main_page(message):
    markup_main = types.ReplyKeyboardMarkup()
    markup_main.row(join_event_button, create_event_button)
    markup_main.row(open_event_list_button, open_profile_list_button)
    markup_main.add(go_to_save_profiles_button)
    bot.send_message(message.chat.id, open_main_page_message_text, reply_markup=markup_main)
    bot.register_next_step_handler(message, main_page_handler)

@bot.message_handler(commands=['start'])
def start(message):
    # TODO: Запрос на "бэк" на регистрацию пользователя
    markup_start = types.ReplyKeyboardMarkup()
    markup_start.row(join_event_button, create_event_button)
    markup_start.row(open_event_list_button, open_profile_list_button)
    bot.send_message(message.chat.id, welcome_message_text, reply_markup=markup_start)
    bot.register_next_step_handler(message, main_page_handler)

@bot.message_handler(commands=['main'])
def main_page_handler(message):
    if message.text == join_event_text:
        bot.send_message(message.chat.id, request_event_key_message_text, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, join_event_handler)
    elif message.text == create_event_text:
        bot.send_message(message.chat.id, enter_event_name_message_text, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, create_event_handler)
    elif message.text == go_to_save_profiles_text:
        bot.send_message(message.chat.id, saved_profiles_doesnt_exist, reply_markup=types.ReplyKeyboardRemove())
        open_main_page(message)
    elif message.text == open_profile_list_text:
        bot.send_message(message.chat.id, user_profiles_doesnt_exist, reply_markup=types.ReplyKeyboardRemove())
        open_main_page(message)
    else:
        bot.send_message(message.chat.id, handler_not_found_message_text, reply_markup=types.ReplyKeyboardRemove())
        open_main_page(message)
    # if message.text == '':
    #     bot.send_message(message.chat.id, '')

def open_confirm_page(message, yes_handler, no_handler):
    confirm_markup = types.ReplyKeyboardMarkup()
    confirm_markup.row(go_to_main_page_button, repeat_button)
    bot.send_message(message.chat.id, request_confirmation_messaget_text,
                     reply_markup=confirm_markup)
    bot.register_next_step_handler(message, confirm_handler)

def confirm_handler(message, yes_handler, no_handler):
    if message.text == yes_text:
        yes_handler(message)
    elif message.text == no_text:
        no_handler(message)
    else:
        no_handler(message)

def create_event_handler(message):
    global event_name
    event_name = message.text
    # TODO: Вызов AddEvent(id, навзание, описание)
    bot.send_message(message.chat.id, event_was_created_message_text(event_name))
    open_event_page(message)

def join_event_handler(message):
    # TODO: Запрос на подключение к событию (id, название).
    # Если success, то
    if message.text == some_key or message.text == "1":
        open_event_page(message)
    # иначе
    elif message.text == go_to_main_page_text:
        open_main_page(message)
    elif message.text == try_again_text:
        bot.register_next_step_handler(message, join_event_handler)
    else:
        markup_join_event = types.ReplyKeyboardMarkup()
        markup_join_event.row(go_to_main_page_button, repeat_button)
        bot.send_message(message.chat.id, event_not_found_message_text,
                         reply_markup=markup_join_event)
        bot.register_next_step_handler(message, join_event_handler)

def open_admin_panel_page(message):
    admin_markup = types.ReplyKeyboardMarkup()
    list_of_participants_button = types.KeyboardButton(list_of_participants_text)
    admin_markup.add(list_of_participants_button)
    bot.send_message(message.chat.id, admin_panel_message_text,
                     reply_markup=admin_markup)
    bot.register_next_step_handler(message, handle_admin_panel)

def handle_admin_panel(message):
    #TODO: запрос GetUsersByEvent(event_title)
    string_text = list_participants_of_event_message_text(event_name)
    for candidate in candidates_list:
        string_text += create_user_with_match_message(candidate)
    bot.send_message(message.chat.id, string_text,
                     reply_markup=people_list_markup)
    bot.register_next_step_handler(message, handle_people_list)

def open_event_page(message):
    has_profile_in_event = True
    is_admin = True
    # TODO: запрос GetIsAdmin(telegram_id, event_title)
    event_page_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if has_profile_in_event:
        delete_profile_from_event_button = types.KeyboardButton(delete_profile_from_event_text)
        find_match_button = types.KeyboardButton(find_match_text)
        event_page_markup.row(add_data_button, find_match_button)
        event_page_markup.row(delete_data_button, delete_profile_from_event_button)
    else:
        event_page_markup.add(add_data_button)
    if is_admin:
        go_to_admin_page_button = types.KeyboardButton(go_to_admin_page_text)
        event_page_markup.add(go_to_admin_page_button)
    event_page_markup.add(go_to_main_page_button)
    if has_profile_in_event:
        bot.send_message(message.chat.id, event_page_with_empty_profile_message_text(event_name),
                     reply_markup=event_page_markup)
    else:
        bot.send_message(message.chat.id, event_page_with_empty_profile_message_text(event_name),
                     reply_markup=event_page_markup)
    bot.register_next_step_handler(message, handle_event_page)

def handle_event_page(message):
    if message.text == add_data_text:
        select_data_for_upload(message)
    elif message.text == find_match_text:
        open_match_list(message)
    elif message.text == delete_data_text:
        bot.send_message(message.chat.id, function_is_not_available)
        open_event_page(message)
    elif message.text == delete_profile_from_event_text:
        bot.send_message(message.chat.id, function_is_not_available)
        open_event_page(message)
    elif message.text == go_to_main_page_text:
        open_main_page(message)
    elif message.text == go_to_admin_page_text:
        open_admin_panel_page(message)
    else:
        bot.send_message(message.chat.id, handler_not_found_message_text)
        open_event_page(message)

def create_user_with_match_message(user):
    result = (f'@{user["telegram_id"]} \n'
              f' Контакт может быть вам интересен, потому что было обнаружено пересечение: \n')
    for tag in user['tags']:
        result += f'🤝 ' + tag + ' \n'
    return result

def open_match_list(message):
    string_text = list_candidates_from_event_message_text(event_name)
    # TODO: запрос списка  get_user_ranking_response()
    for candidate in candidates_list:
        string_text += create_user_with_match_message(candidate)
    bot.send_message(message.chat.id, string_text,
                     reply_markup=people_list_markup)
    bot.register_next_step_handler(message, handle_people_list)

def handle_people_list(message):
    if message.text == back_text:
        open_event_page(message)
    elif message.text == go_to_main_page_text:
        open_main_page(message)
    else:
        bot.send_message(message.chat.id, handler_not_found_message_text)
        bot.register_next_step_handler(message, handle_people_list)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Получаем информацию о файле
    file_info = bot.get_file(message.document.file_id)
    file_name = message.document.file_name
    file_type = message.document.mime_type

    # Проверяем тип файла по MIME-типу
    # TODO: вызовы методов добавления тегов
    if file_type.startswith('image/'):
        bot.reply_to(message, f"Загружен файл изображения: {file_name}")
    elif file_type.startswith('application/pdf'):
        bot.reply_to(message, f"Загружен PDF-файл: {file_name}")
    elif file_type.startswith('application/msword') or file_type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        bot.reply_to(message, f"Загружен Word-документ: {file_name}")
    else:
        bot.reply_to(message, f"Файл типа {file_type} не поддерживается.")
    open_event_page(message)

@bot.message_handler(commands=['upload'])
def select_data_for_upload(message):
    upload_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    upload_dialog_button = types.KeyboardButton(upload_dialog_text)
    upload_cv_button = types.KeyboardButton(upload_cv_text)
    add_link_to_profile = types.KeyboardButton(add_link_to_profile_text)
    add_person_description = types.KeyboardButton(add_person_description_text)
    upload_markup.add(upload_dialog_button, upload_cv_button)
    upload_markup.add(add_link_to_profile, add_person_description)
    upload_markup.add(back_button)
    bot.send_message(message.chat.id, select_data_type_message_text, reply_markup=upload_markup)
    bot.register_next_step_handler(message, handle_upload)

def handle_upload(message):
    if message.document != None:
        handle_document(message)
    elif message.text == upload_dialog_text:
        bot.send_message(message.chat.id, select_file_message_text)
        bot.register_next_step_handler(message, handle_upload)
    elif message.text == upload_cv_text:
        bot.send_message(message.chat.id, select_file_message_text)
        bot.register_next_step_handler(message, handle_upload)
    elif message.text == add_link_to_profile_text:
        bot.send_message(message.chat.id, request_link_message_text)
        bot.register_next_step_handler(message, handle_add_link_to_profile)
    elif message.text == add_person_description_text:
        bot.send_message(message.chat.id, request_description_message_text, reply_markup=cancel_markup)
        bot.register_next_step_handler(message, handle_add_description)
    elif message.text == back_text:
        open_event_page(message)
    else:
        bot.send_message(message.chat.id, uncorrect_command_message_text)
        open_event_page(message)

def handle_add_description(message):
    if message.text != cancel_text:
        bot.send_message(message.chat.id, description_was_saved)
    open_event_page(message)

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// или https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # домен
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP-адрес
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6-адрес
        r'(?::\d+)?'  # порт
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None
    # # TODO: исправить
    # pattern = r'/https?:\/\/\S+\.\S+/g'
    # match = re.fullmatch(pattern, url)
    # return True if match else False

def handle_add_link_to_profile(message):
    if is_valid_url(message.text):
        bot.send_message(message.chat.id, link_was_added)
    else:
        bot.send_message(message.chat.id, uncorrect_link_message_text)
    open_event_page(message)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

bot.polling(none_stop=True)





