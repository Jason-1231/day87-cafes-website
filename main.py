from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, URLField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = 'any secret string'
db = SQLAlchemy(app)
Bootstrap(app)


ROWS_PER_PAGE = 5


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired()])
    img_url = URLField('Image URL', validators=[DataRequired()])
    location = StringField('Cafe Location Area', validators=[DataRequired()])
    seats = StringField('Seatings', validators=[DataRequired()])
    coffee_price = FloatField('coffee_price', validators=[DataRequired()])
    has_toilet = BooleanField('Have Toilets')
    has_wifi = BooleanField('Have Wifi')
    has_sockets = BooleanField('Have Sockets')
    can_take_calls = BooleanField('Can Take Calls')
    submit = SubmitField('Submit')


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    cafes = Cafe.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template("index.html", cafes=cafes, page=page)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form.get('name'),
            map_url=request.form.get('map_url'),
            img_url=request.form.get('img_url'),
            location=request.form.get('location'),
            seats=request.form.get('seats'),
            has_toilet=bool(request.form.get('has_toilet')),
            has_wifi=bool(request.form.get('has_wifi')),
            has_sockets=bool(request.form.get('has_sockets')),
            can_take_calls=bool(request.form.get('can_take_calls')),
            coffee_price=request.form.get('coffee_price'),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('add.html', form=form)


@app.route("/delete", methods=["GET", "DELETE"])
def delete_page():
    all_cafes = Cafe.query.all()
    return render_template('delete.html', cafes=all_cafes)


@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
