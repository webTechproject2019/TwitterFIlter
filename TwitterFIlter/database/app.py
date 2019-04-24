from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os 
from sqlalchemy import update

# import requests
# import api_utils
# import response_utils

app = Flask(__name__)

# When the Flask app is shutting down, close the database session
@app.teardown_appcondict
def shutdown_session(exception=None):
    Database.b_session.remove()

# database.init_db()
from models import User
from models import tweets

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

ACCESS_TOKEN = '1111425621656252416-ZuJOxl3GkKyb3NXKi3DJub1XSxwLeV'
ACCESS_SECRET = 'sOIyBGr93FGxO4eP1ZAr092bMUqK5QwBaT8r2kwwfmLim'
CONSUMER_KEY = 'Bq8L7AYhWdovkEHrxId8vxVG7'
CONSUMER_SECRET = 'NYDkINrS9l4s93eFWuj0XcxMWHifinmt4l1P4MW4l9VA5nJpaG'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

@app.route('/')
	def base():
		return render_template('index.html')

@app.route('/home')
    def home():
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
if request.form['password'] == 'password' and request.form['username'] == 'admin':
session['logged_in'] = True
else:
flash('wrong password!')
return home()
 
@app.route("/logout")
def logout():
session['logged_in'] = False
return home()

@app.route('/search', methods=['GET'])
    def search_tweets():
        if request.method == 'GET':
            query = request.args.get('query')
            #  start = request.args.get('offset', default=1, type=int) #displays the limit offset
            #  num_records = request.args.get('limit', default=10, type=int)
            print('search query is: '+query)
            data = {
                'hello'  : 'world',
                'number' : 3
            }
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
            results = tweepy.Cursor(api.search, q=query)
            i = 0
            while i < len(results):
                print(results[i].text)
                i = i + 1
             js = json.dumps(results)
             resp = Response(js, status=200, mimetype='application/json')
             return resp

@app.route('/live_tweets', methods=['GET'])
    def live():
        TnT_Trends = api.trends_place(id=23424858)
        jtrends = json.dumps(TnT_Trends, indent=4)
        return jtrends

class RegistrationForm(Form):
    user_id = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    name = TextField('Name', [validators.Length(min=6, max=50)])
    location = TextField('Location', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            user_id  = form.user_id.data
            email = form.email.data
            name = form.name.data
            location = form.location.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(user_id)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('signup.html', form=form)

            else:
                c.execute("INSERT INTO users (user_id, email, name,location, password) VALUES (%s, %s, %s, %s)",
                          (thwart(user_id),thwart(email), thwart(name), thwart(location), thwart(password), thwart("/signup.html/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['user_id'] = user_id

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))

#deletes tweet from api
@app.route('/tweets/<ud>', methods=['DELETE'])
def delete_tweet(id):
    """
    Delete a tweet with the provided tweet ID
    """
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(_url(('tweets', id))[1], headers=headers)
        if response_utils.response_error(response):
            Database.stderr.write('Delete tweet failed.')
            Database.exit(1)
        elif response.status_code == 204:
            Database.stdout.write('Deleted tweet with id: %s \n' % id)
    except requests.exceptions.RequestException as error:
        Database.stderr.write(error)
        Database.exit(1)


#deletes user from database
@app.route('/User/<user_id>', methods=['DELETE'])
def delete_User(user_id):
  p = User.query.get(user_id)
  Database.b_session.delete(p)
  Database.b_session.commit()
  return "deleted"


#code to update name db table
# query = db.update(User).values(name=name)
# query = query.where(User.columns.Id == 1)
# results = connection.execute(query)        

#code to update name from the form 
@app.route("/update", methods=["POST"])
def edit(name):
    User = User.query.filter_by(name=name).one()
    form = EventForm(obj=User)
    if form.validate_on_submit():
        form.populate_obj(User)
        db.session.commit()
        flash("info updated", "success")
    return render_template('editprofile.html', User=User.one(), form=form)

#code to update email db table
# query = db.update(User).values(email=email)
# query = query.where(User.columns.Id == 1)
# results = connection.execute(query)        

#code to update email from the form 
@app.route("/update", methods=["POST"])
def edit(email):
    User = User.query.filter_by(email=email).one()
    form = EventForm(obj=User)
    if form.validate_on_submit():
        form.populate_obj(User)
        db.session.commit()
        flash("info updated", "success")
    return render_template('editprofile.html', User=User.one(), form=form)    

# #code to update password db table
# query = db.update(User).values(password=password)
# query = query.where(User.columns.Id == 1)
# results = connection.execute(query)        

#code to update password from the form 
@app.route("/update", methods=["POST"])
def edit(password):
    User = User.query.filter_by(password=password).one()
    form = EventForm(obj=User)
    if form.validate_on_submit():
        form.populate_obj(User)
        db.session.commit()
        flash("info updated", "success")
    return render_template('editprofile.html', User=User.one(), form=form)    


if __name__ == "__main__":
app.secret_key = os.urandom(12)
app.run(debug=True,host='0.0.0.0', port=4000)
