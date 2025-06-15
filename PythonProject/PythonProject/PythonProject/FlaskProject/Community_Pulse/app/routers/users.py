from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.users import UserCreate, UserSchema, UserDelete, UserUpdate
from app.extensions import db
import logging


# creating a log file to control errors
logger = logging.getLogger(__name__)

# creating a blueprint for table "users"
users_bp = Blueprint('users', __name__, url_prefix='/users')


# getting all users
@users_bp.route('/', methods=['GET'])
def get_user():
    founded_users = User.query.all()

    if founded_users:
        serialized = [UserSchema(id=u.id, nickname=u.nickname).model_dump() for u in founded_users]
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message='No user was found.').model_dump()), 404


# creating a new user
@users_bp.route('/', methods=['POST'])
def create_user():
    input_data = request.get_json()

    try:
        userdata = UserCreate(**input_data)
        user = User(nickname=userdata.nickname, password=userdata.password)
        db.session.add(user)
        db.session.commit()
        logger.info(f'| new user {user.nickname} was created |')
        return jsonify(MessageResponse(message='User was created').model_dump()), 201
    except ValidationError as e:
        logger.error('| unknown error |')
        return jsonify(MessageResponse(message='Unknown error. Try again.').model_dump()), 400


# # getting one user by ID
# @users_bp.route('/<u>')


# # updating / changing an existed user
# @users_bp.route('')