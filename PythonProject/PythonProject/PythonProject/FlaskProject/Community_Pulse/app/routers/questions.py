from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from pydantic import ValidationError
from app.models.question import Question
from app.schemas.common import MessageResponse
from app.schemas.questions import QuestionCreate, QuestionSchema, QuestionUpdate
from app.extensions import db
import logging

# creating a log file to control errors
logger = logging.getLogger(__name__)

# creating a blueprint for questions table
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/create', methods=['GET'])
def create_question_form():
    """A form to create a new question"""
    return render_template('questions/create.html')


@questions_bp.route('/<int:id>/edit', methods=['GET'])
def update_question_form(id):
    """A form to edit a question"""
    question = Question.query.get(id)
    if not question:
        return render_template('error.html', message=f'Question {id} not found'), 404

    question_data = QuestionSchema(
        id=question.id,
        text=question.text,
        user_id=question.user.id,
        user_nickname=question.user.nickname
    ).model_dump()

    return render_template('questions/edit.html', question=question_data)


# getting all questions
@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()

    # creating a dictionary of all gotten questions like [{1: 'text', 2: 'text'}]
    serialized = [QuestionSchema(
        id=q.id,
        text=q.text,
        user_id=q.user.id,
        user_nickname=q.user.nickname
    ).model_dump() for q in questions]

    # HTML rendering for 'text/html' requests
    if 'text/html' in request.accept_mimetypes:
        return render_template(
            'questions/list.html',
            questions=serialized,
            message=request.args.get('message')
        )

    # JSON response for 'application/json' requests
    # checking if any questions were found
    if questions:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message='No questions found').model_dump()), 404


# creating
@questions_bp.route('/', methods=['POST'])
def create_question():
    logger.info('creating a question...')

    # HTML
    if 'application/x-www-form-urlencoded' in request.content_type:
        input_data = {
            'text': request.form.get('text', ''),
            'user_id': request.form.get('user_id', '')
        }
    # JSON
    else:
        input_data = request.get_json()

    try:
        question_data = QuestionCreate(**input_data)
        question = Question(text=question_data.text, user_id=question_data.user_id)
        db.session.add(question)
        db.session.commit()

        # redirect for HTML
        if 'application/x-www-form-urlencoded' in request.content_type:
            return redirect(url_for('questions.get_questions', message='Your question was created!'))
        # JSON response
        else:
            return jsonify(MessageResponse(message='Your question was created!').model_dump()), 201

    except ValidationError as e:
        errors = e.errors()
        if 'application/x-www-form-urlencoded' in request.content_type:
            return render_template('questions/create.html', error=errors)
        else:
            return jsonify({'error': errors}), 400


# creating a function to get question by ID with method "GET"
@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    logger.info(f'getting question with {id}')
    question = Question.query.get(id)

    if not question:
        # HTML
        if 'text/html' in request.accept_mimetypes:
            return render_template('error.html', message=f'No question with id {id} was found.'), 404
        # JSON
        return jsonify(MessageResponse(message=f'No question with id {id} was found.').model_dump())

    question_data = QuestionSchema(
        id=question.id,
        text=question.text,
        user_id=question.user.id,
        user_nickname=question.user.nickname
    ).model_dump()

    # HTML
    if 'text/html' in request.accept_mimetypes:
        return render_template('questions/detail.html', question=question_data)

    # JSON
    return jsonify(MessageResponse(message=question_data).model_dump())


# creating a function to update a question by ID with method "PUT"
@questions_bp.route('/<int:id>', methods=['PUT', 'POST'])
def update_question(id):
    question = Question.query.get(id)
    if not question:
        if 'text/html' in request.accept_mimetypes:
            return render_template('error.html', message=f'No question with id {id} was found.'), 404
        return jsonify(MessageResponse(message=f'No question with id {id} was found.').model_dump()), 404

    # HTML
    if request.method == 'POST':
        input_data = {
            'text': request.form.get('text', ''),
            'user_id': request.form.get('user_id', '')
        }
    # JSON
    else:
        input_data = request.get_json()

    try:
        updated_data = QuestionUpdate(**input_data)
        question.text = updated_data.text
        question.user_id = updated_data.user_id
        db.session.commit()

        # HTML
        if request.method == 'POST':
            return redirect(url_for('questions.get_question', id=id))

        # JSON
        return jsonify(MessageResponse(message=f'The question with id {id} was updated.').model_dump()), 200

    except ValidationError as e:
        errors = e.errors()
        if request.method == 'POST':
            question_data = QuestionSchema(
                id=question.id,
                text=question.text,
                user_id=question.user.id,
                user_nickname=question.user.nickname
            ).model_dump()
            return render_template('questions/edit.html', question=question_data, error=errors)
        return jsonify({'error': errors}), 400


# delete via form
@questions_bp.route('/<int:id>/delete', methods=['POST'])
def delete_question_form(id):
    return delete_question(id)


#
# creating a function to delete a question
@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    if not question:
        if 'text/html' in request.accept_mimetypes:
            return render_template('error.html', message=f'No question with id {id} was found.'), 404
        return jsonify(MessageResponse(message=f'No question with id {id} was found.').model_dump()), 404

    db.session.delete(question)
    db.session.commit()

    # HTML
    if request.method == 'POST':
        return redirect(url_for('questions.get_questions', message=f'The question with id {id} was deleted.'))
    # JSON
    else:
        return jsonify(MessageResponse(message=f'The question with id {id} was deleted.').model_dump()), 200
