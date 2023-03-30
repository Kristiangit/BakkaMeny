from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from scraper33 import scrapeImg

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kantine.db' ## lage databasen
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kantinepassord'

if __name__ == "__main__":
    app.run(port=3000, debug=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# UPDATE DATABASE: 
# flask db init
# flask db migrate
# flask db upgrade

# CREATE DATABASE:
# python3
# from app import db
# db.create_all()
# exit()


#Flask_Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Bruker.query.get(int(user_id))


class Bruker(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # passord hashing

    @property
    def password(self):
        raise AttributeError("password is not readable")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class HovedRetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<{self.name} {self.id}>"

class SmVare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    drink = db.Column(db.Boolean)
    price = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<{self.name}>"

class DagPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(7), nullable=False)
    dishname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)


class HovedForm(FlaskForm):
    name = StringField("Navn på retten:", [DataRequired()])
    price = StringField("Pris:", [DataRequired()])
    submit = SubmitField("Send inn")

class SmallForm(FlaskForm):
    name = StringField("Navn på varen:", [DataRequired()])
    drink = BooleanField("Er det en drikke?")
    price = StringField("Pris:", [DataRequired()])
    submit = SubmitField("Send inn")

class DagPlanForm(FlaskForm):
    week = IntegerField("Hvilken uke?", [DataRequired(), NumberRange(min=1, max=51)])
    day = RadioField("Hvilken dag?", [DataRequired()], choices=[("Mandag", "Mandag"), ("Tirsdag", "Tirsdag"), ("Onsdag", "Onsdag"), ("Torsdag", "Torsdag"), ("Fredag", "Fredag")])
    dish = SelectField('Hvilken rett?', [DataRequired()], coerce=int)
    submit = SubmitField("Send inn")
    
    # gjør sånn at select-Field har de som står i hovedretter-table som valg
    def __init__(self, *args, **kwargs):
            super(DagPlanForm, self).__init__(*args, **kwargs)
            self.dish.choices = [(interval.id, interval.name) 
                                            for interval in HovedRetter.query.all()]

class DagRettForm(FlaskForm):
    week = IntegerField("Hvilken uke?", [DataRequired(), NumberRange(min=1, max=51)])
    day = RadioField("Hvilken dag?", [DataRequired()], choices=[(0, "Mandag"), (1, "Tirsdag"), (2, "Onsdag"), (3, "Torsdag"), (4, "Fredag")])
    name = StringField("Navn på retten:", [DataRequired()])
    price = StringField("Pris:", [DataRequired()])
    submit = SubmitField("Send inn")



@app.route('/')
def index():
        smretter = SmVare.query.order_by(SmVare.id)
        dager = DagPlan.query.filter_by(week=2)
        return render_template("index.html", smretter=smretter, dager=dager)

