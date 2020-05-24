from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, asc
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db')
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


today = datetime.today().date()
Base.metadata.create_all(engine)


class Todo:
    def __init__(self):
        self.today_rows = session.query(Table).filter(Table.deadline == today).all()
        self.rows = session.query(Table).all()
        self.user_option = input(
'''1) Today's Tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
''')

    def option_1(self):
        if self.user_option == '1':
            print(f'\nToday {datetime.today().day} {datetime.today().strftime("%b")}:')
            if len(self.today_rows) > 0:
                for count, item in enumerate(self.today_rows):
                    print(f'{count + 1}. {item}\n')
            else:
                print('Nothing to do!\n')

    def option_2(self):
        if self.user_option == '2':

            # day 1 (Today)
            print(f'\n{today.strftime("%A %d %b")}:')
            if len(self.today_rows) > 0:
                for count, item in enumerate(self.today_rows):
                    print(f'{count + 1}. {item}')
            else:
                print('Nothing to do!')

            def week_task(n):
                d = today + timedelta(n)
                print(f'\n{d.strftime("%A %d %b")}:')
                tasks = []
                for j in self.rows:
                    if j.deadline == d:
                        tasks.append(j)
                if len(tasks) > 0:
                    for c, i in enumerate(tasks):
                        print(f'{c + 1}. {i}\n')
                else:
                    print('Nothing to do!')

            week_task(1)  # day 2
            week_task(2)  # day 3
            week_task(3)  # day 4
            week_task(4)  # day 5
            week_task(5)  # day 6
            week_task(6)  # day 7

    def option_3(self):
        if self.user_option == '3':
            print('\nAll tasks:')
            u = session.query(Table).order_by(asc(Table.deadline)).all()
            if len(u) > 0:
                for count, item in enumerate(u):
                    print(f'{count + 1}. {item}. {item.deadline.strftime("%d %b")}')
                print()
            else:
                print('Nothing to do!\n')

    def option_4(self):
        if self.user_option == '4':
            print('\nMissed activities:')
            u = session.query(Table).order_by(asc(Table.deadline)).all()
            m = []
            for item in u:
                if item.deadline < today:
                    m.append(item)
            if len(m) > 0:
                for c, i in enumerate(m):
                    if len(m) > 0:
                        print(f'{c + 1}. {i}. {i.deadline.strftime("%d %b")}')
                print()
            else:
                print('Nothing missing!\n')

    def option_5(self):
        if self.user_option == '5':
            print('\nEnter activity')
            task = input()
            print('Enter deadline')
            deadline = input()
            x = deadline.split('-')
            date_task = datetime(int(x[0]), int(x[1]), int(x[2])).date()
            new_row = Table(task=task, deadline=date_task)
            session.add(new_row)
            session.commit()
            print('The task has been added!\n')

    def option_6(self):
        if self.user_option == '6':
            print('\nChose the number of the task you want to delete:')
            u = session.query(Table).order_by(asc(Table.deadline)).all()
            if len(u) > 0:
                for count, item in enumerate(u):
                    print(f'{count + 1}. {item}. {item.deadline.strftime("%d %b")}')
                to_delete = input()
                for c, i in enumerate(u):
                    if int(to_delete) == c + 1:
                        session.delete(i)
                        session.commit()
                print('The task has been deleted!\n')
            else:
                print('Nothing to delete!\n')

    def option_0(self):
        if self.user_option == '0':
            print('\nBye!')
            exit()


while True:
    module = Todo()
    module.option_1()
    module.option_2()
    module.option_3()
    module.option_4()
    module.option_5()
    module.option_6()
    module.option_0()
