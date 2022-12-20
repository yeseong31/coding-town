from app import db


# ManyToMany: 사용자 - room
room_user = db.Table(
    'room_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'), primary_key=True)
)

# ManyToMany: 태그 - room
room_tag = db.Table(
    'room_tag',
    db.Column('room_id', db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
)


class User(db.Model):
    """사용자"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), unique=True, nullable=False)


class Room(db.Model):
    """방 정보"""
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), nullable=False)
    room_code = db.Column(db.String(6), nullable=False, unique=True)
    is_private = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(50), nullable=True)
    total_user = db.Column(db.Integer, nullable=True)
    # tag_id = db.relationship('Tag', backref=db.backref('tag_set', cascade='all, delete-orphan'))
    room_owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    room_participant = db.relationship('User', secondary=room_user, backref=db.backref('user_set'))
    created_at = db.Column(db.DateTime(), nullable=False)
    modified_at = db.Column(db.DateTime(), nullable=True)
    
    
class Tag(db.Model):
    """태그"""
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True, nullable=False)
    