welcome_message_text = ('Бот "НаСвязи" поможет вам определить наиболее интересные контакты на мероприятии. '
                        'Для начала работы создайте мероприятие или присоединитесь к существующему. '
                        'Для поиска совпадений требуется заполнить информацию о себе. '
                        'Вы можете создавать разные профили для разных мероприятий или '
                        'использовать один. '
                        'Также вы можете заполнить базовую информацию в профиль и добавлять для каждого '
                        'события свои дополнительные данные.')

open_main_page_message_text = 'Главная'

handler_not_found_message_text = 'Обработчик команды не найден'
uncorrect_command_message_text = 'Некорректная команда для этого сценария'
request_confirmation_messaget_text = 'Вы уверены?'
function_is_not_available = 'Функция недоступна'

request_event_key_message_text = 'Введите ключ доступа'
admin_panel_message_text = 'Панель администратора'

event_not_found_message_text = 'К сожалению, мероприятия по такому плючу не найдено'
enter_event_name_message_text = 'Введите название мероприятия'
event_was_created_message_text = lambda event_name : (f'Мероприятие "{event_name}" успешно создано!')
on_event_page_message_text = lambda event_name : (f'Вы находитесь в мероприятии {event_name}')

event_page_with_empty_profile_message_text = lambda event_name : (f'Вы находитесь в мероприятии "{event_name}". '
                                              'Вы можете добавить или удалить данные о себе. '
                                              'Чем больше информации вы загрузите, '
                                              'тем лучше программа сможет подобрать вам совпадение')

select_data_type_message_text = 'Выберите тип данных для определения ваших интересов'

select_file_message_text = 'Выберите файл для загрузки'
request_link_message_text = 'Укажите URL адрес'
uncorrect_link_message_text = 'Некорректная ссылка'
request_description_message_text = 'Введите описание'
description_was_saved = 'Описание сохранено'
link_was_added = 'Ссылка на профиль сохранена'
user_profiles_doesnt_exist = 'У вас нет созданных профилей'
saved_profiles_doesnt_exist = 'Нет сохранённых профилей'

list_candidates_from_event_message_text = lambda event_name : (f'Список наиболее подходящих кандидатов из события '
                                                               f'"{event_name}": \n\n')

list_participants_of_event_message_text = lambda event_name : (f'Список участников события '
                                                               f'"{event_name}": \n\n')