import datetime
import json
import ast
import mysql.connector as sql
from flask import *
import os
canteen=Blueprint('canteen',__name__)
name=None
wallet_bal=0
username=None
APP_ROOT = '/Users/sameershaik/PycharmProjects/NBKR_CONNECT'
UPLOAD_FOLD = '/static/canteen/images'
UPLOAD_FOLDER=APP_ROOT+UPLOAD_FOLD
@canteen.route('/')
def home():
    global name,wallet_bal,username
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    username=session['name']
    cur.execute(f"SELECT ROLLNO,NAME,wallet FROM STUDENT_INFO WHERE ROLLNO='{username}'")
    data =cur.fetchone()
    con.close()
    username=data[0]
    name=data[1]
    wallet_bal=data[2]
    return redirect(url_for('canteen.menu'))
@canteen.route('/menu/')
def menu():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    if not(name or wallet_bal):
        return redirect('/')
    return render_template('canteen/menu.html',name=name,wallet_bal=wallet_bal,user=True)
@canteen.route('/breakfast')
def breakfast():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
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

    return render_template('canteen/breakfast.html',items=breakfast_items,name=name,wallet_bal=wallet_bal,user=True)
@canteen.route('/dinner')
def dinner():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
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
    return render_template('canteen/dinner.html',items=dinner_items,name=name,wallet_bal=wallet_bal,user=True)
@canteen.route('/lunch')
def lunch():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
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
    return render_template('canteen/lunch.html',items=lunch_items,name=name,wallet_bal=wallet_bal,user=True)
@canteen.route('/special')
def special():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
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
    return render_template('canteen/todayspl.html',items=spl_items,name=name,wallet_bal=wallet_bal,user=True)
@canteen.route('/cart')
def cart():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
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
        con.close()
        return render_template('canteen/cart.html',items=cart.cart_items,tot_quan=cart.tot_quan,tot_price=cart.tot_price,name=name,wallet_bal=wallet_bal,user=True)
@canteen.route('/checkout/')
def checkout():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    return render_template('canteen/checkout.html',items=cart.cart_items,tot_price=cart.tot_price,tot_quan=cart.tot_quan,name=name,wallet_bal=wallet_bal,user=True)


@canteen.route('/payments/<item_list>/<tot_price>')
def payments(item_list,tot_price):
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    item_list=ast.literal_eval(item_list)
    items={}
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
    cur = con.cursor(buffered=True)
    for k in item_list:
        for i,j in k.items():
            items[i[1]]=j
    if wallet_bal>=int(tot_price):
        cur.execute('INSERT ITEM_ORDERS (ITEM_ID,USERNAME,TOT_PRICE) VALUES("%s","%s","%s");' %(str(items),str(username),int(tot_price)))
        cur.execute('UPDATE STUDENT_INFO SET wallet="%s" WHERE ROLLNO="%s";' %(wallet_bal-int(tot_price),str(username)))
        cur.execute('SELECT ORDER_ID FROM ITEM_ORDERS WHERE USERNAME="%s" ORDER BY CREATED_AT  DESC;' %(str(username)))
        order_id=cur.fetchone()
        cur.execute(
            'INSERT INTO STATUS(ROLLNO, AMOUNT, CATEGORY, UTR_NO,TOKEN_NO,STATUS,ADMIN_TYPE)  VALUES ("%s","%s","%s","%s","%s","%s","%s");' % (
            str(username), tot_price, 'Canteen', list(order_id)[0],list(order_id)[0],1,1))
        con.commit()
        con.close()
        flash(f'Order placed successfully TOKEN NO: {list(order_id)[0]}\ncheck in Status Tab',category='message')
        return redirect(url_for('canteen.home'))
    flash('Insufficient Balance Please Add money to Wallet',category='warning')
    return redirect(url_for('canteen.home'))



@canteen.route('/dashboard/')
def dashboard():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    tot_orders_list=[]
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
    cur = con.cursor(buffered=True)
    cur.execute('SELECT COUNT(*) FROM ITEM_ORDERS')
    tot_orders=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM ITEM_ORDERS WHERE STATUS=1')
    suc_orders = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM ITEM_ORDERS WHERE STATUS=0')
    pen_orders = cur.fetchone()[0]
    cur.execute('SELECT * FROM ITEM_ORDERS WHERE STATUS=0')
    orders=cur.fetchall()
    for i in orders:
        order=[]
        for j in i:
            try:
                j=ast.literal_eval(str(j))
                order.append(j)
            except:
                order.append(j)
        tot_quan=sum(order[1].values())
        order.append(tot_quan)
        tot_orders_list.append(order)
    return render_template('canteen/dashboard.html',tot_orders=tot_orders,pen_orders=pen_orders,suc_orders=suc_orders,tot_orders_list=tot_orders_list,user=False)
