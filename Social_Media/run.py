from social_media import app

# To Run App in debug mode(for auto reloading on changes in code) directly using py without set env variables
# if __name__=='__main__':
app.run(debug=True)
SQLALCHEMY_TRACK_MODIFICATIONS = False