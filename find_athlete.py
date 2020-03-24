#импорт библиотек
#подключаем библиотеки
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
path=str(os.path.abspath(os.path.dirname(__file__)))
print(path)
os.chdir(path)

import datetime
from datetime import datetime

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
class Athelete(Base):
    #Описывает структуру таблицы users для хранения записей
    __tablename__ = "athelete"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)
    id = sa.Column(sa.INTEGER, primary_key=True)
    age= sa.Column(sa.INTEGER)
    birthdate=sa.Column(sa.TEXT)
    gender=sa.Column(sa.TEXT)
    height=sa.Column(sa.REAL)
    name=sa.Column(sa.TEXT)
    weight=sa.Column(sa.INTEGER)
    gold_medals=sa.Column(sa.INTEGER)
    silver_medals=sa.Column(sa.INTEGER)
    bronze_medals=sa.Column(sa.INTEGER)
    total_medals=sa.Column(sa.INTEGER)
    sport=sa.Column(sa.INTEGER)
    country=sa.Column(sa.TEXT)
	
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

def find_user(session):
    """
    Производит поиск пользователя в таблице user по заданному id
    """
    id=input("Введите id: ")
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром id
    find_user = session.query(Users).filter(Users.id == id).first()
    if find_user!=None:      
        return (find_user.birthdate,find_user.height)
    else: return None

def find_twin(session,user_height,user_birthdate):
    #переводим дату из txt в dateframe
    format="%Y-%m-%d"
    user_birthdate_datetime=datetime.strptime(user_birthdate,format)
    #получение всех записей таблицы atheletes
    atheletes=session.query(Athelete).all()
    #поиск близкого по днб рождения
    #словарь дней рождения атлеттов
    dict_birthdate={athelete.id:athelete.birthdate for athelete in atheletes}
    #самый близкий день рождения
    min_birthdate=min(dict_birthdate.items(),key=lambda x: abs(datetime.strptime(x[1],format)-user_birthdate_datetime))
    #поиск близкого по росту
    #словарь роста
    dict_height={athelete.id:athelete.height for athelete in atheletes}
    #фильтрация словаря роста атлетов на отсутвие сведений
    new_dict_height={k:v for k,v in dict_height.items() if v!=None}
    #самый близкий рост
    min_height=min(new_dict_height.items(), key=lambda x: abs(x[1]-user_height))
    return (min_birthdate[0],min_height[0])

def find_athelete(session,id):
    #Производит поиск пользователя в таблице athelete  по заданному id
    # находим запись с параметром id
    find_athelete = session.query(Athelete).filter(Athelete.id == id).first()
    if find_athelete!=None:      
        return (find_athelete.name,find_athelete.birthdate,find_athelete.height)
    else: return None

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    user=find_user(session)
    if user!=None:
        print("День рождения заданного user: ",user[0])
        print("Рост заданного user: ",user[1])
        result=find_twin(session,user[1], user[0])
        twin_birthdate=find_athelete(session,result[0])
        print("Близкий по дате рождения атлет: ",twin_birthdate[0],twin_birthdate[1])
        twin_height=find_athelete(session,result[1])
        print("Близкий по росту атлет: ",twin_height[0],twin_height[2])
    else:
        print ("Пользователь с таким id не найден")
    #print(find_athelete(session,1.735, '1980-03-23'))
        
        
if __name__ == "__main__":
    main()