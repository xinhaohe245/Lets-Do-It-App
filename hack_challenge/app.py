import json
import os
import string, random
import hashlib
from db import db, User, PublicList, Event, Image, User_PublicList_Association
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "letsdoit.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/api/register/", methods=["POST"])
def register():
    body = json.loads(request.data.decode())
    name = body.get('name')
    if name is None:
        return failure_response("no name entered")
    password = body.get('password')
    if password is None:
        return failure_response("no password entered")
    salt = os.urandom(32)
    password = salt + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # uid = ''.join(random.sample(string.digits, 8))
    # possible_user = User.query.filter_by(uid=uid).first()
    # while possible_user is not None:
    #     uid = ''.join(random.sample(string.digits, 8))
    #     possible_user = User.query.filter_by(uid=uid).first()
    # new_user = User(name=name, password=password, uid=uid, public_lists=[], private_lists=[], sharing_lists=[],
    #                 friends=[])
    new_user = User(name=name, password=password)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/login/", methods=['POST'])
def login():
    body = json.loads(request.data.decode())
    name = body.get('name')
    if name is None:
        return failure_response("no name entered")
    password = body.get('password')
    if password is None:
        return failure_response("no password entered")
    user = User.query.filter_by(name=name).first()
    if user is None:
        return failure_response("user not found!")
    salt = user.password[:32]
    check_pw = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if user.password[32:] != check_pw:
        return failure_response("password incorrect!")
    return success_response(user.serialize())

@app.route("/api/<int:id>/friends_lists/")
def get_friends_lists(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    return success_response({"friends": [f.serialize() for f in user.friends]})
    # friends = user.friends
    # return success_response([lst.serialize() for f in friends for lst in f.public_lists if lst.is_public])

@app.route("/api/<int:id>/lists/")
def get_lists(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    return success_response({"lists": [c.serialize() for c in user.public_lists if c.is_public]})

@app.route("/api/<int:id>/lists/<int:list_id>/")
def get_list_by_id(id, list_id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    public_list = user.public_lists.filter_by(public_list_id=list_id).first()
    if public_list is None:
        return failure_response("list not found!")
    return success_response(public_list.serialize())

@app.route("/api/<int:id>/lists/", methods=['POST'])
def create_list(id):
    body = json.loads(request.data.decode())
    list_name = body.get('list_name')
    is_public = body.get('is_public')
    if is_public is None or list_name is None:
        return failure_response("Please provide access information/name of list")
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    new_list = PublicList(list_name=list_name, publisher_id=id)
    db.session.add(new_list)
    association = User_PublicList_Association(user_id=id, is_public=is_public)
    association.public_list = new_list
    user.public_lists.append(association)
    db.session.add(association)
    db.session.commit()
    return success_response(new_list.serialize())

@app.route("/api/<int:id>/lists/<int:list_id>/events/", methods=["POST"])
def create_event(id, list_id):
    public_list = PublicList.query.filter_by(id=list_id).first()
    if public_list is None:
        return failure_response('list not found!')
    
    body = json.loads(request.data.decode())
    company = body.get('company')
    position = body.get('position')
    reminder = body.get('reminder')
    if not company or not position or not reminder:
        return failure_response("missing field(s)!")
    new_event = Event(company=company, position=position, reminder=reminder, public_list_id = list_id)
    public_list.events.append(new_event)
    db.session.add(new_event)
    db.session.commit()
    return success_response(new_event.serialize(), 201)

@app.route("/api/<int:id>/lists/<int:list_id>/events/<int:event_id>/")
def get_event_by_id(id, list_id, event_id):
    user = User.query.filter_by(id=id).first()
    if user is None: 
        return failure_response("user not found!")
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("list not found!")
    return success_response(event.serialize())

@app.route("/api/<int:id>/lists/<int:list_id>/events/<int:event_id>/", methods=["POST"])
def edit_event_by_id(id, list_id, event_id):
    user = User.query.filter_by(id=id).first()
    if user is None: 
        return failure_response("user not found!")
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("list not found!")
    body = json.loads(request.data.decode())
    event.company = body.get('company', event.company)
    event.position = body.get('position', event.position)
    event.reminder = body.get('reminder', event.reminder)
    db.session.commit()
    return success_response(event.serialize())

@app.route("/api/<int:id>/friends/add/", methods=['POST'])
def add_friend(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    body = json.loads(request.data.decode())
    search_id = body.get('id')
    if search_id is None:
        return failure_response("no id entered")
    if id == search_id:
        return failure_response("cannot send a request to yourself!")
    search_user = User.query.filter_by(id=search_id).first()
    if search_user is None:
        return failure_response("user not found!")
    already_friend = user.friends.filter_by(id=search_id).first()
    if already_friend is not None:
        return failure_response("you already added this user!")
    already_request = user.applying_friends.filter_by(id=search_id).first()
    if already_request is not None:
        return failure_response("you already have a pending response!")
    search_user.applying_friends.append(user)
    db.session.commit()
    return success_response(search_user.serialize())

@app.route("/api/<int:id>/friends/accept/<int:friend_id>/", methods=["POST"])
def accept_friend_request(id, friend_id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    friend = User.query.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("friend user not found!")
    friend = user.applying_friends.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("this user does not have a pending request!")
    user.friends.append(friend)
    user.applying_friends.remove(friend)
    db.session.commit()
    return success_response(friend.serialize())

@app.route("/api/<int:id>/friends/reject/<int:friend_id>/", methods=["POST"])
def reject_friend_request(id, friend_id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    friend = User.query.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("friend user not found!")
    friend = user.applying_friends.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("this user does not have a pending request!")
    user.applying_friends.remove(friend)
    db.session.commit()
    return success_response(friend.serialize())

@app.route("/api/<int:id>/friends/requests/")
def get_requests(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    return success_response({"requests": [f.serialize() for f in user.applying_friends]})

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port)
