
from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from dbconnect import connection

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
		
