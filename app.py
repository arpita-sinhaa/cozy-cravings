from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
menu_items = {
    "Butter Chicken": 850,
    "Paneer Tikka": 550,
    "Masala Dosa": 480,
    "Chole Bhature": 400,
    "Gulab Jamun (2 pcs)": 100,
    "Margherita Pizza": 500,
    "Pasta Alfredo": 450,
    "Bruschetta": 480,
    "Tiramisu": 300,
    "Veg Hakka Noodles": 350,
    "Chicken Manchurian": 700,
    "Spring Rolls": 380,
    "Hot and Sour Soup": 250,
    "Bibimbap": 520,
    "Korean Fried Chicken": 850,
    "Kimchi (on the side)": 250,
    "Tteokbokki": 400,
    "Momos (8 pcs)": 280,
    "Thukpa": 320,
    "Sel Roti": 350,
    "Gundruk Soup": 300
}

app.secret_key = 'supersecretkey' 

#dummy admin credentials for now
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password23'

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid credentials!")

    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    orders = []
    grouped_orders = {}

    with open('data/orders.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 6:
                name, email, item, quantity, cost, total_cost = row
                key = (name, email, total_cost)

                if key not in grouped_orders:
                    grouped_orders[key] = []

                grouped_orders[key].append({
                    'item': item,
                    'quantity': quantity,
                    'cost': cost
                })

    for (name, email, total_cost), items in grouped_orders.items():
        orders.append({
            'name': name,
            'email': email,
            'items': items,
            'total_cost': total_cost
        })

    return render_template('admin_dashboard.html', orders=orders)

         
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        print(f"New message from {name} ({email}): {message}")
        
        return "<h3>Thank you for reaching out! We'll get back to you soon. </h3>"
    
    return render_template('contact.html')

import csv

@app.route('/order', methods=['GET', 'POST'])
def order():
    indian = [("Butter Chicken", 850), ("Paneer Tikka", 550), ("Masala Dosa", 480),
              ("Chole Bhature", 400), ("Gulab Jamun (2 pcs)", 100)]
    
    italian = [("Margherita Pizza", 500), ("Pasta Alfredo", 450),
               ("Bruschetta", 480), ("Tiramisu", 300)]
    
    chinese = [("Veg Hakka Noodles", 350), ("Chicken Manchurian", 700),
               ("Spring Rolls", 380), ("Hot and Sour Soup", 250)]
    
    korean = [("Bibimbap", 520), ("Korean Fried Chicken", 850),
              ("Kimchi (on the side)", 250), ("Tteokbokki", 400)]
    
    nepalese = [("Momos (8 pcs)", 280), ("Thukpa", 320),
                ("Sel Roti", 350), ("Gundruk Soup", 300)]

    menu_items = {item[0]: item[1] for cuisine in [indian, italian, chinese, korean, nepalese] for item in cuisine}

    if request.method == 'POST':
        name = request.form.get('name')  
        email = request.form.get('email')
        items = request.form.getlist('items')

        order_summary = []
        total_cost = 0

        for item in items:
            qty = request.form.get(f"{item}_qty")
            if qty and int(qty) > 0:
                price = menu_items[item]
                cost = price * int(qty)
                total_cost += cost
                order_summary.append({'name': item, 'quantity': qty, 'cost': cost})

        
        with open('data/orders.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for order in order_summary:
                writer.writerow([name, email, order['name'], order['quantity'], order['cost']])
            
            writer.writerow(['', '', '', 'Total Cost', '', total_cost])

        # redirecting to the confirmation page after storing the order
        return render_template('confirmation.html', name=name, order_details=order_summary, total=total_cost)

    return render_template('order.html', indian=indian, italian=italian,
                           chinese=chinese, korean=korean, nepalese=nepalese)


@app.route('/admin')
def admin():
    orders = []
    with open('data/orders.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            orders.append(row)
    return render_template('admin.html', orders=orders)


  
#if __name__ == '__main__':
    #app.run(debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  
