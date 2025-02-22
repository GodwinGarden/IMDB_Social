from flask_app import app
from flask import render_template,redirect,session,request, flash, url_for
from flask_app.models import user
from flask_app.models import movie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/index')
@app.route('/')
def index():
	# clear out the session cache to avoid member data issues on-load
	session.clear()
	return render_template('index.html')
	
@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/login')
def load_login_and_reg():
	return render_template('login_reg.html')
	
@app.route('/login/member', methods=['POST'])
def user_login():
	member = user.User.get_by_email(request.form)
	
	if not member:
		flash("Invalid Email","login")
		return redirect('/login')
	
	if not bcrypt.check_password_hash(member.password, request.form['password']):
		flash("Invalid Password","login")
		return redirect('/login')
	
	session['member_id'] = member.id
	session['user_email'] = member.email
	session['logged_in'] = True
	# flash(f"Welcome, ", "logged_in")
	return redirect('/dashboard')

@app.route('/new/member', methods=['POST'])
def register_user():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'screenname' : request.form['screenname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
        }
    user.User.create(data)
    return redirect('/')

@app.route('/update/member', methods=['POST'])
def update_user():
	if 'user_id' not in session:
    	return redirect('/logout')
    if User.edit_user(request.form):
        return redirect(f"/update/member/{request.form['id']}")
    # if not user.User.validate_registration(request.form):
    #     return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'screenname' : request.form['screenname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
        }
    user.User.create(data)
    return redirect('/')


@app.route('/dashboard')
def load_dashboard():
    if 'logged_in' not in session:
        return redirect('/')
    member = user.User.get_by_id({'id' : session['member_id']})
    movies = movie.Movie.get_all()
    return render_template('dashboard.html', member=member, movies=movies)

