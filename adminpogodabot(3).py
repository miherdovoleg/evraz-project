import json
import requests
import telebot
from telebot import types

bot = telebot.TeleBot('7057079309:AAHMuhcO8p-udULRN5LJCrS3l3_Ua01P10o')

employee = {}
employees = []

work_type = {}
work_types = []

conditions = {}

date = {}
grafik = []

is_edit = False


def add_employee_fio(message):
    global employee
    employee['fio'] = message.text
    bot.send_message(message.from_user.id, text='Введите должность сотрудника')
    bot.register_next_step_handler(message, add_employee_post)


def add_employee_post(message):
    global employee
    employee['post'] = message.text
    bot.send_message(message.from_user.id, text='Укажите ссылку на профиль сотрудника в Телеграм')
    bot.register_next_step_handler(message, add_employee_link)


def add_employee_link(message):
    global employee, employees
    employee['link'] = message.text
    file = open('employees.json', 'r', encoding='utf-8')
    if file.read() != '':
        file.seek(0)
        employees = json.load(file)
    file.close()

    employees.append(employee)

    file = open('employees.json', 'w', encoding='utf-8')
    json.dump(employees, file, ensure_ascii=False)
    file.close()


def add_work_type(message):
    global work_type, work_types
    work_type['type'] = message.text
    bot.send_message(message.from_user.id, text='Укажите ограничения для проведения работ')
    bot.send_message(message.from_user.id, text='Укажите минимальную температуру, допустимую для проведения работ')
    bot.register_next_step_handler(message, add_work_conditions_min_temp)


def add_work_conditions_min_temp(message):
    global conditions
    conditions['min_temp'] = message.text
    bot.send_message(message.from_user.id, text='Укажите максимальную температуру, допустимую для проведения работ')
    bot.register_next_step_handler(message, add_work_conditions_max_temp)


keyboard1 = types.InlineKeyboardMarkup()
button11 = types.InlineKeyboardButton(text='Да', callback_data='rainfall_true')
button22 = types.InlineKeyboardButton(text='Нет', callback_data='rainfall_false')

keyboard1.add(button11, button22)

keyboard2 = types.InlineKeyboardMarkup()
button111 = types.InlineKeyboardButton(text='Да', callback_data='snow_true')
button222 = types.InlineKeyboardButton(text='Нет', callback_data='snow_false')

keyboard2.add(button111, button222)


def add_work_conditions_max_temp(message):
    global conditions
    conditions['max_temp'] = message.text
    bot.send_message(message.from_user.id, text="Уточните, возможно ли проведение работ в дождь (Да/Нет)",
                     reply_markup=keyboard1)
    # bot.register_next_step_handler(message, add_work_conditions_rainfall)


def add_work_conditions_rainfall(message):
    global conditions, keyboard1
    conditions['rainfall'] = keyboard1.callback_data
    bot.send_message(message.from_user.id, text='Уточните, возможно ли проведение работ в снегопад (Да/Нет)',
                     reply_markup=keyboard2)
    bot.register_next_step_handler(message, add_work_conditions_snow)


def add_work_conditions_snow(message):
    global conditions, keyboard2
    conditions['snow'] = keyboard2.callback_data
    bot.send_message(message.from_user.id, text='Данные сохранены')

def edit_work_type(message):
    global conditions, work_type

    work_type['type'] = message.text
    file = open('work_types.json', 'r', encoding='utf-8')
    text = 'Проверьте введенные данные:\n\n\n'
    if 'type' in work_type:
        text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n\n'
    if 'min_temp' in conditions:
        text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
    if 'max_temp' in conditions:
        text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
    if 'rainfall' in conditions:
        if conditions['rainfall'] == True:
            text += 'Возможно проводить в дождь: Да' + '\n\n'
        else:
            text += 'Возможно проводить в дождь: Нет' + '\n\n'
    if 'snow' in conditions:
        if conditions['snow'] == True:
            text += 'Возможно проводить в снегопад: Да' + '\n'
        else:
            text += 'Возможно проводить в снегопад: Нет' + '\n'
    keyboard4 = types.InlineKeyboardMarkup()
    buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
    buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
    keyboard4.add(buttonfile, buttonfile1)
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard4)
    file.close()


