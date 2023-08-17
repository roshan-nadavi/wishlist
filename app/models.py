from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDreams(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    dreamJob = db.Column(db.String(120))
    dreamPlace = db.Column(db.String(120))
    dreamExperience = db.Column(db.String(200))
    def __init__(self, username, dreamJob, dreamPlace, dreamExperience):
        self.username = username
        self.dreamJob = dreamJob
        self.dreamPlace = dreamPlace
        self.dreamExperience = dreamExperience
    def __repr__(self):
        return f"<UserDreams(username='{self.username}', dreamJob='{self.dreamJob}', dreamPlace='{self.dreamPlace}', dreamExperience='{self.dreamExperience}')>"