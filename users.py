#импорт библиотек
#подключаем библиотеки
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
path=str(os.path.abspath(os.path.dirname(__file__)))
print(path)
os.chdir(path)

#переменная, в которой будет храниться строка подключения к БД:
DB_PATH="sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()
#описание модели данных
class Users(Base):
    #Описывает структуру таблицы users для хранения записей
    __tablename__ = "user"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name=sa.Column(sa.TEXT)
    last_name=sa.Column(sa.TEXT)
    gender=sa.Column(sa.TEXT)
    email=sa.Column(sa.TEXT)
    birthdate=sa.Column(sa.TEXT)
    height=sa.Column(sa.REAL)

#функция для установления соединения с базой данных
def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
	# создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()
	
#функция запроса данных пользователя
def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу Ваши данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введите своё имя: ")
    last_name = input("Введите свою фамилию: ")
    gender = input("Введите свой пол (Male\Female): ")
    email=input("Введите адрес своей электронной почты: ")
    birthdate = input("Введите дату своего рождения в фориате ГОД-МЕСЯЦ-ДЕНЬ: ")
    height=input("Введите свой рост в м: ")
    # создаем нового пользователя
    user = Users(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height)
    # возвращаем созданного пользователя
    return user

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # запрашиваем данные пользоватлея
    user = request_data()
    # добавляем нового пользователя в сессию
    session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")

if __name__ == "__main__":
    main()