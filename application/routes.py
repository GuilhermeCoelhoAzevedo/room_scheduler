from cgi import test
from crypt import methods
from email import message
from re import L
from app import app, db, mail
from flask import jsonify, request
from application.models import *
from flask_jwt_extended import jwt_required, create_access_token
from flask_mail import Message

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/rooms', methods = ['GET'])
def rooms():
    rooms_list = Room.query.all()
    result = rooms_schema.dump(rooms_list)
    return jsonify(result)

@app.route('/register', methods = ['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email = email).first()
    
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(email=email,first_name=first_name, last_name=last_name, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()

    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()

    if user:
        msg = Message("Your room_scheduler API password is: " + user.password,
            sender="admin@room-scheduler.com",
            recipients=[email])
        mail.send(msg)
        
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="Email doesn't exist in the system")

@app.route('/room_details/<int:room_id>', methods=['GET'])
def room_details(room_id: int):
    room = Room.query.filter_by(id=room_id).first()

    if room:
        result = room_schema.dump(room)
        return jsonify(result)
    else:
        return jsonify(message="Room doesn't exist"), 404

@app.route('/add_room', methods=['POST'])
@jwt_required()
def add_room():
    room_name = request.form['room_name']

    test = Room.query.filter_by(name=room_name).first()

    if test:
        return jsonify(message="There is already a room by that name"), 409
    else:
        name = request.form['room_name']
        new_room = Room(name=name)
        db.session.add(new_room)
        db.session.commit()
        
        return jsonify(message="Room added"), 201

@app.route('/update_room', methods=['PUT'])
@jwt_required()
def update_room():
    room_id = int(request.form['room_id'])
    room = Room.query.filter_by(id=room_id).first()

    if room:
        room.name = request.form['room_name']
        db.session.commit()
        return jsonify(message="Room updated!"), 202
    else:
        return jsonify(message="Room doesn't exist!"), 404

@app.route('/remove_room/<int:room_id>', methods=['DELETE'])
@jwt_required()
def remove_room(room_id: int):
    room = Room.query.filter_by(id=room_id).first()

    if room:
        db.session.delete(room)
        db.session.commit()
        return jsonify(message="Room removed!"), 202
    else:
        return jsonify(message="Room doesn't exist!"), 404

##################
#Database commands
##################
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

@app.cli.command('db_seed')
def db_seed():
    room1 = Room(name="Room Paris")
    room2 = Room(name="Room Rome")
    room3 = Room(name="Room Barcelona")

    db.session.add(room1)
    db.session.add(room2)
    db.session.add(room3)

    test_user = User(
                        first_name = "Guilherme",
                        last_name = "Azevedo",
                        email = "guilherme@gmail.com",
                        password = "gui123"
                    )

    db.session.add(test_user)
    db.session.commit()
    print("Database seeded!")