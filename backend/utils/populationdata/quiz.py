from typing import List
from pydantic import Json

from datetime import datetime

quizzes: List[Json] = [
    {
        "end_time": datetime(2021, 6, 13, 13, 00, 00),
        "start_time": datetime(2021, 6, 13, 11, 00, 00),
        "title": "Fundamentals of Computer First Quiz",
        "description": "Quiz for Course COMP101, which is to test the understanding of students on the basic fundamentals of Computer Programming.",
        "is_randomized": True,
        "display_individual": False,
        "group": [1, 3, 5, 6],
        "instructor": [9],
        "course_id": 1,
    },
    {
        "end_time": datetime(2021, 4, 12, 10, 00, 00),
        "start_time": datetime(2021, 4, 12, 9, 00, 00),
        "title": "Introduction to Environemental Engineering quiz",
        "description": "Quiz for Course ENVE101, which is to test the understanding of students on the fundamentals of Environmental Enginnering.",
        "is_randomized": False,
        "display_individual": True,
        "group": [1, 3, 5, 6, 17],
        "instructor": [10],
        "course_id": 3,
    },
    {
        "end_time": datetime(2021, 12, 12, 12, 00, 00),
        "start_time": datetime(2021, 12, 12, 10, 00, 00),
        "title": "Elements of Engineering First Quiz",
        "description": "Quiz for Course ENGG101, which is to test the understanding of students on the elementaries of engineering.",
        "is_randomized": False,
        "display_individual": False,
        "group": [4],
        "instructor": [10],
        "course_id": 5,
    },
    {
        "end_time": datetime(2021, 9, 14, 14, 00, 00),
        "start_time": datetime(2021, 9, 14, 12, 00, 00),
        "title": "Fundamentals of Computer First Quiz",
        "description": "Quiz for Course COMP101, which is to test the understanding of students on the basic fundamentals of Computer Programming.",
        "is_randomized": True,
        "display_individual": False,
        "group": [1, 3, 5, 6],
        "instructor": [8],
        "course_id": 2,
    },
    {
        "end_time": datetime(2021, 2, 2, 5, 00, 00),
        "start_time": datetime(2021, 2, 1, 17, 00, 00),
        "title": "Advanced Environmental Engineering Third Quiz",
        "description": "Quiz for Course ENVE201, which is to test the understanding of students on the advanced knowledge of environmental engineering.",
        "is_randomized": True,
        "display_individual": False,
        "group": [2, 6, 18],
        "instructor": [8],
        "course_id": 4,
    },
    {
        "end_time": datetime(2021, 3, 8, 17, 00, 00),
        "start_time": datetime(2021, 3, 8, 15, 00, 00),
        "title": "Advanced Engineering Third Quiz",
        "description": "Quiz for Course ENGG211, which is to test the understanding of students on the advanced knowledge of engineering.",
        "is_randomized": True,
        "display_individual": False,
        "group": [4, 20],
        "instructor": [10],
        "course_id": 6,
    },
    {
        "end_time": datetime(2021, 4, 10, 10, 00, 00),
        "start_time": datetime(2021, 4, 10, 8, 00, 00),
        "title": "Basics of Law First Quiz",
        "description": "Quiz for Course LLB101, which is to test the understanding of students on the basic human rights.",
        "is_randomized": True,
        "display_individual": True,
        "group": [9, 25],
        "instructor": [8, 9],
        "course_id": 7,
    },
    {
        "end_time": datetime(2021, 11, 11, 14, 00, 00),
        "start_time": datetime(2021, 11, 11, 13, 00, 00),
        "title": "Criminal Law Second Quiz",
        "description": "Quiz for Course LLB202, which is to test the understanding of students on criminal laws and rights surrounding them.",
        "is_randomized": False,
        "display_individual": False,
        "group": [25],
        "instructor": [9, 10],
        "course_id": 8,
    },
    {
        "end_time": datetime(2021, 6, 13, 13, 00, 00),
        "start_time": datetime(2021, 6, 13, 11, 00, 00),
        "title": "Information Systems Basics Quiz",
        "description": "Quiz for Course IST101, which is to test the understanding of students on the basic fundamentals of Computer Information Systems.",
        "is_randomized": True,
        "display_individual": False,
        "group": [7, 8, 24],
        "instructor": [10, 8],
        "course_id": 9,
    },
    {
        "end_time": datetime(2021, 10, 12, 12, 00, 00),
        "start_time": datetime(2021, 10, 9, 12, 00, 00),
        "title": "Business and Management Studies First Quiz",
        "description": "Quiz for Course BMS222, which is to test the understanding of students on topics within the depths of Business and Management Studies",
        "is_randomized": False,
        "display_individual": True,
        "group": [7, 24],
        "instructor": [9, 10, 8],
        "course_id": 10,
    },
]


