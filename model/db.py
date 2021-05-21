import mysql.connector
from mysql.connector import pooling  # 還在測試中
import json


class DB_controller:
    '''connect to your mysql, using connection pool'''

    def __init__(self, host, user, password, db=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

        dbconfig = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "db": self.db
        }
        try:
            self.mydb = mysql.connector.connect(  # 一開始mydb沒有self，連不到資料庫
                host=host,
                user=user,
                password=password,
                database=self.db,
            )
            self.mycursor = self.mydb.cursor()
        except Exception as e:
            print(str(e))

    def create_db(self, db_name):
        '''method: create database if not exists.'''
        try:
            self.mycursor.execute(f"create database {db_name}")
            return f"created {db_name} successful."
        except Exception as e:
            return e

    # "create table user (id int auto_increment primary key, name varchar(255), account varchar(255), password varchar(30))"
    def create_table(self, sql):
        '''method: base on specific database create table'''
        if self.db is None:
            print("when instance constroller, give a specific database.")
        else:
            try:
                self.mycursor.execute(f"use {self.db}")
                self.mycursor.execute(sql)
                return "created table"
            except Exception as e:
                return e

    def read_db(self):
        '''method: show all the db list'''
        try:
            self.mycursor.execute("show databases")
            self.db_list = []
            for i in self.mycursor:
                raw_db = str(i)
                raw_db = raw_db.replace("('", "").replace("',)", "")
                self.db_list.append(raw_db)
            return self.db_list
        except Exception as e:
            return e

    def read_table(self):
        '''method: base on specific database, show all the table list'''
        try:
            self.mycursor.execute(f"use {self.db}")
            self.mycursor.execute("show tables")
            table_list = []
            for i in self.mycursor:
                table = str(i)
                table = table.replace("('", "").replace("',)", "")
                table_list.append(table)
            return table_list
        except Exception as e:
            return e

    def insert_data(self, table_name, settingrow, settingvalue):
        '''add new data'''
        try:
            self.mycursor.execute(f"use {self.db}")
            self.mycursor.execute(
                f'insert into {table_name} ({settingrow}) values ({settingvalue})')
            self.mydb.commit()
            return (self.mycursor.rowcount, "record inserted.")
        except Exception as e:
            return e

    def show_data(self, table_name, column_name, value):
        '''show one data on specific db&table'''
        try:
            self.mycursor.execute(f"use {self.db}")
            self.mycursor.execute(
                f"select * from {table_name} where {column_name}='{value}'")
            result = self.mycursor.fetchone()
            return result
        except Exception as e:
            return e

    def fetch_all_data(self, table_name, column_name, value):
        '''show all relative data on specific db&table'''
        try:
            self.mycursor.execute(f"use {self.db}")
            self.mycursor.execute(f"select * from {table_name} where {column_name}='{value}'")
            result = self.mycursor.fetchall()
            return result
        except Exception as e:
            return e        

    def update_name(self, origin_name, new_name):
        '''update name to db'''
        try:
            sql = f"update user set name='{new_name}' where name='{origin_name}'"
            self.mycursor.execute(sql)
            self.mydb.commit()
            return "db name update successful"
        except Exception as e:
            return e

    def count_data(self, table_name):
        '''count all the data in specific table.'''
        try:
            self.mycursor.execute(f"use {self.db}")
            sql = f"select count(*) from {table_name}"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            result = str(result).replace("(", "").replace(",)", "")
            return result
        except Exception as e:
            return e

    def relative_data(self, table_name, column_name, value):
        '''search relative data using "like". '''
        try:
            self.mycursor.execute(f"use {self.db}")
            sql = f"select * from {table_name} where {column_name} like '%{value}%'"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            return result

        except Exception as e:
            return e

    def limit_data(self, table_name, start, data_num):
        '''limit page data'''
        try:
            self.mycursor.execute(f"use {self.db}")
            sql = f"select * from {table_name} limit {start},{data_num}"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            return result
        except Exception as e:
            return e

    def delete(self, table_name, cloumn_name, value):
        '''delete data from database'''
        try:
            self.mycursor.execute(f"use {self.db}")
            self.mycursor.execute(f"delete from {table_name} where {cloumn_name} = {value}")
            self.mydb.commit()
            return (self.mycursor.rowcount, "records deleted.")
        except Exception as e:
            return eval


    def close(self):
        ''' close database'''
        try:
            self.mycursor.close()
            self.mydb.close()
            return "close db success"
        except Exception as e:
            return e


if __name__ == '__main__':
    with open("../data/config.json", "r", encoding="utf-8") as f:
        conf = json.load(f)

    db = DB_controller(
        host=conf["HOST"],
        user=conf["USER"],
        password=conf["PWD"],
        db=conf["DB"])
    # print(db.read_db())
    # print(db.create_db("taipeitravel"))

    print(db.create_table(
        '''
        create table orders (
        id int auto_increment,
        order_number varchar(255) not null unique,
        attractionId int not null,
        userId int not null,
        phone varchar(255) not null,
        date date not null,
        time varchar(255) not null,
        price int not null,
        status int not null,
        create_time datetime not null default now(),
        PRIMARY KEY (id),
        FOREIGN KEY (attractionId) REFERENCES attractions(id) ON DELETE CASCADE,
        FOREIGN KEY (userId) REFERENCES user(id) ON DELETE CASCADE
        )
        CHARSET=utf8mb4'''))
    
    # print(db.insert_data(table_name='orders', settingrow='order_number, attractionId, userId, phone, date, time, price, status', settingvalue='"202105211813", "2", "2", "0911111111", "2021-05-13", "afternoon", "2500", "0"'))
    # res = db.fetch_all_data("booking", "userId", "2")
    # print(res[0][2])
    # print(db.read_table())
    # print(db.count_data("user"))
    # print(db.show_data("booking", "bookingId", 2))
    # print(db.delete("booking", "bookingId", 2))
    # res = db.limit_data("attractions",400,12)
    # print(res)
