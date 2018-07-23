"""The following libraries should be installed via pip install: flask, flask_mongoengine, flask_wtf, flask_login.

A free MongoDB database can be set up via mLab. Once it has been obtained insert its details in the following code below.

app.config['MONGODB_SETTINGS'] = {
    'db': '<---YOUR_DB_NAME--->',
    'host': 'mongodb://<---YOUR_DB_FULL URI--->'
}
Provide a unique Secret Form Key to prevent CSRF."""

app.config['SECRET_KEY'] = '<---YOUR_SECRET_FORM_KEY--->'
#Create a unique model for Users depending. In this case, it only includes their email and password:

class User(UserMixin, db.Document):
    meta = {'collection': '<---YOUR_COLLECTION_NAME--->'}
    email = db.StringField(max_length=30)
    password = db.StringField()
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
#A similar model needs to be created for WTForms. It also ensures that the data provided by users satisfy the conditions you created:

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
#Registration
#The registration route can look as follows. Note that it renders a register.html template with the WTForm. When this form is submitted via a POST request to the same /register route, it is firstly validated via WTForm .validate() method. If submitted email hasn’t already been registered, a new entry for the user is created in the database’s collection that stores all of users’ details. Note that the password is hashed using generate_password_hash function from werkzeug.security.

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.email.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)
#Once the entry has been created, login_user function from flask_login logs the user in, who is then redirected to the dashboard route.

"""The webpage is rendered using a simple teplate:

<h1>Registration</h1>
<form action="/register" method="post">
  <p>Email</p>
  {{ form.email }}
  <p>Password</p>
  {{ form.password }}
  {{ form.hidden_tag() }}
  <br>
  <br>
  <input type="submit" value="Submit">
</form>"""
Logging In
#The route for logging in is similar to the registration one. Instead of a new entry being created upon form submission, first the submitted email address is cross checked. If it exists, a hashed version of submitted password is cross checked with the hashed copy of the password using check_password_hash function from werkzeug.security.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)
#If successful, as previously,login_user function from flask_login logs the user in, who is then redirected to the dashboard route.

"""The login webpage is rendered using a simple teplate:

<h1>Login</h1>
<form action="/login" method="post">
  <p>Email</p>
  {{ form.email }}
  <p>Password</p>
  {{ form.password }}
  {{ form.hidden_tag() }}
  <br>
  <br>
  <input type="submit" value="Login">
</form>"""
#Dashboard
#Note that the dashboard is only accessible for logged in users because of @login_required decorator.

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)

"""As a small cross chech, the webpage will render the email of the user currently logged.

<h1>Dashboard</h1>
<p>You are currently logged in as {{ name }}</p>
<a href='logout'>Logout</a>"""
#Logging out
#Logging out is implemented using logout_user function from flask_login. They are then redirected to the login route.

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))