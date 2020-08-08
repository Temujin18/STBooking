from stbooking import db, login_manager
from flask_login import UserMixin

## Room table in postgres has room_type enum with values single, double, triple, quad, queen, king
## Room table also has room_status enum with values booked, vacant, out order

# class RoomType(enum.Enum):
#     SINGLE = 'single'
#     DOUBLE = 'double'
#     TRIPLE = 'triple'
#     QUAD = 'quad'
#     QUEEN = 'queen'
#     KING = 'king'

# class RoomStatus(enum.Enum):
#     BOOKED = 'booked'
#     VACANT = 'vacant'
#     OUT_OF_ORDER = 'out of order'

@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    guest_booking = db.relationship('Booking', backref='guest', lazy=False)
    guest_info = db.relationship('UserAccount', backref='guest_info', lazy=False)

    def __repr__(self):
        return f"Guest({self.id}, {self.first_name}, {self.last_name})"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(20), nullable=False)
    room_status = db.Column(db.String(20), nullable=False)
    room_booking = db.relationship('Booking', backref='room', lazy=False)

    def __repr__(self):
        return f"Room({self.id}, {self.room_type}, {self.room_status})"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        return f"Booking({self.id}, {self.room}, {self.guest})"

class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.guest_id})"