@app.route('/logg_inn', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        password = password=request.form['pword']
        alleP = Bruker.query.all()
        for i in alleP:
            if check_password_hash(i.password_hash, password):

                login_user(i)
                print("loged")
                return redirect("/retter")
        
        flash("login fail")
        return render_template("login.html")
    
    elif current_user.is_authenticated:
        return redirect('/retter')
    else:
        return render_template("login.html")

@app.route('/logg_ut', methods=["POST", "GET"])
@login_required
def logout():
    logout_user()

    return redirect("/")


# legge til retter/varer
@app.route('/retter', methods=['POST', 'GET'])
@login_required
def retter():
    hForm = DagRettForm()
    smForm = SmallForm()
    dagForm = DagPlanForm()
    if hForm.validate_on_submit():
        rett_name = hForm.name.data
        price = hForm.price.data
        new_rett = HovedRetter(name=rett_name, price=price)
        new_day = DagPlan(week=hForm.week.data, day=hForm.day.data, dishname=rett_name, price=price)
        try:
            db.session.add(new_rett)
            db.session.add(new_day)
            db.session.commit()
            print("success")
            return redirect('/retter')
        except Exception as e:
            print(new_rett)
            print(e)
            return "There was error"
    if smForm.validate_on_submit():
        new_rett = SmVare(name=smForm.name.data, price=smForm.price.data, drink=smForm.drink.data)
        try:
            db.session.add(new_rett)
            db.session.commit()
            print("success")
            return redirect('/retter')
        except Exception as e:
            print(new_rett)
            print(e)
            return "There was error"
    if dagForm.validate_on_submit():
        dishname = dagForm.dish.data
        dish = HovedRetter.query.get_or_404(dishname)
        new_rett = DagPlan(week=dagForm.week.data, day=dagForm.day.data, dishname=dish.name, price=dish.price)
        try:
            db.session.add(new_rett)
            db.session.commit()
            print("success")
            return redirect('/retter')
        except Exception as e:
            print(new_rett)
            print(e)
            return "There was error"
    else:
        # dager = DagPlan.query.filter_by(week=2)
        smretter = SmVare.query.order_by(SmVare.id)
        dager = DagPlan.query.order_by(DagPlan.week, DagPlan.day)
        return render_template("retter.html", smretter=smretter, dager=dager, hForm=hForm, smForm=smForm, dagForm=dagForm)

@app.route('/api/imgScrape', methods=['POST', 'GET'])
def Scrape(query):
    return scrapeImg(query=query)

@app.route("/endre/h/<int:id>", methods=["POST", "GET"])
@login_required
def hUpdate(id):
    
    form = HovedForm() 
    # print()
    # print(id)
    selectedItem = HovedRetter.query.get_or_404(id)

    # print(selectedItem)
    if form.validate_on_submit():
        selectedItem.name = request.form["name"]
        selectedItem.price = request.form["price"]
        try:
            db.session.commit()
            return redirect('/retter')
        except:
            flash("problem oppsto. Prøv igjen")
            print("rip")
            return render_template('changeitem.html', form=form, selected=selectedItem)

    else:
        return render_template('changeitem.html', form=form, selected=selectedItem)

@app.route("/endre/sm/<int:id>", methods=["POST", "GET"])
@login_required
def smUpdate(id):
    
    form = SmallForm() 
    # print()
    # print(id)
    selectedItem = SmVare.query.get_or_404(id)

    # print(selectedItem)
    if form.validate_on_submit():
        selectedItem.name = form.name.data
        # selectedItem.drink = form.drink.data
        selectedItem.price = form.price.data
        try:
            db.session.commit()
            return redirect('/retter')
        except:
            flash("problem oppsto. Prøv igjen")
            print("rip")
            return render_template('changeitem.html', form=form, selected=selectedItem)

    else:
        return render_template('changeitem.html', form=form, selected=selectedItem)

@app.route("/endre/d/<int:id>", methods=["POST", "GET"])
@login_required
def dUpdate(id):
    
    form = DagPlanForm()
    # print()
    # print(id)
    selectedItem = DagPlan.query.get_or_404(id)

    # print(selectedItem)
    if form.validate_on_submit():
        selectedItem.name = form.name.data
        selectedItem.price = form.price.data
        try:
            db.session.commit()
            return redirect('/retter')
        except:
            flash("problem oppsto. Prøv igjen")
            print("rip")
            return render_template('changeitem.html', form=form, selected=selectedItem)

    else:
        return render_template('changeitem.html', form=form, selected=selectedItem)

@app.route("/slett/h/<int:id>", methods=["POST", "GET"])
@login_required
def hDelete(id):
    
        selectedUser = HovedRetter.query.get_or_404(id)
        try:
            db.session.delete(selectedUser)
            db.session.commit()
            return redirect('/retter')
        except:
            return redirect('/retter')
    
        # retter = Retter.query.all()
        # return render_template("retter.html", retter=retter)

@app.route("/slett/d/<int:id>", methods=["POST", "GET"])
@login_required
def dDelete(id):
    
        selectedUser = DagPlan.query.get_or_404(id)

        try:
            db.session.delete(selectedUser)
            db.session.commit()
            return redirect('/retter')
        except:
            flash("problem oppsto. prøv igjen")
            return redirect('/retter')
    
        # retter = Retter.query.all()
        # return render_template("retter.html", retter=retter)

@app.route("/slett/sm/<int:id>", methods=["POST", "GET"])
@login_required
def smDelete(id):
    
        selectedUser = SmVare.query.get_or_404(id)

        try:
            db.session.delete(selectedUser)
            db.session.commit()
            return redirect('/retter')
        except:
            return redirect('/retter')
    
        # retter = Retter.query.all()
        # return render_template("retter.html", retter=retter)

# legge til nytt passord
@app.route('/passord', methods=['POST', 'GET'])
@login_required
def user():
    if request.method == "POST":
        password = request.form['pword']
        new_user = Bruker(password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            print("success")
            return redirect('/passord')
        except Exception as e:
            print(new_user)
            print(e)
            return "There was error"
    else:
        return render_template("user.html")
    
@app.route('/slett/passord', methods=['POST', 'GET'])
@login_required
def resetUser():
    slett = True
    if request.method == "POST":
        password = password=request.form['pword']
        alleP = Bruker.query.all()
        for i in alleP:
            if check_password_hash(i.password_hash, password):
                try:
                    for i in alleP:
                        print(i)
                        if current_user != i:
                            
                            db.session.delete(i)
                    print(current_user, " lol ", i)
                    # db.session.commit()
                    print("success")
                    return redirect('/passord')
                except Exception as e:
                    print(e)
                    return "There was error"

    else:
        return render_template("user.html", slett=slett)

@app.route('/test')
def testing():
    # retter = Retter.query.order_by(desc(Retter.date_created))
    retter = HovedRetter.query.all(HovedRetter.id)
    db.session.delete(retter)

    return render_template("display.html", retter = retter) 

#export FLASK_ENV=development
#flask run



# lage ny .db :
#python3
#from app import db
#db.create_all()
#exit()
