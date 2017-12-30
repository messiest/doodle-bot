from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, IntegerField, FloatField


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/candy'  #

db = SQLAlchemy(app)  # instantiate the database


class Candy(db.Model):  # setting up the database
    __tablename__ = "candies"
    id = db.Column(db.Integer(), primary_key=True)
    competitorname = db.Column(db.String(120), unique=True)
    chocolate = db.Column(db.Integer())
    fruity = db.Column(db.Integer())
    caramel = db.Column(db.Integer())
    peanutyalmondy = db.Column(db.Integer())
    nougat = db.Column(db.Integer())
    crispedricewafer = db.Column(db.Integer())
    hard = db.Column(db.Integer())
    bar = db.Column(db.Integer())
    pluribus = db.Column(db.Integer())
    sugarpercent = db.Column(db.Float())
    pricepercent = db.Column(db.Float())
    winpercent = db.Column(db.Float())

    @classmethod
    def display_json(cls):
        return [{"name": candy.competitorname, "winpercent": candy.winpercent} for candy in Candy.query.all()]


class CandyForm(Form):
    competitorname = StringField('Name')
    chocolate = IntegerField('Chocolate')
    fruity = IntegerField('fruity')
    caramel = IntegerField('caramel')
    peanutyalmondy = IntegerField('peanutyalmondy')
    nougat = IntegerField('nougat')
    crispedricewafer = IntegerField('crispedricewafer')
    hard = IntegerField('hard')
    bar = IntegerField('bar')
    pluribus = IntegerField('pluribus')
    sugarpercent = FloatField('sugar percent')
    pricepercent = FloatField('price percent')
    winpercent = FloatField('win percent')


@app.route('/')  # the index url that for our app
def show_candies():
    """
    render the list of candies in the candy database

    :return:
    :rtype:
    """
    candies = Candy.query.all()
    return render_template('candy_list.html', candies=candies, candy_json=Candy.display_json())


@app.route('/create', methods=['GET', 'POST'])  # get: render the form, post: update the data base
def create_candies():
    """
    add a new candy to the database with from a form

    :return:
    :rtype:
    """
    form = CandyForm(request.form)
    if request.method == 'POST' and form.validate():
        candy = Candy(competitorname=form.competitorname.data,
                      chocolate=form.chocolate.data,
                      fruity=form.fruity.data,
                      caramel=form.caramel.data,
                      peanutyalmondy=form.peanutyalmondy.data,
                      nougat=form.nougat.data,
                      crispedricewafer=form.crispedricewafer.data,
                      hard=form.hard.data,
                      bar=form.bar.data,
                      pluribus=form.pluribus.data,
                      sugarpercent=form.sugarpercent.data,
                      pricepercent=form.pricepercent.data,
                      winpercent=form.winpercent.data)
        db.session.add(candy)  # add the candy to the database
        db.session.commit()  # write it to the database
        return redirect('/')
    else:
        return render_template('candy_form.html', form=form)


if __name__ == "__main__":
    app.debug = True
    app.run()
