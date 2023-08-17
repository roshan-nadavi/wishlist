from flask import Flask, render_template, request
import redis

from models import db, UserDreams
app = Flask(__name__)

redisClient = redis.Redis(host="Redis", port = 6379)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/")
def main():
    return render_template("index.html")
@app.route("/enter-information", methods=["POST"])
def enter_information():
    username = request.form['username']
    dreamJob = request.form['dreamJob']
    dreamPlace = request.form['dreamPlace']
    dreamExperience = request.form['dreamExperience']
    print(username, dreamExperience, dreamJob, dreamPlace)
    if redisClient.hgetall(username).keys():
        print("username exists of", redisClient.hgetall(username))
        returnedJob = redisClient.hget(username,"dreamJob").decode('utf-8')
        returnedPlace = redisClient.hget(username,"dreamPlace").decode('utf-8')
        returnedExperience = redisClient.hget(username,"dreamExperience").decode('utf-8')
        return render_template('index.html', exists=True, msg='From Redis', username=username, dreamJob=returnedJob, dreamPlace=returnedPlace, dreamExperience=returnedExperience)
    else:
        retVal = UserDreams.query.filter_by(username=username).first() 
        if retVal:
            redisClient.hset(username, "dreamJob", retVal.dreamJob)
            redisClient.hset(username, "dreamPlace", retVal.dreamPlace)
            redisClient.hset(username, "dreamExperience", retVal.dreamExperience)
            return render_template('index.html', exists=True, msg='From Postgres', username=username, dreamJob=retVal.dreamJob, dreamPlace=retVal.dreamPlace, dreamExperience=retVal.dreamExperience)
        else:
            retVal = UserDreams(username=username, dreamJob=dreamJob, dreamPlace=dreamPlace, dreamExperience=dreamExperience)
            db.session.add(retVal)
            db.session.commit()
            redisClient.hset(username, "dreamJob", dreamJob)
            redisClient.hset(username, "dreamPlace", dreamPlace)
            redisClient.hset(username, "dreamExperience", dreamExperience)

            returnedJob = redisClient.hget(username,"dreamJob").decode('utf-8')
            returnedPlace = redisClient.hget(username,"dreamPlace").decode('utf-8')
            returnedExperience = redisClient.hget(username,"dreamExperience").decode('utf-8')
            return render_template('index.html', created=True, msg='created', username=username, dreamJob=returnedJob, dreamPlace=returnedPlace, dreamExperience=returnedExperience)

@app.route("/usernames", methods=['GET'])
def usernames():
	users = UserDreams.query.all()
	names = [user.username for user in users]
	return render_template('index.html', listing=True, usernames=names)
@app.route("/username", methods=['POST'])
def username():
    username = request.form['username']
    if redisClient.hgetall(username).keys():
        print("username exists of", redisClient.hgetall(username))
        returnedJob = redisClient.hget(username,"dreamJob").decode('utf-8')
        returnedPlace = redisClient.hget(username,"dreamPlace").decode('utf-8')
        returnedExperience = redisClient.hget(username,"dreamExperience").decode('utf-8')
        return render_template('index.html', userRet=True, msg2='From Redis', username=username, dreamJob=returnedJob, dreamPlace=returnedPlace, dreamExperience=returnedExperience)
    else:
        retVal = UserDreams.query.filter_by(username=username).first() 
        if retVal:
            redisClient.hset(username, "dreamJob", retVal.dreamJob)
            redisClient.hset(username, "dreamPlace", retVal.dreamPlace)
            redisClient.hset(username, "dreamExperience", retVal.dreamExperience)
            return render_template('index.html', userRet=True, msg2='From Postgres', username=username, dreamJob=retVal.dreamJob, dreamPlace=retVal.dreamPlace, dreamExperience=retVal.dreamExperience)
        else:
            return render_template('index.html', invisible=True, msg2='User does not exist')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)