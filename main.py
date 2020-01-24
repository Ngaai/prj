import requests
import pygal, sys,json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config.config import Development, Production
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Production)
db = SQLAlchemy(app)
from models.inventories import Inventories
from models.sales import Sales


@app.before_first_request
def create_tables():
    db.create_all()

rows = db.engine.execute("""
    select (sum(i.buying_price*s.quantity)) as subtotal, extract(Month from s.created_at) from public.inventories i join 
    public.sales s on i.id=s.inv_id where Extract(year from s.created_at)='2019' group by extract (month from s.created_at) order by extract (month from s.created_at)
    """)
months = []
total_sales = []

for each in rows:
    months.append(each[1])
    total_sales.append(each[0])

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/delete/<int:id>')
def delete_item(id):
    record = Inventories.fetch_a_record(id)
    try:
        record.delete_record()
    except:
        return 'Could not delete item, confirm there are no sales'
    return redirect(url_for('add_inventories'))


#@app.route('/view_sales/<int:id1>')
#def view_sales(id1):
#   record = Inventories.fetch_a_record(id1)
#   return render_template('about.html', record=record)
@app.route('/salepro/<int:id>', methods=['POST', 'GET'])
def makeSales(id):
    record = Inventories.fetch_one_record(id)
    if record:
        if request.method == 'POST':

            quantity = request.form['quantity']
            newStock = record.stock - int(quantity)
            record.stock = newStock
            db.session.commit()
            flash('You successfully made a sale', 'success')

    return redirect(url_for('add_inventories'))


@app.route('/make_sale/<int:id1>', methods=['POST', 'GET'])
def make_sale(id1):
    print(id1)
    record = Inventories.fetch_a_record(id1)
    if record:
        if request.method == 'POST':
            quantity = request.form['quantity']
            inv_id =request.form['inv_id']

            if int(quantity) < record.stock:
                new_stock = record.stock - int(quantity)
                record.stock = new_stock
                sale = Sales(inv_id=inv_id, quantity=quantity, created_at=now())
                sale.sell()
                db.session.commit()
                flash('Successful Sale')
            else:
                flash('stock not available')

    return redirect(url_for('add_inventories'))


@app.route('/update_sale/<int:id>', methods=['POST', 'GET'])
def update_sale(id):
    record=Inventories.fetch_a_record(id)

    if request.method=='POST':
        record.name = request.form['name']
        record.type = request.form['type']
        record.buying_price = request.form['buying_price']
        record.selling_price = request.form['selling_price']
        record.stock = request.form['stock']
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('update_sale.html',record=record)


@app.route('/add_inventory', methods=['POST', 'GET'])
def add_inventories():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']
        stock = request.form['stock']
        record = Inventories( name=name, buying_price=buying_price, selling_price=selling_price, type=type, stock=stock)
        record.add_records()

    return redirect(url_for('index'))


@app.route('/add_inventories')
def index():
    records = Inventories.query.all()
    return render_template('add_inventories.html', records=records)


@app.route('/predictor',methods=['POST','GET'])
def predictor():
    if request.method == 'GET':
        select_year = '2019'
    else:
         select_year = request.form['selected_year']
    rows = db.engine.execute("""
        select (sum(i.buying_price*s.quantity)) as subtotal, 
        extract(Month from s.created_at)
         from public.inventories i join 
        public.sales s on i.id=s.inv_id where 
        Extract(year from s.created_at)=""" + select_year + """
         group by extract (month from s.created_at) 
         order by extract (month from s.created_at)""")
    months = []
    total_sales = []

    for each in rows:
        months.append(each[1])
        total_sales.append(each[0])
    graph = pygal.Line()
    graph.title = 'Sales over time in year '+ select_year
    graph.x_labels = months
    graph.add('Total Sales', total_sales)
    graph_data = graph.render_data_uri()
    return render_template('predictor.html', graph_data=graph_data)


@app.route('/')
def hello_world():
    records = db.engine.execute("""
    select to_char( s.created_at,'Month'),sum(s.quantity*(i.selling_price)) from sales s join inventories i on s.inv_id=i.id where Extract(year from s.created_at)='2019'
     group by to_char( s.created_at,'Month')
    """)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Sales Month wise'
    for each in records:
        pie_chart.add(each[0], each[1])

    graph = pygal.Line()
    graph.title = 'Sales over time'
    graph.x_labels = months
    graph.add('Total Sales', total_sales)
    graph_data = graph.render_data_uri()
    pie_data = pie_chart.render_data_uri()
    return render_template('index.html', graph_data=graph_data, pie_data=pie_data)

# Todo functions


@app.route('/feedback', methods=['GET'])
def todo_all():
    resp={}
    try:
        resp = requests.get('https://todomainclient.herokuapp.com/todos')
    except ValueError:
        return {"Message": "Error"}
    print(resp.json()['todos'])
    return render_template('todo.html', resp=resp.json()['todos'])


@app.route('/review/<int:id>', methods=['GET'])
def todo(id):
    todo={}
    try:
       todo = requests.get('https://todomainclient.herokuapp.com/todos/'+ str(id)).json()
    except ValueError:
        return {'Message': 'Error occurred'}
    return todo


@app.route('/edit_review/<int:id>', methods=['POST', 'GET'])
def edit_todo(id):
    todo = requests.get('https://todomainclient.herokuapp.com/todos/' + str(id)).json()
    if request.method == 'POST':
        todo['title'] = request.form['title']
        todo['description'] = request.form['comment']+":"+request.form['name']+":"+request.form['email']
    resp = requests.put('https://todomainclient.herokuapp.com/todos/' + str(id), json=todo)
    print(resp)
    return redirect(url_for('todo_all'))


@app.route('/delete_todo/<int:id>', methods=['POST', 'GET'])
def delete_todo(id):
    resp = requests.delete('https://todomainclient.herokuapp.com/todos/' + str(id))
    if resp != 200:
        pass
    return redirect(url_for('todo_all'))


@app.route('/add_todo', methods=['POST'])
def add_todo():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['comment']+":"+request.form['name']+":"+request.form['email']
    task = {"title": title, "description": description}
    try:
        requests.post("https://todomainclient.herokuapp.com/todos", json=task)

    except ValueError:
        return {'Message': 'Error occurred could not post the item'}
    return redirect(url_for('/todo_all'))


if __name__ == '__main__':
    app.run()
