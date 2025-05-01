
import os
from pathlib import Path
import mysql.connector
import dotenv

# Загрузка переменных окружения
dotenv.load_dotenv(Path(__file__).parent / '.env')

# Конфигурация базы данных
db_config_read = {
    'host': os.environ.get("host_read"),
    'user': os.environ.get("user_read"),
    'password': os.environ.get("password_read"),
    'database': 'sakila'  # ✅ База, откуда читаем фильмы!
}

db_config_write = {
    'host': os.environ.get("host_write"),
    'user': os.environ.get("user_write"),
    'password': os.environ.get("password_write"),
    'database': 'group_111124_fp_Elena_Marshalova'  # ✅ База, куда записываем популярные запросы
}
# Функции подключения с обработкой ошибок
def get_read_connection():
    try:
        conn = mysql.connector.connect(**db_config_read)
        print("✅ Успешное подключение к READ базе данных")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Ошибка подключения к READ базе: {err}")
        return None

def get_write_connection():
    try:
        conn = mysql.connector.connect(**db_config_write)
        print("✅ Успешное подключение к WRITE базе данных")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Ошибка подключения к WRITE базе: {err}")
        return None