@canteen.route('/View_Dishes/')
def view_product():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
    cur = con.cursor(buffered=True)
    cur.execute('SELECT * FROM ITEMS;')
    tot_products = cur.fetchall()
    return render_template('canteen/view_product.html',tot_products=tot_products,user=False)
@canteen.route('/update_product/<product_id>')
def update_product(product_id):
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
    cur = con.cursor(buffered=True)
    cur.execute(f'SELECT * FROM ITEMS WHERE ID={product_id};')
    product = cur.fetchone()
    return render_template('canteen/update_product.html',product=product,user=False)
@canteen.route('/delete_product/<product_id>/<product_name>')
def delete_product(product_id,product_name):
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    return render_template('canteen/delete_product.html',product_id=product_id,product_name=product_name,user=False)
@canteen.route('/deleting/',methods=['GET','POST'])
def deleting():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    if request.method=='POST':
        id=request.form['id']
        con = sql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="MINI_PROJECT"
        )
        cur = con.cursor(buffered=True)
        cur.execute('UPDATE ITEMS SET ITEMS_STATUS=0 WHERE ID="%s"'%(id,))
        con.commit()
        con.close()
        return redirect(url_for('canteen.view_product'))

@canteen.route('/updating/',methods=['GET','POST'])
def updating():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    if request.method=='POST':
        filename=None
        id=request.form['id']
        name=request.form["name"]
        price=request.form['price']
        category=request.form['category']
        if request.files['image']:
            file=request.files['image']
            filename=file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        con = sql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="MINI_PROJECT"

        )
        cur = con.cursor()
        if filename:
            cur.execute('UPDATE ITEMS SET ITEM_NAME="%s",ITEM_COST="%s",ITEM_CATEGORY="%s",ITEM_IMG_LINK="%s" WHERE ID="%s"'%(name,price,category,filename,id))
        else:
            cur.execute(
                'UPDATE ITEMS SET ITEM_NAME="%s",ITEM_COST="%s",ITEM_CATEGORY="%s" WHERE ID="%s"' % (name, price, category, id))
        con.commit()
        con.close()
        return redirect(url_for('canteen.view_product'))
@canteen.route('/add_product/')
def add_product():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    return render_template('canteen/add_product.html',user=False)
@canteen.route('/add',methods=['GET','POST'])
def add():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    if request.method=="POST":
        name = request.form["name"]
        name=name.upper()
        price = request.form['price']
        category = request.form['category']
        file = request.files['image']
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        con = sql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="MINI_PROJECT"

        )
        cur = con.cursor()
        cur.execute('INSERT INTO ITEMS(ITEM_NAME,ITEM_IMG_LINK,ITEM_COST,ITEM_CATEGORY) VALUES ("%s","%s","%s","%s")'%(name,filename,price,category))
        con.commit()
        con.close()
        return redirect(url_for('canteen.view_product'))
    else:
        id=request.args.get('id')
        con = sql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="MINI_PROJECT"
        )
        cur = con.cursor(buffered=True)
        cur.execute('UPDATE ITEMS SET ITEMS_STATUS=1 WHERE ID="%s"' % (id,))
        con.commit()
        con.close()
        return redirect(url_for('canteen.view_product'))

@canteen.route('/place_order/<id>')
def place_order(id):
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
    cur = con.cursor(buffered=True)
    cur.execute('UPDATE ITEM_ORDERS SET STATUS=1 WHERE ORDER_ID="%s"' % (id,))
    cur.execute('UPDATE STATUS SET Order_STATUS=1 WHERE TOKEN_NO="%s"'%(id,))
    con.commit()
    con.close()
    return redirect(url_for('canteen.dashboard'))
#@canteen.route('/update_item/',methods=["POST","GET"])
'''def update_item():
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

        return JsonResponse('Item was added', safe=False)'''