quizQuestions: List[Json] = [
    {
        "question_type": 1,
        "question_text": "Question with only text?",
        "question_image": None,
        "answer_type": 1,
        "option_image": None,
        "option": """ { "1" : "Yupp" , "2" : "Nope"} """,
        "answer_image": None,
        "answer": 1,
        "quiz_id": 1,
    },
    {
        "question_type": 2,
        "question_text": "Question with only text?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 1,
        "option_image": None,
        "option": """ { "1" : "Yupp" , "2" : "Nope"} """,
        "answer_image": None,
        "answer": 2,
        "quiz_id": 1,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 2,
        "option_image": ["option1Img.jpg", "option2Img.jpg"],
        "option": """{ "1" : "This", "2" : "Or, This" }""",
        "answer": None,
        "answer_image": "option1Img.jpg",
        "quiz_id": 1,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 3,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 1,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 4,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 1,
    },
    {
        "question_type": 1,
        "question_text": "Question with only text?",
        "question_image": None,
        "answer_type": 1,
        "option_image": None,
        "option": """{ "1" : "Yupp" , "2" : "Nope"}""",
        "answer_image": None,
        "answer": 1,
        "quiz_id": 2,
    },
    {
        "question_type": 2,
        "question_text": "Question with only text?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 1,
        "option_image": None,
        "option": """{ "1" : "Yupp" , "2" : "Nope"}""",
        "answer_image": None,
        "answer": 2,
        "quiz_id": 2,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 2,
        "option_image": ["option1Img.jpg", "option2Img.jpg"],
        "option": """{ "1" : "This", "2" : "Or, This" }""",
        "answer": None,
        "answer_image": "option1Img.jpg",
        "quiz_id": 2,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 3,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 2,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 4,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 2,
    },
    {
        "question_type": 1,
        "question_text": "Question with only text?",
        "question_image": None,
        "answer_type": 1,
        "option_image": None,
        "option": """{ "1" : "Yupp" , "2" : "Nope"}""",
        "answer_image": None,
        "answer": 1,
        "quiz_id": 3,
    },
    {
        "question_type": 2,
        "question_text": "Question with only text?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 1,
        "option_image": None,
        "option": """{ "1" : "Yupp" , "2" : "Nope"}""",
        "answer_image": None,
        "answer": 2,
        "quiz_id": 3,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 2,
        "option_image": ["option1Img.jpg", "option2Img.jpg"],
        "option": """{ "1" : "This", "2" : "Or, This" }""",
        "answer": None,
        "answer_image": "option1Img.jpg",
        "quiz_id": 3,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 3,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 3,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 4,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 3,
    },
    {
        "question_type": 1,
        "question_text": "Question with only text?",
        "question_image": None,
        "answer_type": 1,
        "option_image": None,
        "option": """{ "1" : "Yupp" , "2" : "Nope"}""",
        "answer_image": None,
        "answer": 1,
        "quiz_id": 4,
    },
    {
        "question_type": 2,
        "question_text": "Question with only text?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 1,
        "option_image": None,
        "option": """ { "1" : "Yupp" , "2" : "Nope"} """,
        "answer_image": None,
        "answer": 2,
        "quiz_id": 4,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 2,
        "option_image": ["option1Img.jpg", "option2Img.jpg"],
        "option": """ { "1" : "Yupp" , "2" : "Nope"} """,
        "answer": None,
        "answer_image": "option1Img.jpg",
        "quiz_id": 4,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 3,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 4,
    },
    {
        "question_type": 2,
        "question_text": "Find Answer with right Image?",
        "question_image": ["question1Img.jpg", "question2Img.jpg"],
        "answer_type": 4,
        "option_image": None,
        "option": None,
        "answer": None,
        "answer_image": None,
        "quiz_id": 4,
    },
]