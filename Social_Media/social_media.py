from flask import Flask, render_template
app = Flask(__name__)

# Dummy Post data
Posts = [
    {
        'author': 'Komal Thakur',
        'title': 'Blog Post 1',
        'content': '1st Blog Post Content',
        'date_posted': 'April 10, 2022'
    },
        {
        'author': 'Sneha Kapoor',
        'title': 'Blog Post 2',
        'content': '2st Blog Post Content',
        'date_posted': 'April 10, 2022'
    }
]

@app.route('/')  
@app.route('/home')
def home():
    return render_template('homepage.html', posts=Posts, title="Home")

@app.route('/about')
def about():
    return render_template('about.html' ,title="About")


# To Run App in debug mode(for auto reloading on changes in code) directly using py without set env variables
if __name__=='__main__':
    app.run(debug=True)
