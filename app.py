from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key here
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    item = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)


# Create the Expense table if it doesn't exist
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("home.html")


@app.route('/expense', methods=['GET', 'POST'])
def addexpense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        item = request.form['item']
        cost = float(request.form['cost'])

        new_expense = Expense(
            date=date, category=category, item=item, cost=cost)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully', 'success')

    return render_template("addexpense.html")


@app.route('/delete-expense/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully', 'success')
    return redirect(url_for('manageexpense'))


@app.route('/edit-expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.date = request.form['date']
        expense.category = request.form['category']
        expense.item = request.form['item']
        expense.cost = float(request.form['cost'])

        db.session.commit()
        flash('Expense updated successfully', 'success')
        return redirect(url_for('manageexpense'))

    return render_template('editexpense.html', expense=expense)


# @app.route('/edit-expense/<int:id>', methods=['GET', 'POST'])
# def edit_expense(id):
#     expense = Expense.query.get_or_404(id)

#     if request.method == 'POST':
#         expense.date = request.form['date']
#         expense.category = request.form['category']
#         expense.item = request.form['item']
#         expense.cost = float(request.form['cost'])

#         db.session.commit()
#         flash('Expense updated successfully', 'success')
#         return redirect(url_for('manageexpense'))

#     return render_template('editexpense.html', expense=expense)


@app.route("/manageexpense")
def manageexpense():
    expenses = Expense.query.all()

    return render_template("manageexpense.html", expenses=expenses)


@app.route("/categexpense")
def categexpense():
    expenses = Expense.query.all()
    # Create a dictionary to store total cost by date and category
    total_costs = defaultdict(lambda: defaultdict(float))

    # Calculate total cost for each category on each date
    for expense in expenses:
        total_costs[expense.date][expense.category] += expense.cost

    return render_template("category.html", total_costs=total_costs)
