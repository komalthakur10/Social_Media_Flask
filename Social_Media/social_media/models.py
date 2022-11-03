from social_media import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database coding (methods are table in db here)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f" User ('{self.username}', '{self.email}', '{self.image_file}') "

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now) #(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S") 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}', '{self.image}')"
