# Запросы SQL
# Запрос фильмов  содержащих указанное слово в названии
GET_FILMS_BY_TITLE = """
    SELECT film.film_id, film.title, category.name , 
           film.release_year, film.description
    FROM film 
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE film.title LIKE %s
    ORDER BY film.title;
"""
# Запрос фильмов  содержащих указанное слово в названии или описании
GET_FILMS_BY_TITLE_OR_DESCRIPTION = """SELECT film.film_id, film.title, category.name ,
                   film.release_year, film.description
            FROM film 
            JOIN film_category ON film.film_id = film_category.film_id
            JOIN category ON film_category.category_id = category.category_id
            WHERE film.title LIKE %s OR film.description LIKE %s
            ORDER BY film.title
"""
# Запрос фильмов  содержащих указанное слово в  описании
GET_FILMS_BY_DESCRIPTION = """
    SELECT film.film_id, film.title, category.name, 
           film.release_year, film.description
    FROM film 
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE film.description LIKE %s
    ORDER BY film.title;
"""
# Запрос фильмов по жанру
GET_FILMS_BY_GENRE = """
    SELECT film.film_id, film.title, category.name, 
           film.release_year, film.description
    FROM film 
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE category.name = %s
    ORDER BY film.title;
"""
# запись популярных запросов
INSERT_POPULAR_SEARCH = """
    INSERT INTO Popular_Searches (keyword, count) 
    VALUES (%s, 1)
    ON DUPLICATE KEY UPDATE count = count + 1;
"""
# запрос ТОР 5 жанров
GET_TOP_GENRES = """
    SELECT category_data, count 
    FROM Popular_Searches
    WHERE category_data IS NOT NULL
    ORDER BY count DESC
    LIMIT 5;
"""
# запрос ТОР 5 поиска по слову
GET_TOP_KEYWORDS = """
    SELECT keyword, count 
    FROM Popular_Searches
    WHERE keyword IS NOT NULL
    ORDER BY count DESC
    LIMIT 5;
"""



# Запрос списка жанров
GET_CATEGORIES = """
    SELECT category_id, name FROM category;
"""

# Запрос фильмов по жанру
GET_FILMS_BY_GENRE = """
    SELECT film.film_id, film.title, category.name ,
           film.release_year, film.description
    FROM film 
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE category.name = %s
"""

# Запрос фильмов по жанру и году
GET_FILMS_BY_GENRE_AND_YEAR = """
    SELECT film.film_id, film.title, category.name,
           film.release_year, film.description
    FROM film 
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE category.name = %s AND film.release_year = %s
"""

# Запись популярного жанра в базу
INSERT_POPULAR_GENRE = """
    INSERT INTO Popular_Searches (category_data, count) 
    VALUES (%s, 1)
    ON DUPLICATE KEY UPDATE count = count + 1;
"""
# Запрос фильмов по ID
GET_FILM_BY_ID = """
    SELECT film.film_id, film.title, category.name AS genre,
           film.release_year, film.description
    FROM film 
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE film.film_id = %s
"""