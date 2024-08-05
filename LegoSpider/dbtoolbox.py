import pymysql.cursors
import os

def config2connection():
    connection = pymysql.connect(
        host = os.getenv("DATABASE_HOST"),
        user = os.getenv("DATABASE_USER"),
        password = os.getenv("DATABASE_PASSWORD"),
        database = os.getenv("DATABASE_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection


def db_init():
    connection = config2connection()
    sql = "CREATE TABLE IF NOT EXISTS LegoItems_legoitems(item_number INT UNSIGNED AUTO_INCREMENT, \
        set_number INT UNSIGNED, \
        title VARCHAR(255), \
        price INT UNSIGNED, \
        site VARCHAR(255), \
        url VARCHAR(2047), \
        date_modified DATETIME, \
        PRIMARY KEY(item_number))"
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("execute sql: " + sql)
        connection.commit()
    return


def db_select(config, attr, value, operator):
    connection = config2connection()
    table = config["table"]
    sql = "SELECT * FROM {} WHERE {}{}{}".format(table, attr, operator, value)
            
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("execute sql: " + sql)
            return cursor.fetchone()


def db_insert(config, record):
    connection = config2connection()
    table = config["table"]
    attrs = record.keys()
    values = [ record[attr] for attr in attrs ]
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table, ",".join(attrs), ",".join(values))

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("execute sql: " + sql)
        connection.commit()
    return


def db_update(config, record, attr, value, operator):
    connection = config2connection()
    table = config["table"]
    attrs = record.keys()
    attr_value_pairs = [ attr + "=" + record[attr] for attr in attrs]
    sql = "UPDATE {} SET {} WHERE {}{}{}".format(table, ",".join(attr_value_pairs), attr, operator, value)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("execute sql: " + sql)
        connection.commit()
    return


def db_delete(config, attr, value, operator):
    connection = config2connection()
    table = config["table"]
    sql = "DELETE FROM {} WHERE {}{}{}".format(table, attr, operator, value)
            
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("execute sql: " + sql)
        connection.commit()
    return
