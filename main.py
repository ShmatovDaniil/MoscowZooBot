import telebot
from config import TOKEN
from error_handler import handle_error, logging


bot = telebot.TeleBot(TOKEN)

questions = [
    ("Какое качество вы цените в себе больше всего?", ["A. Сила", "B. Мудрость", "C. Доброта", "D. Смелость"]),
    ("Как вы предпочитаете проводить свободное время?", ["A. Заниматься спортом или активными играми", "B. Читая книги или изучая что-то новое", "C. Помогая другим или проводя время с близкими", "D. Путешествуя и исследуя новые места"]),
    ("Как вы реагируете на стрессовые ситуации?", ["A. Сохраняю спокойствие и действую решительно", "B. Обдумываю все возможные варианты", "C. Ищу поддержку у друзей и семьи", "D. Действую инстинктивно и быстро"]),
    ("Какое из этих мест вам ближе всего?", ["A. Горы или леса", "B. Озера или реки", "C. Город или деревня", "D. Пустыня или пляж"]),
    ("Как вы обычно принимаете решения?", ["A. Полагаюсь на логику и факты", "B. Слушаю свою интуицию", "C. Обсуждаю с другими", "D. Действую спонтанно"]),
    ("Как вы относитесь к переменам?", ["A. Я люблю перемены и новые вызовы", "B. Я предпочитаю стабильность, но готов к изменениям", "C. Я немного боюсь перемен, но стараюсь адаптироваться", "D. Я не боюсь перемен, они меня вдохновляют"]),
    ("Как вы справляетесь с конфликтами?", ["A. Стараюсь решить их быстро и эффективно", "B. Предпочитаю обсуждать и находить компромисс", "C. Избегаю конфликтов, если это возможно", "D. Сражаюсь за свои убеждения"]),
    ("Как вы относитесь к новым знакомствам?", ["A. Я люблю знакомиться с новыми людьми", "B. Я предпочитаю общаться с близкими друзьями", "C. Я немного стесняюсь, но открываю свое сердце", "D. Я всегда готов к новым знакомствам и приключениям"]),
    ("Какое ваше любимое время года?", ["A. Лето — время активности и приключений", "B. Осень — время размышлений и изменений", "C. Зима — время уюта и спокойствия", "D. Весна — время обновления и роста"]),
    ("Как вы относитесь к риску?", ["A. Я люблю рисковать и пробовать новое", "B. Я предпочитаю осторожный подход", "C. Я взвешиваю риски перед принятием решения", "D. Я иногда рискую, если это того стоит"]),
]

totem_animals = {
    "Тигр": ("Ты - Тигр! Символ силы и храбрости.", "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/71062cdc-ae27-432a-84ed-d3743afd903b.jpeg"),
    "Сова": ("Ты - Сова! Символ мудрости и интуиции.", "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/e2f19554-2ab4-453e-b796-a2e975d8090d.jpg"),
    "Медведь": ("Ты - Медведь! Символ дружбы и игривости.", "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/b535fefc-6867-497b-a278-05966e32ff2d.jpg"),
    "Волк": ("Ты - Волк! Символ свободы и независимости.", "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/a26086b0-53a3-452a-8552-5f5cef835879.jpg"),
}

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    logging.info(f"User  @{message.from_user.username} initiated the quiz.")
    text = "👋 Привет! Я — ваш дружелюбный бот, и сегодня мы отправимся в увлекательное путешествие, чтобы узнать, какое у вас тотемное животное!🐾\n\n" \
           "🎉 В ходе викторины я задам вам несколько вопросов о ваших предпочтениях и интересах. На основе ваших ответов я подберу животное, которое идеально вам подходит!\n\n" \
           "🐻 Но это еще не все! В конце викторины вы получите информацию о том, как стать опекуном этого замечательного животного в нашем зоопарке.\n\n" \
           "Готовы начать? Нажмите на кнопку '/go', и давайте узнаем, кто ваш тотемный спутник!"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['go'])
def restart(message):
    user_data[message.chat.id] = {"A": 0, "B": 0, "C": 0, "D": 0, "question_index": 0}
    logging.info(f"User  @{message.from_user.username} restarted the quiz.")
    ask_question(message)

@bot.message_handler(commands=['send'])
def send_us(message):
    bot.reply_to(message, "Пожалуйста, введите ваше имя:")
    bot.register_next_step_handler(message, ask_phone)

def ask_phone(message):
    user_name = message.text
    bot.reply_to(message, "Спасибо, {}! Теперь, пожалуйста, введите ваш номер телефона:".format(user_name))
    bot.register_next_step_handler(message, ask_email, user_name)

def ask_email(message, user_name):
    user_phone = message.text
    bot.reply_to(message, "Отлично! Теперь, пожалуйста, введите ваш email:")
    bot.register_next_step_handler(message, save_contact_info, user_name, user_phone)

def save_contact_info(message, user_name, user_phone):
    user_email = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        with open('contacts.txt', 'a', encoding='utf-8') as f:
            f.write(f"Данные от @{username} (ID: {user_id}): Имя: {user_name}, Телефон: {user_phone}, Email: {user_email}\n")
        bot.send_message(message.chat.id, "Спасибо! Ваши данные успешно отправлены. 😊\n\nОжидайте звонок и письмо в течении 24 часов")
        logging.info(f"Contact info received from @{username}: {user_name}, {user_phone}, {user_email}")
    except Exception as e:
        handle_error(bot, message.chat.id, e)

@bot.message_handler(commands=['feedback'])
def collect_feedback(message):
    bot.reply_to(message, "Пожалуйста, напишите ваш отзыв:")
    bot.register_next_step_handler(message, save_feedback)

