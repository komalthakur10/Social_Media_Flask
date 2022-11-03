from logging import log
import os
import secrets
from turtle import title 
from PIL import Image
from fileinput import filename
from flask import render_template, url_for, flash, redirect, request, abort
from social_media import app, db, bcrypt
from social_media.forms import SignUpForm, LoginForm, UpdateAccountForm, PostForm
from social_media.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Dummy Post data
# Posts = [
#     {
#         'author': 'Komal Thakur',
#         'content': '1st Blog Post Content',
#         'date_posted': 'April 10, 2022'
#     },
    
#     {
#         'author': 'Sneha Kapoor',
#         'content': '2st Blog Post Content',
#         'date_posted': 'April 10, 2022'
#     }
# ]

@app.route('/')  
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('homepage.html', posts=posts, title="Home")

@app.route('/about')
def about():
    return render_template('about.html' ,title="About")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    # Check if form is valid, if it is then tell user that account created successfully using flash alert on homepage
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! You can Log In.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # Check if form is valid, if it is then tell user that account logged in successfully using flash alert on homepage
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page)if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title="Log In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\Profile', picture_fn)
    #app.logger.info("picture_path :: %s",picture_path)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #app.logger.info("if check :: %s",form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            #app.logger.info("user :: %s",current_user)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static', filename='Profile\\' + current_user.image_file)
    image_file = 'static/Profile/' + current_user.image_file
    # app.logger.info("image file %s",image_file)
    return render_template('account.html', title="Profile", image_file=image_file, form=form)


def save_posted_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\Profile', picture_fn)
    #app.logger.info("picture_path :: %s",picture_path)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    post = Post(content=form.content.data, author=current_user, image=form.picture.data)
    if form.validate_on_submit():
        #app.logger.info("if check :: %s",form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image = picture_file
            #app.logger.info("user :: %s",current_user)
        post.content = form.content.data
        post.image = picture_file
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.content.data = post.content
    # image_file = url_for('static', filename='Profile\\' + current_user.image_file)
    image = 'static/Post/' + post.image
    # app.logger.info("image file %s",image_file)
    return render_template('create_post.html', title="New Post", image=image, form=form)

# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(content=form.content.data, author=current_user, image=form.picture.data)
#         app.logger.info("picture %s", form.picture.data)
#         if form.picture.data:
#             image = save_posted_image(form.picture.data)
#             post.image = image
#             image = 'static/Post/' + post.image
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         return redirect(url_for('home'))
#     image=form.picture.data
#     return render_template('create_post.html', title='New Post', image=image, form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.id, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