def edit_min_temp(message):
    global conditions, keyboard4
    conditions['min_temp'] = message.text
    file = open('work_types.json', 'r', encoding='utf-8')
    text = 'Проверьте введенные данные:\n\n\n'
    if 'type' in work_type:
        text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n\n'
    if 'min_temp' in conditions:
        text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
    if 'max_temp' in conditions:
        text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
    if 'rainfall' in conditions:
        if conditions['rainfall'] == True:
            text += 'Возможно проводить в дождь: Да' + '\n\n'
        else:
            text += 'Возможно проводить в дождь: Нет' + '\n\n'
    if 'snow' in conditions:
        if conditions['snow'] == True:
            text += 'Возможно проводить в снегопад: Да' + '\n'
        else:
            text += 'Возможно проводить в снегопад: Нет' + '\n'
    keyboard4 = types.InlineKeyboardMarkup()
    buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
    buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
    keyboard4.add(buttonfile, buttonfile1)
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard4)
    file.close()

def edit_max_temp(message):
    global conditions, keyboard4
    conditions['max_temp'] = message.text
    file = open('work_types.json', 'r', encoding='utf-8')
    text = 'Проверьте введенные данные:\n\n\n'
    if 'type' in work_type:
        text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n\n'
    if 'min_temp' in conditions:
        text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
    if 'max_temp' in conditions:
        text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
    if 'rainfall' in conditions:
        if conditions['rainfall'] == True:
            text += 'Возможно проводить в дождь: Да' + '\n\n'
        else:
            text += 'Возможно проводить в дождь: Нет' + '\n\n'
    if 'snow' in conditions:
        if conditions['snow'] == True:
            text += 'Возможно проводить в снегопад: Да' + '\n'
        else:
            text += 'Возможно проводить в снегопад: Нет' + '\n'
    keyboard4 = types.InlineKeyboardMarkup()
    buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
    buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
    keyboard4.add(buttonfile, buttonfile1)
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard4)
    file.close()

def edit_rainfall(message):
    global conditions, keyboard4, keyboard1
    conditions['rainfall'] = keyboard1.callback_data
    file = open('work_types.json', 'r', encoding='utf-8')
    text = 'Проверьте введенные данные:\n\n\n'
    if 'type' in work_type:
        text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n\n'
    if 'min_temp' in conditions:
        text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
    if 'max_temp' in conditions:
        text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
    if 'rainfall' in conditions:
        if conditions['rainfall'] == True:
            text += 'Возможно проводить в дождь: Да' + '\n\n'
        else:
            text += 'Возможно проводить в дождь: Нет' + '\n\n'
    if 'snow' in conditions:
        if conditions['snow'] == True:
            text += 'Возможно проводить в снегопад: Да' + '\n'
        else:
            text += 'Возможно проводить в снегопад: Нет' + '\n'
    keyboard4 = types.InlineKeyboardMarkup()
    buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
    buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
    keyboard4.add(buttonfile, buttonfile1)
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard4)
    file.close()

def edit_snow(message):
    global conditions, keyboard4
    conditions['snow'] = keyboard2.callback_data
    file = open('work_types.json', 'r', encoding='utf-8')
    text = 'Проверьте введенные данные:\n\n\n'
    if 'type' in work_type:
        text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n\n'
    if 'min_temp' in conditions:
        text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
    if 'max_temp' in conditions:
        text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
    if 'rainfall' in conditions:
        if conditions['rainfall'] == True:
            text += 'Возможно проводить в дождь: Да' + '\n\n'
        else:
            text += 'Возможно проводить в дождь: Нет' + '\n\n'
    if 'snow' in conditions:
        if conditions['snow'] == True:
            text += 'Возможно проводить в снегопад: Да' + '\n'
        else:
            text += 'Возможно проводить в снегопад: Нет' + '\n'
    keyboard4 = types.InlineKeyboardMarkup()
    buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
    buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
    keyboard4.add(buttonfile, buttonfile1)
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard4)
    file.close()

