import mysql.connector
from database import get_read_connection, get_write_connection
import queries
from itertools import islice

# Подключение к базам
conn_read = get_read_connection()
cursor_read = conn_read.cursor()
conn_write = get_write_connection()
cursor_write = conn_write.cursor()



def execute_query(cursor, query, params=()):
    try:
        # print(f"DEBUG: Выполняем запрос - {query}, Параметры - {params}")
        cursor.execute(query, params) if params else cursor.execute(query)
        results = cursor.fetchall()
        # print(f"DEBUG: Полученные данные - {results}")
        return results
    except mysql.connector.Error as err:
        print(f"❌ Ошибка выполнения SQL-запроса: {err}")
        return []


def search_films_by_keyword(cursor_read, cursor_write, conn_write, query, params, keyword):
    """Выполняет поиск фильмов по ключевому слову и записывает запрос в базу популярных запросов."""
    cursor_read.execute(query, tuple(params))
    films = cursor_read.fetchall()

    # Записываем ключевое слово в базу **независимо от результата**
    cursor_write.execute(queries.INSERT_POPULAR_SEARCH, (keyword,))
    conn_write.commit()

    if not films:
        print("\n❗+ Фильмы по заданному ключевому слову не найдены.")  # ✅  сообщение появляется корректно!
        return []  # Возвращаем пустой список

    return films

def get_genres(cursor_read):
    """Получает и выводит список доступных жанров."""
    category_data = dict(execute_query(cursor_read, queries.GET_CATEGORIES))
    print("\n📌 Доступные жанры:")
    for category_id, name in category_data.items():
        print(f"{category_id}: {name}")
    return category_data

def search_by_genre(cursor_read, cursor_write, conn_write, ask_year=False):

    """Выбор жанра и, при необходимости, года."""
    # category_data = get_genres(cursor_read, conn_read)
    category_data = get_genres(cursor_read)
    while True:
        user_choice = input("\nВведите номер жанра (1 - 16): ").strip()
        if not user_choice.isdigit() or int(user_choice) not in category_data:
            print("❌ Ошибка: Введите корректный номер жанра.")
            continue
        genre_number = int(user_choice)
        break

    film_year = None
    if ask_year:
        while True:
            film_year = input("Введите год фильма (1990 - 2025) или Enter для пропуска: ").strip()

            if not film_year:  # 🔥 Если пусто, пропускаем выбор
                break

            if film_year.isdigit() and 1990 <= int(film_year) <= 2025:
                film_year = int(film_year)
                break  # ✅ Корректный год → выходим из цикла

            print("❌ Ошибка: Введите корректный год.")  # 🔥 Неправильный ввод → повторяем запрос

    query = queries.GET_FILMS_BY_GENRE_AND_YEAR if ask_year and film_year else queries.GET_FILMS_BY_GENRE
    params = [category_data[genre_number]] + ([film_year] if film_year else [])
    films = execute_query(cursor_read, query, tuple(params))

    if not films:  # 🔥 Если список фильмов пуст, показываем сообщение
        print("\n❗ Фильмы по указанному жанру и году не найдены.")
        return []

    execute_query(cursor_write, queries.INSERT_POPULAR_GENRE, (category_data[genre_number],))
    conn_write.commit()

    return films


def display_films(films, cursor_read):
    """Вывод списка найденных фильмов с возможностью просмотра ещё 10 или выбора фильма по ID."""
    if not films:
        print("\n❗ Фильмы не найдены.")
        return

    print("\n🎬 Найденные фильмы:")

    for i in range(0, len(films), 10):
        print("\n📌 Блок фильмов:")
        for film in islice(films, i, i + 10):
            film_id, title, genre, release_year, description = film
            print(f"ID: {film_id}, 🎬 Название: {title}, 🗂️ Жанр: {genre}, 📆 Год: {release_year}\n"
                  f"               📝Описание: {description}")

        if i + 10 < len(films):
            while True:
                user_choice = input("\n🔍 Введите:\n1️⃣ - Показать ещё 10 фильмов\n2️⃣ - Выбрать фильм по ID\n"
                                    "0️⃣ - Завершить просмотр\nВаш выбор: ").strip()

                if user_choice == "1":
                    break  # Продолжаем просмотр следующего блока
                elif user_choice == "2":
                    return select_film_by_id(cursor_read, films)  # 🔥 Переход к выбору фильма
                elif user_choice == "0":
                    print("⏭️ Завершение просмотра.")
                    return
                else:
                    print("❌ Ошибка: Введите 1, 2 или 0.")