def save_feedback(message):
    feedback = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        with open('feedback.txt', 'a', encoding='utf-8') as f:
            f.write(f"Отзыв от @{username} (ID: {user_id}):\n{feedback}\n\n")
        bot.send_message(message.chat.id, "Спасибо за ваш отзыв! Мы ценим ваше мнение! 😊")
        logging.info(f"Feedback received from @{username}: {feedback}")
    except Exception as e:
        handle_error(bot, message.chat.id, e)

@bot.message_handler(commands=['contact'])
def contact(message):
    try:
        text = "📞 Вы можете связаться с нами по следующим каналам:\n\n" \
               "✉️ Email: zoofriends@moscowzoo.ru\n\n" \
               "📱 Телефон: +7 (962) 971-38-75\n\n" \
               "🌐 Веб-сайт: https://moscowzoo.ru/animals/kinds\n\n" \
               "Если у вас есть вопросы или предложения, не стесняйтесь писать нам!"
        bot.reply_to(message, text)
        logging.info(f"Contact information sent to user @{message.from_user.username}.")
    except Exception as e:
        handle_error(bot, message.chat.id, e)

@bot.message_handler(commands=['info'])
def about_us(message):
    try:
        text = f"Московский зоопарк — один из старейших зоопарков Европы. Он был открыт 31 января 1864 года по старому стилю и назывался тогда зоосадом.\n\n" \
               "Московский зоопарк был организован Императорским русским обществом акклиматизации животных и растений. Начало его существования связано с замечательными именами профессоров Московского Университета Карла Францевича Рулье, Анатолия Петровича Богданова и Сергея Алексеевича Усова.\n\n" \
               "Местность, где теперь находится Старая территория зоопарка, называлась «Пресненские пруды». Здесь протекала довольно широкая река Пресня, и было одно из любимых мест гуляний москвичей — зелёные холмы, заливные луга, цветущие сады украшали окрестности.\n\n" \
               "Для создания зоосада большинством голосов членов Общества акклиматизации был выбран именно этот участок, так как он находился на доступном расстоянии для всех москвичей, в том числе и небогатых. Территория Петровской академии, например, была удобнее и больше, но ездить туда было бы далеко и дорого для большинства потенциальных посетителей.\n\n"
        bot.reply_to(message, text)
        logging.info(f"Information about the zoo sent to user @{message.from_user.username}.")
    except Exception as e:
        handle_error(bot, message.chat.id, e)

def ask_question(message):
    user_id = message.chat.id
    if user_id not in user_data:
        user_data[user_id] = {"A": 0, "B": 0, "C": 0, "D": 0, "question_index": 0}
        logging.info(f"User  @{user_id} started the quiz.")

    index = user_data[user_id]["question_index"]
    if index < len(questions):
        question, options = questions[index]
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for option in options:
            markup.add(option)
        bot.send_message(user_id, question, reply_markup=markup)
        logging.info(f"Question {index + 1} sent to user @{user_id}: {question}")
    else:
        show_result(message)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.chat.id
    if user_id in user_data:
        question_index = user_data[user_id]["question_index"]
        if question_index < len(questions):
            answer = message.text.strip().upper()[0]
            if answer in ['A', 'B', 'C', 'D']:
                user_data[user_id][answer] += 1
                user_data[user_id]["question_index"] += 1  # Переход к следующему вопросу
                logging.info(f"User  @{user_id} answered {answer} for question {question_index + 1}.")
                ask_question(message)
            else:
                logging.warning(f"User  {user_id} provided an invalid answer: {message.text}")
                bot.send_message(user_id, "Пожалуйста, выберите правильный вариант ответа (A, B, C или D).")
        else:
            logging.info(f"User  @{user_id} attempted to answer after quiz completion.")
            bot.send_message(user_id, "Вы уже завершили викторину!")

def show_result(message):
    user_id = message.chat.id
    scores = {
        "A": user_data[user_id]["A"],
        "B": user_data[user_id]["B"],
        "C": user_data[user_id]["C"],
        "D": user_data[user_id]["D"],
    }

    # Определяем тотемное животное на основе максимального количества ответов
    totem = max(scores, key=scores.get)
    logging.info(f"User @{user_id} has a totem animal: {totem}.")

    if totem == "A":
        message_text, image_url = totem_animals["Тигр"]
    elif totem == "B":
        message_text, image_url = totem_animals["Сова"]
    elif totem == "C":
        message_text, image_url = totem_animals["Медведь"]
    else:
        message_text, image_url = totem_animals["Волк"]

    share_link = "тут ссылка на поделиться"
    bot.send_photo(user_id, image_url,
                   caption=f"{message_text}\n\nХотите поделиться своим результатом в социальных сетях? Вот ссылка: \n{share_link}")
    logging.info(f"Result sent to user @{user_id}: {message_text}.")

    text = f"Если хотите пройти тест заново нажмите: /go\n\n"\
            "Если хотите узнать больше о программе опекунства нажмите: \n/info\n\n"\
            "Если хотите оставить заявку на опекунство животного нажмите: \n/send и заполните анкету\n\n"\
            "Если хотите проконсультироваться по программе опеке и стать опекуном вы можете связаться с нами: /contact\n\n"\
            "Если хотите оставить отзыв о боте и программе опекунства нажмите: \n/feedback\n"\

    bot.send_message(user_id, text, parse_mode="Markdown")

if __name__ == '__main__':
    logging.info("Bot is starting...")
    bot.polling(none_stop=True) 