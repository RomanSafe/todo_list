from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
# from os import path
import sqlite3


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


# def create_db_and_table():
    # directory_path = path.dirname(path.abspath(__file__))
    # if not path.isfile("\\".join((directory_path, "todo.db"))):
    #     engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    #     Base.metadata.create_all(engine)

today = datetime.today()

class ToDo(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Just relax.')
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def show_menu():
    while True:
        user_command = input("\n1) Today's tasks\n"
                             "2) Week's tasks\n"
                             "3) All tasks\n"
                             "4) Missed tasks\n"
                             "5) Add task\n"
                             "6) Delete task\n"
                             "0) Exit\n")
        if user_command == "1":
            show_today_tasks()
        elif user_command == "2":
            show_weeks_tasks()
        elif user_command == "3":
            show_tasks("all")
        elif user_command == "4":
            show_tasks("missed")
        elif user_command == "5":
            add_task()
        elif user_command == "6":
            delete_task()
        elif user_command == "0":
            exit_from_programme()
            break
        else:
            print("Wrong number. Please, enter number from 0 to 4.")

def get_day_shedule(date_):
    todo_list = session.query(ToDo).filter(ToDo.deadline == date_).all()
    if not todo_list:
        print("Nothing to do!\n")
    else:
        for item in range(len(todo_list)):
            print(f"{item + 1}. {todo_list[item].task}\n")


def show_today_tasks():
    print(f"\nToday {today.strftime('%#d %b')}:")
    get_day_shedule(today.date())


def show_weeks_tasks():
    for delta in range(7):
        current_day = today + timedelta(days=delta)
        print(current_day.strftime('%A %#d %b:'))
        get_day_shedule(current_day.date())


def show_tasks(tasks_type):
    message = {"all": "All tasks:", "missed": "Missed tasks:",
               "delete": "Chose the number of the task you want to delete:"}
    print(message[tasks_type])
    if tasks_type == "all" or tasks_type == "delete":
        all_tasks = session.query(ToDo).order_by(ToDo.deadline).all()
    elif tasks_type == "missed":
        all_tasks = session.query(ToDo).filter(ToDo.deadline < today.date()).order_by(ToDo.deadline).all()
        if len(all_tasks) == 0:
            print("Nothing is missed!\n")
            return None
    if tasks_type == "delete" and len(all_tasks) == 0:
        print("Nothing to delete\n")
        return None
    for item in range(len(all_tasks)):
        print(f"{item + 1}. {all_tasks[item].task}. {all_tasks[item].deadline.strftime('%#d %b')}")
    if tasks_type == "delete":
        return all_tasks

def add_task():
    new_row = ToDo(task=input("\nEnter task\n"),
                   deadline=datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    tasks_list = show_tasks("delete")
    if tasks_list:
        what_delete = int(input()) - 1
        session.delete(tasks_list[what_delete])
        session.commit()
        print("The task has been deleted!")


def exit_from_programme():
    session.close()
    print("\nBye!")


def table_name_test():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    tables_in_db = c.execute('SELECT name FROM sqlite_master '
                                'WHERE type =\'table\' AND name '
                                'NOT LIKE \'sqlite_%\';')
    tables_in_db = [table[0] for table in tables_in_db]
    if 'task' not in tables_in_db:
        print("not in table")
    else:
        print(tables_in_db, "in table")
    conn.close()
    return None


if __name__ == '__main__':
    show_menu()
    # table_name_test()
