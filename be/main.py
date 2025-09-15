import os
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlmodel import select

from db import SessionDep, create_db_and_tables
from models import (
    Answer,
    AnswerCreate,
    AnswersResponse,
    EventCreate,
    Question,
    QuestionCreate,
    QuestionResponse,
    QuestionsResponse,
    StatsResponse,
)

app = FastAPI()

origins = os.getenv(
    "CORS_ORIGINS", "http://localhost,http://localhost:8080,http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/v1/questions")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> QuestionsResponse:
    count = session.exec(select(func.count()).select_from(Question)).one()
    questions = session.exec(select(Question).offset(offset).limit(limit)).all()
    return QuestionsResponse(count=count, results=list(questions))


@app.post("/v1/questions", status_code=201)
def create_question(question_data: QuestionCreate, session: SessionDep) -> Question:
    question = Question(text=question_data.text)
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@app.get("/v1/questions/{question_id}")
def read_question(question_id: int, session: SessionDep) -> QuestionResponse:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return QuestionResponse(
        id=question_id,
        text=question.text,
    )


@app.get("/v1/questions/{question_id}/answers")
def read_answers(
    question_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> AnswersResponse:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    count = session.exec(
        select(func.count())
        .select_from(Answer)
        .where(Answer.question_id == question_id)
    ).one()
    answers = session.exec(
        select(Answer)
        .where(Answer.question_id == question_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return AnswersResponse(count=count, results=list(answers))


@app.get("/v1/questions/{question_id}/stats")
def read_question_stats(question_id: int, session: SessionDep) -> StatsResponse:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return StatsResponse(visits=question.visits)


@app.post("/v1/questions/{question_id}/answers", status_code=201)
def create_answer(
    question_id: int, answer_data: AnswerCreate, session: SessionDep
) -> Answer:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    answer = Answer(question_id=question_id, text=answer_data.text)
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


@app.post("/v1/events", status_code=201)
def log_event(event_data: EventCreate, session: SessionDep) -> None:
    """Event logging should silently accept any valid data"""
    if event_data.object == "question":
        question = session.get(Question, event_data.id)
        if not question:
            return

        question.visits += 1

        session.add(question)
        session.commit()
