from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:CelesSummo114@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

class BlogPost(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.Text)
	
	def __init__(self, title, body):
		self.title = title
		self.body = body

@app.route('/')
def index:
	return redirect('/blog')

@app.route('/blog', methods=['GET','POST'])
def blog:
	render_template('blog.html',posts=BlogPost.query.all())
	
@app.route('/new_post', methods=['GET','POST'])
def new_post:
	if request.method == 'POST':
		t_error = ""
		b_error = ""
		error = False
		title = request.form['title']
		body = request.form['body']
		
		if len(title) == 0:
			error = True
			t_error="empty"
		if len(body) == 0:
			error = True
			b_error="empty"
			
		if error == False:
			db.session.add(BlogPost(title=title,body=body))
			db.session.commit()
			redirect('/blog')
		else:
			render_template('new_post.html',bodyerror=b_error,titleerror=t_error)
			
	else:
		render_template('new_post.html')