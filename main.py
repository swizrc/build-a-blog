from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:CelesSummo114@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class BlogPost(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.Text)
	owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	
	def __init__(self, title, body, owner):
		self.title = title
		self.body = body
		self.owner = owner
		
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(30))
	password = db.Column(db.String(15))
	blogs = db.relationship('BlogPost', backref='owner')
	
	def __init__(self,name,password):
		self.name = name
		self.password = password

@app.before_request
def require_login():
	allowed_routes = ['register','login','blog','logout','index']
	if 'user' not in session and request.endpoint not in allowed_routes:
		return redirect('/login')
		
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		usererror = ""
		pwderror = ""
		Error = False
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(name=username).first()
		if not user:
			usererror = "nonexist"
			Error = True
		if user and user.password != password:
			pwderror = "mismatch"
			Error = True
		if user and user.password == password and Error == False:
			session['user'] = username
			return redirect('/')
		else:
			return render_template('login.html',usererror=usererror,pwderror=pwderror,name=username)
	else:
		return render_template('login.html')
		
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		usererror = ""
		pwderror = ""
		vpwderror = ""
		Error = False
		username = request.form['username']
		password = request.form['password']
		verify = request.form['verify']
		if User.query.filter_by(name=username).first():
			usererror = "existing"
			Error = True
		if password != verify:
			pwderror = "mismatch"
			vpwderror = "mismatch"
			Error = True
		if len(username) < 3:
			usererror = "short"
			Error = True
		if len(password) < 3:
			pwderror = "short"
			Error = True
		if len(username) == 0:
			usererror = "empty"
			Error = True
		if len(password) == 0:
			pwderror = "empty"
			Error = True
		if len(verify) == 0:
			vpwderror = "empty"
			Error = True
		if Error == False:
			user = User(username,password)
			db.session.add(user)
			db.session.commit()
			session['user'] = username
			return redirect('/new_post')
		else:
			return render_template('register.html',usererror=usererror,pwderror=pwderror,vpwderror=vpwderror,name=username)
	else:
		return render_template('register.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
	del session['user']
	return redirect('/blog')

@app.route('/')
def index():
	users = User.query.order_by(User.name).all()
	return render_template('index.html',users=users)

@app.route('/blog', methods=['GET','POST'])
def blog():
	if request.args.get('id'):
		id = request.args.get('id')
		return render_template('blog.html',post=BlogPost.query.get(id),blogid=id)
	elif request.args.get('user'):
		user_id = request.args.get('user')
		user = User.query.get(user_id)
		posts = BlogPost.query.filter_by(owner=user).all()
		return render_template('blog.html',posts=posts,user=user)
	else:
		return render_template('blog.html',posts=BlogPost.query.all())
		
@app.route('/new_post', methods=['GET','POST'])
def new_post():
	if request.method == 'POST':
		t_error = ""
		b_error = ""
		error = False
		title = request.form['title']
		body = request.form['body']
		owner = User.query.filter_by(name=session['user']).first()
		
		if len(title) == 0:
			error = True
			t_error="empty"
		if len(body) == 0:
			error = True
			b_error="empty"
			
		if error == False:
			blogpost = BlogPost(title,body,owner)
			db.session.add(blogpost)
			db.session.commit()
			post = BlogPost.query.filter_by(title=title,body=body).first()
			return redirect('./blog?id=' + str(post.id))
		else:
			return render_template('new_post.html',bodyerror=b_error,titleerror=t_error)
			
	else:
		return render_template('new_post.html')

if __name__ == "__main__":
	app.run()