def select_film_by_id(cursor_read, films):
    """Позволяет пользователю выбрать фильм по ID и получить подробности."""
    film_ids = {film[0] for film in films}  # 🔥 Получаем список доступных ID

    while True:
        selected_id = input("\nВведите ID фильма для подробного просмотра (или 0 для выхода): ").strip()
        if selected_id.isdigit():
            selected_id = int(selected_id)

            if selected_id == 0:
                print("⏭️ Выход из выбора фильма.")
                return  # 🔥 Завершаем работу, если пользователь выбирает '0'

            if selected_id not in film_ids:  # 🔥 Проверяем, есть ли фильм в списке
                print("❗ Ошибка: Фильм с таким ID не найден в текущем списке.")
                continue  # 🔥 Позволяем пользователю вводить ID снова

            # Запрос информации о фильме
            cursor_read.execute(queries.GET_FILM_BY_ID, [selected_id])
            film_info = cursor_read.fetchone()

            if film_info:
                film_id, title, genre, release_year, description = film_info
                print("\n✅ Вы выбрали фильм:")
                print(f"🎬 Название: {title}")
                print(f"🗂️ Жанр: {genre}")
                print(f"📆 Год выпуска: {release_year}")
                print(f"📝 Описание: {description}")

                while True:
                    user_choice = input("\nХотите выбрать ещё один фильм? (1 - Да, 0 - Нет): ").strip()

                    if user_choice == "1":
                        return  # 🔥 Возвращаемся к главному меню
                    elif user_choice == "0":
                        print("👋 Спасибо за использование программы! До свидания!")
                        exit()  # 🔥 Завершаем работу программы
                    else:
                        print("❌ Ошибка: Введите 1 (да) или 0 (нет).")
                return  # 🔥 Позволяем пользователю выбрать другой ID, вместо завершения
            else:
                print("❗ Ошибка: Фильм с таким ID не найден.")


# --- Основной код ---
search_queries = {
    "1": {"query": queries.GET_FILMS_BY_TITLE, "params": lambda k: [f"%{k}%"]},
    "2": {"query": queries.GET_FILMS_BY_DESCRIPTION, "params": lambda k: [f"%{k}%"]},
    "3": {"query": queries.GET_FILMS_BY_TITLE_OR_DESCRIPTION, "params": lambda k: [f"%{k}%", f"%{k}%"]}
}

while True:
    choice = input("\nВыберите метод поиска:\n"
                   "1️⃣ По ключевому слову в названии фильма\n"
                   "2️⃣ По ключевому слову в описании фильма\n"
                   "3️⃣ По ключевому слову в названии или описании фильма\n"
                   "4️⃣ По жанру\n"
                   "5️⃣ По жанру и году\n"
                   "6️⃣ Популярные запросы\n"
                   "0️⃣ Завершить работу\n"
                   "Введите номер варианта (0-6): ").strip()

    if choice == "0":
        print("👋 Завершение работы. До свидания!")
        break

    films = []

    if choice in search_queries:
        while True:
            keyword = input("Введите ключевое слово (без пробелов): ").strip()

            if " " in keyword:  # 🔥 Проверяем, содержит ли строка пробел
                print("❌ Ошибка: Не используйте пробелы. Введите одно слово.")
                continue  # 🔥 Запрашиваем ввод заново
            elif not keyword:
                print("❌ Ошибка: Ключевое слово не должно быть пустым.")
                continue  # 🔥 Запрашиваем ввод заново
            break  # 🔥 Если ввод корректен, продолжаем поиск фильмов

        query_data = search_queries[choice]
        films = search_films_by_keyword(cursor_read, cursor_write, conn_write, query_data["query"],
                                        query_data["params"](keyword), keyword)


    elif choice == "4":
        # films = search_by_genre(cursor_read, conn_read, cursor_write, conn_write, ask_year=False)
        films = search_by_genre(cursor_read, cursor_write, conn_write, ask_year=False)

    elif choice == "5":
        # films = search_by_genre(cursor_read, conn_read, cursor_write, conn_write, ask_year=True)
        films = search_by_genre(cursor_read, cursor_write, conn_write, ask_year=True)


    elif choice == "6":
        print("🔍 Загружаем популярные запросы...")

        # 🔄 Проверяем соединение перед запросами
        if not conn_read.is_connected():
            print("🔄 Восстанавливаем соединение с MySQL...")
            conn_read = get_read_connection()
            cursor_read = conn_read.cursor()


        top_genres = execute_query(cursor_write, queries.GET_TOP_GENRES)
        top_keywords = execute_query(cursor_write, queries.GET_TOP_KEYWORDS)


        # 🔥 Проверяем количество записей в popular_search
        cursor_write.execute("SELECT COUNT(*) FROM Popular_Searches")
        count = cursor_write.fetchone()

        # ✅ Проверка на пустые данные
        if not top_genres or not isinstance(top_genres, list):
            print("❗ Ошибка: Данные о популярных жанрах отсутствуют или неверны!")
        else:
            print("\n🔥 Топ-5 популярных жанров:")
            for genre, count in top_genres:
                print(f"🎬 {genre}: {count} запросов")

        if not top_keywords or not isinstance(top_keywords, list):
            print("❗ Ошибка: Данные о популярных ключевых словах отсутствуют или неверны!")
        else:
            print("\n🔍 Топ-5 популярных ключевых слов:")
            for keyword, count in top_keywords:
                print(f"📝 {keyword.upper()}: {count} запросов")

    if films:
        display_films(films, cursor_read)
        select_film_by_id(cursor_read, films)  # ✅ Теперь передаётся films

# Закрытие соединений
cursor_read.close()
conn_read.close()
cursor_write.close()
conn_write.close()
