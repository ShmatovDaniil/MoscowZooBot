import logging
import sys

# Настройка логирования для вывода в файл и терминал
logging.basicConfig(
    filename='bot_log.log',  # Логирование в файл
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат логов
)

# Создаем обработчик для вывода логов в терминал
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # Уровень для терминала
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Добавляем обработчик к корневому логгеру
logging.getLogger().addHandler(console_handler)

def handle_error(bot, chat_id, error):
    logging.error(f"Ошибка в чате {chat_id}: {error}")
    bot.send_message(chat_id, "Произошла ошибка. Пожалуйста, попробуйте еще раз позже.")
