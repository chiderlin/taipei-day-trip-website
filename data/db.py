import mysql.connector
import json


class DB_controller:
    '''connect to your mysql'''

    def __init__(self, host, user, password, db=None):
        self.db = db
        try:
            self.mydb = mysql.connector.connect(  # 一開始mydb沒有self，連不到資料庫
                host=host,
                user=user,
                password=password,
                database=self.db
            )
            self.mycursor = self.mydb.cursor()
        except Exception as e:
            print(e)

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

    def insert_data(self, name, category, description, address, transport, mrt, latitude, longitude, images):
        '''add new data'''
        try:
            self.mycursor.execute(
                f'insert into attractions (name, category, description, address, transport, mrt, latitude, longitude, images) values ("{name}", "{category}", "{description}", "{address}", "{transport}", "{mrt}", {latitude}, {longitude}, "{images}")')
            self.mydb.commit()
            return (self.mycursor.rowcount, "record inserted.")
        except Exception as e:
            return e

    def show_data(self, table_name, column_name, value):
        '''show all data base on specific db&table'''
        try:
            self.mycursor.execute(f"use {self.db}")
            self.mycursor.execute(
                f"select * from {table_name} where {column_name}='{value}'")
            result = self.mycursor.fetchone()
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
            result = str(result).replace("(","").replace(",)","")
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

    def delete(self):
        pass


if __name__ == '__main__':
    with open("config.json", "r", encoding="utf-8") as f:
        conf = json.load(f)

    db = DB_controller(
        host=conf["HOST"],
        user=conf["USER"],
        password=conf["PWD"],
        db=conf["DB"])
    # print(db.read_db())
    # print(db.create_db("taipeitravel"))

    # print(db.create_table(
    #     '''
    #     create table attractions (id int auto_increment primary key,
    #     name varchar(50) unique not null, 
    #     category varchar(10),
    #     description varchar(2000),
    #     address varchar(255),
    #     transport varchar(5000),
    #     mrt varchar(20),
    #     latitude DECIMAL(9,6),
    #     longitude DECIMAL(9,6),
    #     images varchar(5000))
    #     CHARSET=utf8mb4'''))

    # print(db.read_table())
    # print(db.count_data("attractions"))
    # print(db.show_data("attractions","id",1))
    result = db.relative_data("attractions", "name", "藝術")
    for ans in result:
        print(ans)
        