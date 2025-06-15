from flask_sqlalchemy import SQLAlchemy

from .category import Category
from .question import Question


db = SQLAlchemy()

from app.models.response import *
from app.models.question import *