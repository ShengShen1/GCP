# #db.py

import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                   unix_socket=unix_socket, db=db_name,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
            return conn
    except pymysql.MySQLError as e:
        print(e)

    return None


def get_products():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM products;')
        products = cursor.fetchall()
        if result > 0:
            product_data = jsonify(products)
        else:
            product_data = 'No Products in DB'
    conn.close()
    return product_data


def add_product(product):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO products (product_name, product_description, quantity, seller_name) VALUES(%s, %s, %s, %s)',
                       (product["product_name"], product["product_description"], product["quantity"], product["seller_name"]))
    conn.commit()
    conn.close()

def delete_product_by_id(product_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM products WHERE product_id = %s', (product_id,))
    conn.commit()
    conn.close()

def update_product_quantity(product_name, quantity_change):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE products SET quantity = quantity + %s WHERE product_name = %s', (quantity_change, product_name))
    conn.commit()
    conn.close()