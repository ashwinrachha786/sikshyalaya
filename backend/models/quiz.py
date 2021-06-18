from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Date,
    Time,
    Boolean,
    ARRAY,
)
import enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import JSON
from .association_tables import (
    group_quiz_association_table,
    instructor_quiz_association_table,
)

from core.db import Base


class Quiz(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    end_time = Column(Time)
    start_time = Column(Time)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_randomized = Column(Boolean, default=False)
    display_individual = Column(Boolean, default=False)
    group = relationship(
        "Group", secondary=group_quiz_association_table, backref="quiz"
    )
    instructor = relationship(
        "User", secondary=instructor_quiz_association_table, backref="quiz"
    )
    total_marks = Column(Integer, default=0)
    course_id = Column(Integer, ForeignKey("course.id", ondelete="cascade"))
    course = relationship("Course", backref="quiz")
    __tablename__ = "quiz"  # noqa


class AnswerType(enum.Enum):
    TEXT_OPTIONS: int = 1
    IMAGE_OPTIONS: int = 2
    FILE_UPLOAD: int = 3
    TEXT_TYPING: int = 4


class QuestionType(enum.Enum):
    TEXT: int = 1
    IMAGE: int = 2


class QuizQuestion(Base):
    id = Column(Integer, primary_key=True)

    question_text = Column(String, nullable=True)
    question_image = Column(ARRAY(String), nullable=True)

    # if IMAGE_OPTIONS in combination with option_image is present then, we show all the image in option_image, and then show all the options present in options
    options = Column(JSON, nullable=False)
    marks = Column(Integer, default=0)
    # if IMAGE_Options present and answer == 0, then check answer_image
    answer = Column(ARRAY(Integer), nullable=True)

    quiz_id = Column(Integer, ForeignKey("quiz.id", ondelete="cascade"))
    quiz = relationship("Quiz", backref="question")

    __tablename__ = "quiz_question"  # noqa

    @hybrid_property
    def multiple(self):
        if len(self.answer) > 1:
            return True
        else:
            return False


# for storing user answers
class QuizAnswer(Base):
    id = Column(Integer, primary_key=True)
    # user_id
    # question_id
    __tablename__ = "quiz_answer"  # noqa
