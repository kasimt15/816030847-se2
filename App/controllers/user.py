from sqlalchemy.exc import IntegrityError
from App.models import User
from App.database import db

def create_user(name, address):
    try:
        newuser = User(name=name, address=address)
        db.session.add(newuser)
        db.session.commit()
        return newuser
    
    except IntegrityError as e:
        db.session.rollback()

        if "UNIQUE constraint failed" in str(e):
            return f"A user with the name '{name}' already exists."
        else:
            return f"An error occurred while creating the user: {str(e)}"
    
    except Exception as e:
        db.session.rollback()
        return f"An unexpected error occurred: {str(e)}"

def get_user_by_name(name):
    return User.query.filter_by(name=name).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, name):
    user = get_user(id)
    if user:
        user.name = name
        db.session.add(user)
        return db.session.commit()
    return None
    