from app import db, ma
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'User'
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique = True)
    password = Column(String)

class Room(db.Model):
    __tablename__ = 'Room'
    id = Column(Integer, primary_key = True)
    name = Column(String)

class Booking(db.Model):
    __tablename__ = 'Booking'
    id = Column(Integer, primary_key = True)
    user = Column(Integer, ForeignKey('User.id'))
    Room = Column(Integer, ForeignKey('Room.id'))
    dt_start = Column(DateTime)
    dt_finish = Column(DateTime)
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class RoomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class BookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user', 'Room', 'dt_start', 'dt_finish')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)

booking_schema = BookingSchema()
booking_schema = BookingSchema(many=True)