def add_date_start(message):
    global date
    file = open('work_types.json', 'r', encoding='utf-8')
    work_types = json.load(file)
    index = int(message.text) - 1
    work_type = work_types[index]['type']
    date['work_type'] = work_type
    bot.send_message(message.from_user.id, text='Укажите дату начала проведения работ в формате дд.мм.гггг')
    bot.register_next_step_handler(message, add_date_end)
    file.close()

def add_date_end(message):
    global date
    date['date_start'] = message.text
    bot.send_message(message.from_user.id, text='Укажите дату окончания проведения работ в формате дд.мм.гггг')
    bot.register_next_step_handler(message, all_employees)

def all_employees(message):
    global employees, employee
    text = 'Выберите ответственного сотрудника (в сообщении отправьте только номер)\n\n\n'

    file1 = open('employees.json', 'r', encoding='utf-8')
    employees = json.load(file1)
    for i in range(len(employees)):
        text += str(i + 1) + '. ' + employees[i]['fio'] + '\n\n'
    bot.send_message(message.from_user.id, text=text)
    bot.register_next_step_handler(message, head_employee)
    file1.close()

def head_employee(message):
    file = open('employees.json', 'r', encoding='utf-8')
    employees = json.load(file)
    index = int(message.text) - 1
    employee = employees[index]['fio']
    date['head_employee'] = employee
    file.close()
    print(date)

     # добавить список сотрудников для выбора ответственного

    #
    # text = 'Выберите ответственного сотрудника (в сообщении отправьте только номер)\n\n\n'
    # file1 = open('employees.json', 'r', encoding='utf-8')
    # employees = json.load(file1)
    # for i in range(len(employees)):
    #     text += str(i + 1) + '. ' + employees[i]['fio'] + '\n\n'
    # bot.send_message(message.from_user.id, text=text)
    # file1.close()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global keyboard1, keyboard2
    # Проверка на доступ пользователя
    file = open('admins.json', 'r', encoding='utf-8')
    admins = json.load(file)
    if str(message.from_user.id) not in admins.keys():
        bot.send_message(message.from_user.id, text='У Вас нет доступа')
    else:
        if message.text == '/start':
            # Создание меню с командами
            bot.set_my_commands(
                commands=[
                    types.BotCommand('/start', 'Начать работу с ботом'),
                ],
                scope=types.BotCommandScopeChat(message.chat.id)
            )
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text='Вид проводимых работ', callback_data='Вид проводимых работ')
            button2 = types.InlineKeyboardButton(text='Ответсвенного сотрудника',
                                                 callback_data='Ответсвенного сотрудника')
            button3 = types.InlineKeyboardButton(text='График проведения работ',
                                                 callback_data='График проведения работ')

            keyboard.add(button1, button2, button3)

            keyboard1 = types.InlineKeyboardMarkup()
            button11 = types.InlineKeyboardButton(text='Да', callback_data='rainfall_true')
            button22 = types.InlineKeyboardButton(text='Нет', callback_data='rainfall_false')

            keyboard1.add(button11, button22)

            keyboard2 = types.InlineKeyboardMarkup()
            button111 = types.InlineKeyboardButton(text='Да', callback_data='snow_true')
            button222 = types.InlineKeyboardButton(text='Нет', callback_data='snow_false')

            keyboard2.add(button111, button222)

            bot.send_message(message.from_user.id, text='Привет! Добро пожаловать')
            bot.send_message(message.from_user.id, text="Выберите, что хотите добавить/редактировать",
                             reply_markup=keyboard)


