from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.response import Response
from app.schemas.common import MessageResponse
from app.schemas.responses import ResponseCreate, ResponseSchema, ResponseUpdate
from app.extensions import db
import logging


# creating a log file to control errors
logger = logging.getLogger(__name__)


responses_bp = Blueprint('responses', __name__, url_prefix='/responses')


# creating a function to get response with method "GET"
@responses_bp.route('/', methods=['GET'])
def get_responses():
    responses = Response.query.all()
    serialized = [ResponseSchema(question_text=r.question.text,
                                 is_agree=r.is_agree,
                                 question_id=r.question.id,
                                 id=r.id,
                                 text=r.text,
                                 user_id=r.user.id,
                                 user_nickname=r.user.nickname).model_dump() for r in responses]

    if responses:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No responses found").model_dump()), 404


# creating a function to create a response with method "POST"
@responses_bp.route('/', methods=['POST'])
def create_response():
    input_data = request.get_json()
    try:
        response_data = ResponseCreate(**input_data)
        response = Response(question_id=response_data.question_id,
                            is_agree=response_data.is_agree,
                            text=response_data.text,
                            user_id=response_data.user_id)
        db.session.add(response)
        db.session.commit()
        return jsonify(MessageResponse(message="Your response was created!").model_dump()), 200
    except ValidationError as e:
        return jsonify({'error': e.errors}), 400


# creating a function to get response by ID with method "GET"
@responses_bp.route('/<int:id>', methods=['GET'])
def get_response(id):
    response = Response.query.get(id)

    if response:
        return jsonify(MessageResponse(message=ResponseSchema(question_text=response.question.text,
                                                              is_agree=response.is_agree,
                                                              question_id=response.question.id,
                                                              id=response.id,
                                                              text=response.text,
                                                              user_id=response.user.id,
                                                              user_nickname=response.user.nickname).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump())


# creating a function to update a response by ID with method "PUT"
@responses_bp.route('/<int:id>', methods=['PUT'])
def update_response(id):
    response = Response.query.get(id)
    input_data = request.get_json()

    if response:
        try:
            updated_data = ResponseUpdate(**input_data)
            response.is_agree = updated_data.is_agree
            response.user_id = updated_data.user_id
            response.question_id = updated_data.question_id
            db.session.commit()
            return jsonify(MessageResponse(message=f"The response with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404


# creating a function to delete an answer to the question by ID with method "DELETE"
@responses_bp.route('/<int:id>', methods=['DELETE'])
def delete_response(id):
    response = Response.query.get(id)

    if response:
        db.session.delete(response)
        db.session.commit()
        return jsonify(MessageResponse(message=f"The response with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404