import json
import os
import re

import telebot
from pdfminer.high_level import extract_text
from telebot import types

from src.presentation.button_texts import *
from src.presentation.message_texts import *
from src.service.service_assembler import ServiceAssembler

telegram_key = os.getenv("TELEGRAM_KEY", "")

bot = telebot.TeleBot(telegram_key)
service = ServiceAssembler()

event_name = "AI Product Hack"

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


@bot.message_handler(commands=["start"])
def start(message):
    service.get_add_user_response({"telegram_id": message.from_user.username})
    markup_start = types.ReplyKeyboardMarkup()
    markup_start.row(join_event_button, create_event_button)
    markup_start.row(open_event_list_button, open_profile_list_button)
    bot.send_message(message.chat.id, welcome_message_text, reply_markup=markup_start)
    bot.register_next_step_handler(message, main_page_handler)


@bot.message_handler(commands=["main"])
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


def open_confirm_page(message, yes_handler, no_handler):
    confirm_markup = types.ReplyKeyboardMarkup()
    confirm_markup.row(go_to_main_page_button, repeat_button)
    bot.send_message(message.chat.id, request_confirmation_messaget_text, reply_markup=confirm_markup)
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
    service.get_add_event_response({"admin_telegram_id": message.from_user.username, "title": message.text,
                                    "description": message.text})
    bot.send_message(message.chat.id, event_was_created_message_text(event_name))
    open_event_page(message)


def join_event_handler(message):
    if message.text == go_to_main_page_text:
        open_main_page(message)
    elif message.text == try_again_text:
        bot.register_next_step_handler(message, join_event_handler)
    else:
        success = service.get_add_user_to_event_response({"telegram_id": message.from_user.username,
                                                          "title": event_name})["body"]["success"]
        if success:
            open_event_page(message, False)
        else:
            markup_join_event = types.ReplyKeyboardMarkup()
            markup_join_event.row(go_to_main_page_button, repeat_button)
            bot.send_message(message.chat.id, event_not_found_message_text, reply_markup=markup_join_event)
            bot.register_next_step_handler(message, join_event_handler)


def open_admin_panel_page(message):
    admin_markup = types.ReplyKeyboardMarkup()
    list_of_participants_button = types.KeyboardButton(list_of_participants_text)
    admin_markup.add(list_of_participants_button)
    bot.send_message(message.chat.id, admin_panel_message_text, reply_markup=admin_markup)
    bot.register_next_step_handler(message, handle_admin_panel)


def handle_admin_panel(message):
    participants = service.get_users_by_event_response({"event_title": event_name})["body"]
    string_text = list_participants_of_event_message_text(event_name)
    for participant in participants:
        string_text += create_user_with_match_message(participant)
    bot.send_message(message.chat.id, string_text, reply_markup=people_list_markup)
    bot.register_next_step_handler(message, handle_people_list)


def open_event_page(message, has_profile_in_event=True):
    is_admin = service.get_is_admin_response({"telegram_id": message.from_user.username,
                                              "event_title": event_name})["body"]["success"]
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
        bot.send_message(
            message.chat.id, event_page_with_empty_profile_message_text(event_name), reply_markup=event_page_markup
        )
    else:
        bot.send_message(
            message.chat.id, event_page_with_empty_profile_message_text(event_name), reply_markup=event_page_markup
        )
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
    result = (
        f'@{user["telegram_id"]} \n' f" Контакт может быть вам интересен, потому что было обнаружено пересечение: \n"
    )
    for tag in user["tags"]:
        result += f"🤝 " + tag + " \n"
    return result


def open_match_list(message):
    candidates = service.get_user_ranking_response({"telegram_id": message.from_user.username,
                                                    "event_title": event_name})["body"]["users"]
    string_text = list_candidates_from_event_message_text(event_name)
    for candidate in candidates:
        string_text += create_user_with_match_message(candidate)
    bot.send_message(message.chat.id, string_text, reply_markup=people_list_markup)
    bot.register_next_step_handler(message, handle_people_list)


def handle_people_list(message):
    if message.text == back_text:
        open_event_page(message)
    elif message.text == go_to_main_page_text:
        open_main_page(message)
    else:
        bot.send_message(message.chat.id, handler_not_found_message_text)
        bot.register_next_step_handler(message, handle_people_list)


@bot.message_handler(content_types=["document"])
def handle_document(message):
    # Получаем информацию о файле
    file_info = bot.get_file(message.document.file_id)
    file_name = message.document.file_name
    file_type = message.document.mime_type

    if file_type.startswith("application/pdf"):
        handle_add_cv(message)
    elif file_type.startswith("application/json"):
        handle_upload_dialogs(message)
    else:
        bot.reply_to(message, f"Файл типа {file_type} не поддерживается.")
    open_event_page(message)


@bot.message_handler(commands=["upload"])
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
        bot.register_next_step_handler(message, handle_upload_dialogs)
    elif message.text == upload_cv_text:
        bot.send_message(message.chat.id, select_file_message_text)
        bot.register_next_step_handler(message, handle_add_cv)
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


def read_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "text" in data:
                return data
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False


def handle_upload_dialogs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        file_type = message.document.mime_type
        if file_type.startswith("application/json"):
            dialogs = read_json_file(file_info)
            if dialogs != False:
                service.get_add_tags_by_dialogue_to_user_response({"telegram_id": message.from_user.username,
                                                                   "text": dialogs})
                bot.reply_to(message, "Файл загружен")
        else:
            bot.reply_to(message, f"Файл типа {file_type} не поддерживается.")
    except:
        bot.reply_to(message, f"Не удалось прочитать файл")
    finally:
        open_event_page(message)


def read_pdf(file_path):
    with open(file_path) as temp_file:
        extracted_text: str = extract_text(temp_file)
        return extracted_text


def handle_add_cv(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        file_type = message.document.mime_type
        if file_type.startswith("application/pdf"):
            try:
                data = read_pdf(file_info)
                service.get_add_tags_by_cv_to_user_response({"telegram_id": message.from_user.username,
                                                             "text": data})
                bot.reply_to(message, f"Загружен PDF-файл: {file_name}")
            except:
                bot.reply_to(message, f"Не удалось загрузить файл {file_name}")
        else:
            bot.reply_to(message, f"Файл типа {file_type} не поддерживается.")
    except:
        bot.reply_to(message, f"Не удалось прочитать файл")
    finally:
        open_event_page(message)


def handle_add_description(message):
    if message.text != cancel_text:
        service.get_add_tags_by_text_to_user_response({"telegram_id": message.from_user.username,
                                                       "text": message.text})
        bot.send_message(message.chat.id, description_was_saved)
    open_event_page(message)


def is_valid_url(url):
    regex = re.compile(r"^(https?:\/\/)?www.linkedin.com([\/\w .-]*)*\/?$", re.IGNORECASE)
    return re.match(regex, url) is not None


def handle_add_link_to_profile(message):
    if is_valid_url(message.text):
        service.get_add_tags_by_link_to_user_response({"telegram_id": message.from_user.username,
                                                       "link": message.text})
        bot.send_message(message.chat.id, link_was_added)
    else:
        bot.send_message(message.chat.id, uncorrect_link_message_text)
    open_event_page(message)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)


if __name__ == "__main__":
    bot.polling(none_stop=True)