# Обработчик нажатия
@bot.callback_query_handler(func=lambda call: True)
# Функция обработки нажатия на кнопку
def callback_worker(call):
    global work_type, keyboard1, keyboard2, keyboard3, is_edit, keyboard

    if call.data == 'Вид проводимых работ':
        bot.send_message(call.message.chat.id, text='Добавьте вид проводимых работ')
        bot.send_message(call.message.chat.id, text='Введите название вида работ')
        bot.register_next_step_handler(call.message, add_work_type)

    elif call.data == 'Ответсвенного сотрудника':
        bot.send_message(call.message.chat.id, text='Добавьте ответственного сотрудника')
        bot.send_message(call.message.chat.id, text='Введите ФИО ответственного сотрудника')
        bot.register_next_step_handler(call.message, add_employee_fio)

    elif call.data == 'rainfall_true':
        conditions['rainfall'] = True

        keyboard2 = types.InlineKeyboardMarkup()
        button11 = types.InlineKeyboardButton(text='Да', callback_data='snow_true')
        button22 = types.InlineKeyboardButton(text='Нет', callback_data='snow_false')
        keyboard2.add(button11, button22)
        if not is_edit:
            bot.send_message(call.message.chat.id, text='Уточните, возможно ли проведение работ в снег (Да/Нет)', reply_markup=keyboard2)
        else:
            file = open('work_types.json', 'r', encoding='utf-8')
            text = 'Проверьте введенные данные:\n\n\n'
            if 'type' in work_type:
                text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n'
            if 'min_temp' in conditions:
                text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
            if 'max_temp' in conditions:
                text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
            if 'rainfall' in conditions:
                if conditions['rainfall'] == True:
                    text += 'Возможно проводить в дождь: Да' + '\n\n'
                else:
                    text += 'Возможно проводить в дождь: Нет' + '\n\n'
            if 'snow' in conditions:
                if conditions['snow'] == True:
                    text += 'Возможно проводить в снегопад: Да' + '\n'
                else:
                    text += 'Возможно проводить в снегопад: Нет' + '\n'
            keyboard4 = types.InlineKeyboardMarkup()
            buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
            buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
            keyboard4.add(buttonfile, buttonfile1)
            bot.send_message(call.message.chat.id, text=text, reply_markup=keyboard4)
            file.close()


    elif call.data == 'rainfall_false':
        conditions['rainfall'] = False

        keyboard2 = types.InlineKeyboardMarkup()
        button11 = types.InlineKeyboardButton(text='Да', callback_data='snow_true')
        button22 = types.InlineKeyboardButton(text='Нет', callback_data='snow_false')
        keyboard2.add(button11, button22)
        if not is_edit:
            bot.send_message(call.message.chat.id, text='Уточните, возможно ли проведение работ в снег (Да/Нет)', reply_markup=keyboard2)

    elif call.data == 'snow_true' or call.data == 'snow_false':
        if call.data == 'snow_true':
            conditions['snow'] = True
        else:
            conditions['snow'] = False
        file = open('work_types.json', 'r', encoding='utf-8')
        text = 'Проверьте введенные данные:\n\n\n'
        if 'type' in work_type:
            text += 'Вид проводимых работ: ' + work_type['type'] + '\n\n'
        if 'min_temp' in conditions:
            text += 'Мин. допустимая температура: ' + conditions['min_temp'] + '\n\n'
        if 'max_temp' in conditions:
            text += 'Макс. допустимая температура: ' + conditions['max_temp'] + '\n\n'
        if 'rainfall' in conditions:
            if conditions['rainfall'] == True:
                text += 'Возможно проводить в дождь: Да' + '\n\n'
            else:
                text += 'Возможно проводить в дождь: Нет' + '\n\n'
        if 'snow' in conditions:
            if conditions['snow'] == True:
                text += 'Возможно проводить в снегопад: Да' + '\n'
            else:
                text += 'Возможно проводить в снегопад: Нет' + '\n'
        keyboard4 = types.InlineKeyboardMarkup()
        buttonfile = types.InlineKeyboardButton(text='Сохранить', callback_data='save_file')
        buttonfile1 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit_file')
        keyboard4.add(buttonfile, buttonfile1)
        bot.send_message(call.message.chat.id, text=text, reply_markup=keyboard4)
        file.close()
    if call.data == 'save_file':
        filesave = open('work_types.json', 'r', encoding='utf-8')
        worktypes = json.load(filesave)
        filesave.close()
        filesave1 = open('work_types.json', ' ', encoding='utf-8')
        worktypes.append({
            **work_type,
            "conditions": {
                **conditions
            }
        })
        json.dump(worktypes, filesave1, ensure_ascii=False)
        filesave1.close()
        bot.send_message(call.message.chat.id, text='Вид проводимых работ успешно сохранен')

        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Вид проводимых работ', callback_data='Вид проводимых работ')
        button2 = types.InlineKeyboardButton(text='Ответсвенного сотрудника',
                                             callback_data='Ответсвенного сотрудника')
        button3 = types.InlineKeyboardButton(text='График проведения работ',
                                             callback_data='График проведения работ')

        keyboard.add(button1, button2, button3)
        bot.send_message(call.message.chat.id, text="Выберите, что хотите добавить/редактировать", reply_markup=keyboard)

    if call.data == 'edit_file':
        is_edit = True
        keyboard3 = types.InlineKeyboardMarkup()
        button_edit_work_type = types.InlineKeyboardButton(text='Вид работ', callback_data='edit_file_work_type')
        button_edit_min_temp = types.InlineKeyboardButton(text='Мин. температура', callback_data='edit_file_min_temp')
        button_edit_max_temp = types.InlineKeyboardButton(text='Макс. температура', callback_data='edit_file_max_temp')
        button_edit_rainfall = types.InlineKeyboardButton(text='Дождь', callback_data='edit_file_rainfall')
        button_edit_snow = types.InlineKeyboardButton(text='Снег', callback_data='edit_file_snow')
        keyboard3.add(button_edit_work_type, button_edit_min_temp, button_edit_max_temp, button_edit_rainfall, button_edit_snow)
        bot.send_message(call.message.chat.id, text='Выберите, что редактировать', reply_markup=keyboard3)


    if call.data == 'edit_file_work_type':
        bot.send_message(call.message.chat.id, text='Введите название вида работ')
        bot.register_next_step_handler(call.message, edit_work_type)

    if call.data == 'edit_file_min_temp':
        bot.send_message(call.message.chat.id, text='Укажите минимальную температуру')
        bot.register_next_step_handler(call.message, edit_min_temp)

    if call.data == 'edit_file_max_temp':
        bot.send_message(call.message.chat.id, text='Укажите максимальную температуру')
        bot.register_next_step_handler(call.message, edit_max_temp)

    if call.data == 'edit_file_rainfall':
        bot.send_message(call.message.chat.id, text='Можно проводить в дождь',  reply_markup=keyboard1)
        bot.register_next_step_handler(call.message, edit_rainfall)

    if call.data == 'edit_file_snow':
        bot.send_message(call.message.chat.id, text='Можно проводить в снег', reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, edit_snow)


    elif call.data == 'График проведения работ':
        text = 'Выберите вид работ для изменения графика проведения (в сообщении отправьте только номер)\n\n\n'
        file1 = open('work_types.json', 'r', encoding='utf-8')
        file2 = open('employees.json', 'r', encoding='utf-8')
        worktypes = json.load(file1)
        for i in range(len(worktypes)):
            text += str(i + 1) + '. ' + worktypes[i]['type'] + '\n\n'
        bot.send_message(call.message.chat.id, text=text)
        bot.register_next_step_handler(call.message, add_date_start)
        file1.close()
        file2.close()




bot.polling(none_stop=True, interval=0)