from stbooking import db, login_manager, admin
from flask_user import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255))
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
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return f"User({self.id}, {self.email}, {self.roles})"

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name  = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user_account.id', ondelete='CASCADE'))    
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))    


class AdminAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin({self.id}, {self.username})"

class MyModelView(ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_roles('admin')
        )

class RoomModelView(ModelView):

    column_list = ['id', 'room_type', 'room_status']

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_roles('admin')
        )


admin.add_view(MyModelView(Guest, db.session))
admin.add_view(RoomModelView(Room, db.session))
admin.add_view(MyModelView(Booking, db.session))
admin.add_view(MyModelView(UserAccount, db.session))