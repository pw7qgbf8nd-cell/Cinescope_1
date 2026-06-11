import psycopg2
from resorses.db_creds import USER
from resorses.db_creds import USER_PASSWORD
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resorses.db_creds import MoviesDbCreds

def connect_to_postgres():
    """Функция для подключения к PostgreSQL базе данных"""
    connection = None
    cursor = None

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            dbname="db_movies",
            user=USER,
            password=USER_PASSWORD,
            host="80.90.191.123",
            port="31200"
        )

        print("Подключение успешно установлено")

        # Создание курсора
        cursor = connection.cursor()

        # cursor.execute(f"""SELECT * from genres
        # ORDER by id desc limit 100""")

        # Вывод информации о PostgreSQL сервере
        print("Информация о сервере PostgreSQL:")
        print(connection.get_dsn_parameters(), "\n")

        # Выполнение SQL-запроса
        cursor.execute('''
                   DELETE from genres 
                   where name = %s;
               ''', ('жареная баранина',))
        affected_rows = cursor.rowcount
        # new_id = cursor.fetchone()[0]
        print(f"Количество обновленных строк: {affected_rows}")
        connection.commit()
        # Получение результата
        # record = cursor.fetchmany(5)
        # print("Вы подключены к - ", record, "\n")

    except Exception as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
    # Закрытие соединения с базой данных
        if cursor:
                cursor.close()
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")

if __name__ == "__main__":
    connect_to_postgres()


"""# Безопасный способ передачи параметров (предотвращает SQL-инъекции)
user_id = 5
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Несколько параметров
cursor.execute("SELECT * FROM users WHERE department = %s AND salary > %s",
               ("IT", 350000))

# Именованные параметры (используя словарь)
cursor.execute("SELECT * FROM users WHERE department = %(dept)s AND salary > %(min_salary)s",
               {"dept": "IT", "min_salary": 50000})"""

USERNAME = MoviesDbCreds.USERNAME
PASSWORD = MoviesDbCreds.PASSWORD
HOST = MoviesDbCreds.HOST
PORT = MoviesDbCreds.PORT
DATABASE_NAME = MoviesDbCreds.DATABASE_NAME

#  движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

#  создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()