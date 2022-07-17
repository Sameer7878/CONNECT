import datetime
import json

import mysql.connector as sql
from flask import *

canteen=Blueprint('canteen',__name__)

@canteen.route('/')
def home():
    return redirect('menu')
@canteen.route('/menu')
def menu():
    return render_template('canteen/menu.html')
@canteen.route('/breakfast')
def breakfast():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEMS WHERE ITEM_CATEGORY='BREAKFAST'")
    breakfast_items=cur.fetchall()
    con.close()

    return render_template('canteen/breakfast.html',items=breakfast_items)
@canteen.route('/dinner')
def dinner():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEMS WHERE ITEM_CATEGORY='DINNER'")
    dinner_items = cur.fetchall()
    con.close()
    return render_template('canteen/dinner.html',items=dinner_items)
@canteen.route('/lunch')
def lunch():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEMS WHERE ITEM_CATEGORY='LUNCH'")
    lunch_items=cur.fetchall()
    con.close()
    return render_template('canteen/lunch.html',items=lunch_items)
@canteen.route('/special')
def special():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEMS WHERE ITEM_CATEGORY='SPECIAL'")
    spl_items = cur.fetchall()
    con.close()
    return render_template('canteen/todayspl.html',items=spl_items)
@canteen.route('/cart')
def cart():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cart.cart_items=[]
    cart.tot_quan=0
    cart.tot_price=0
    if request.cookies['cart']:
        data=request.cookies['cart']
        json_data=json.loads(data)
        for id,quan in json_data.items():
            cart.tot_quan+=quan['quantity']
            cart_dict = {}
            cur.execute(f'SELECT * FROM ITEMS WHERE ID={id}')
            item_data =cur.fetchone()
            cart.tot_price+=item_data[3]*quan['quantity']
            cart_dict[item_data]=quan['quantity']
            cart.cart_items.append(cart_dict)
        return render_template('canteen/cart.html',items=cart.cart_items,tot_quan=cart.tot_quan,tot_price=cart.tot_price)
@canteen.route('/checkout/')
def checkout():
    return render_template('canteen/checkout.html',items=cart.cart_items,tot_price=cart.tot_price,tot_quan=cart.tot_quan)


@canteen.route('/dashboard')
def dashboard():
    return render_template('canteen/dashboard.html')
@canteen.route('/update_item/',methods=["POST","GET"])
def update_item():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    if request.method=="POST":
        data=request.json
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        customer = 'sameer'
        product = cur.execute(f'SELECT ITEM_NAME FROM ITEMS WHERE ID={productId}')
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
        elif action == 'delete':
            orderItem.quantity = 0

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)
