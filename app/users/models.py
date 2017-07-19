from app import db 
from sqlalchemy import DDL, event
from flask_login import UserMixin


# SQLAlchemy classes that reference to tables
# user_pofile, status, async_operation
class UserProfile(UserMixin, db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)


class AsyncOperationStatus(db.Model):
    __tablename__ = 'async_operation_status'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column('code', db.String(20), nullable=True)


class AsyncOperation(db.Model):
    __tablename__ = 'async_operation'
    id = db.Column(db.Integer, primary_key=True)
    async_operation_status_id = db.Column(db.Integer, db.ForeignKey(AsyncOperationStatus.id))
    status = db.relationship('AsyncOperationStatus', foreign_keys=async_operation_status_id)
    
    user_profile_id = db.Column(db.Integer, db.ForeignKey(UserProfile.id))
    user_profile = db.relationship('UserProfile', foreign_keys=user_profile_id)


event.listen(
        AsyncOperationStatus.__table__, 'after_create',
        DDL(
                """ INSERT INTO async_operation_status (id,code) VALUES(1,'pending'),(2, 'ok'),(3, 'error'); """)
)
