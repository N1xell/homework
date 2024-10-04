from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
db = SQLAlchemy(app)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Dish {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        new_dish = Dish(name=name, description=description, price=price)
        db.session.add(new_dish)
        db.session.commit()

        return redirect('/menu')

    return render_template('add_dish.html')

@app.route('/menu')
def menu():
    dishes = Dish.query.all()
    return render_template('menu.html', dishes=dishes)

if __name__ == '__main__':
    app.run(debug=True)