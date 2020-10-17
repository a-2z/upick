import json
import json
from flask import Flask, request
from db import db
import dao

# Define db filename
app = Flask(__name__)
db_filename = "upick.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all

# Helper Methods


def success_response(data, code=200):
    """Returns a generic failure response with a specific error message
    as a json."""
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    """Returns a generic failure response with a specific error message
    as a json."""
    return json.dumps({"success": False, "error": message}), code


def ju(jason):
    """Unpacks jsons"""
    return json.loads(jason)


# Routes go here
@app.route('/users/<user>', methods=['GET'])
def get_users(user):
    try:
        return success_response(dao.get_user(user))
    except:
        return failure_response("Please try again.")


@app.route('/pending/<user>', methods=['GET'])
def get_pending(user):
    try:
        return success_response(dao.get_pending(user))
    except:
        return failure_response("User not found.")


@app.route('/groups/<group>', methods=['GET'])
def get_group(group):
    try:
        return success_response(dao.get_group)
    except:
        return failure_response("Group not found")


@app.route('invites/<user>', methods=['GET'])
def check_invites(user):
    try:
        return success_response(dao.get_invites)
    except:
        return failure_response("Group not found")

@app.route('/users/', methods=['POST'])
def new_user():
    """Create a new user account"""
    data = ju(request.data)
    usr = data["usr"]
    pwd = data["pwd"]
    if dao.authenticate(usr, pwd):
        success_response(usr)
    else:
        failure_response(
            "Username has already been taken or invalid password.")

@app.route('/signin/', methods=['POST'])
def login():
    """Sign in"""
    data = ju(request.data)
    usr = data["usr"]
    pwd = data["pwd"]
    if dao.authenticate(usr, pwd):
        success_response("You are logged in.")
    else:
        failure_response("Invalid username or password.")

@app.route('/invites/', methods=['POST'])
def accept_friend():
    data = ju(request.data)
    f1 = data["friend1"]
    f2 = data["friend2"]
    try:
        return success_response(dao.accept_friend(f1, f2))
    except:
        return failure_response("User not found")

@app.route('/create/', methods=['POST'])
def create_group():
    data = ju(request.data)
    host = data["host"]
    date = data["date"]
    try:
        return success_response(dao.create_group(host, date))
    except:
        return failure_response("Please try again")

@app.route('/groups/', methods=['POST'])
def invite_member():
    data = ju(request.data)
    grp = data["group"]
    user = data["user"]
    try:
        return success_response(dao.invite_member())
    except:
        return failure_response("Please try again.")

@app.route('/survey/',methods=['POST'])
def submit_survey():
    data = ju(request.data)
    loc_x = data["location_x"]
    loc_y = data["location_y"]
    price = data["price"]
    dist = data["distance"]
    time = data["time"]
    tags = data["preferences"]
    try:
        return success_response(dao.submit_survey(loc_x,
        loc_y,
        price,
        dist,
        time, 
        tags))
    except:
        return failure_response("Please try again.")

@app.route('/survey/',methods=['POST'])
def place_vote():
    data = ju(request.data)
    user = data["user"]
    restaurants = data["restaurants"]
    try:
        return success_response(dao.place_vote(user,restaurants))
    except:
        return failure_response("Vote failed or group does not exist")

@app.route('/groups/',methods=['DELETE'])
def leave_group():
    data = ju(request.data)
    user = data["user"]
    group = data["group"]
    try:
        return success_response(dao.leave_group(user, group))
    except:
        return failure_response("User not in group.")

@app.route('/users/',methods=['DELETE'])
def delete_user():
    data = ju(request.data)
    user = data["user"]
    pwd = data["pwd"]
    try:
        return success_response(dao.delete_user(user))
    except:
        return failure_response("User not in group.")






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
