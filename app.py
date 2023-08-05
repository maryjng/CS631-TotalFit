from sqlalchemy.exc import IntegrityError
from flask import Flask, request, render_template, flash, redirect, url_for
from forms import MemberRegistration, ClassSignup
from models import db, connect_db, Member, ExerciseClass, MemberClass
from custom_exceptions import MemberAlreadyRegisteredError 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:kitty@localhost:5432/totalfit1"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'

app.debug = True

connect_db(app)

#########################################################################

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    form_member = MemberRegistration()
    form_class = ClassSignup()

    classes = [(c.class_id) for c in ExerciseClass.query.all()]
    form_class.class_id.choices = classes

    if request.method == 'POST':
        if form_member.validate_on_submit():
            try:
                new_member = Member.signup(
                member_name = form_member.name.data,
                address = form_member.address.data,
                membership_type = form_member.membership_type.data)

                db.session.commit()

                flash(f"Registration successful. Your member ID is {new_member.member_id}")

                return redirect(url_for("index"))
            
            except IntegrityError:
                flash("There was an issue. Please try again later.", 'danger')

    
        if form_class.validate_on_submit():
            check_member = Member.query.get(form_class.member_id.data)
            if check_member:
                try:
                    res = MemberClass.register_member(form_class.class_id.data, form_class.member_id.data)
                    db.session.commit()

                    flash(f"Successfully registered for Class #{form_class.class_id.data}")
                except MemberAlreadyRegisteredError:
                    flash("You already registered for this class.")
                except:
                    flash("The class is full.")
            else:
                flash(f"Please check your Member ID.")

    return render_template("index.html", form_member=form_member, form_class=form_class)


###############################################################################

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
