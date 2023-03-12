from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'shopping_cart'

mysql = MySQL(app)

@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    products = []
    for row in rows:
        product = {}
        product['id'] = row[0]
        product['name'] = row[1]
        product['price'] = row[2]
        product['description'] = row[3]
        products.append(product)
    cur.close()
    return jsonify({'products': products})

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM carts WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
        mysql.connection.commit()
        row = (cur.lastrowid, user_id, datetime.now())
    cur.execute("SELECT * FROM cart_items WHERE cart_id = %s", (row[0],))
    rows = cur.fetchall()
    cart_items = []
    for row in rows:
        cart_item = {}
        cart_item['id'] = row[0]
        cart_item['cart_id'] = row[1]
        cart_item['product_id'] = row[2]
        cart_item['quantity'] = row[3]
        cart_items.append(cart_item)
    cur.close()
    return jsonify({'user_id': user_id, 'cart_id': row[0], 'cart_items': cart_items})

@app.route('/cart/<int:user_id>', methods=['POST'])
def add_to_cart(user_id):
    cart_item = json.loads(request.data)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM carts WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
        mysql.connection.commit()
        row = (cur.lastrowid, user_id, datetime.now())
    cur.execute("SELECT * FROM cart_items WHERE cart_id = %s AND product_id = %s", (row[0], cart_item['product_id']))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)", (row[0], cart_item['product_id'], cart_item['quantity']))
    else:
        cur.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (cart_item['quantity'], row[0]))
    mysql.connection.commit()
    cur.close()
    return jsonify({'user_id': user_id, 'message': 'Item added to cart successfully'})

if __name__ == '__main__':
    app.run(debug=True)
