from sqlmodel import Field, SQLModel


class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    visits: int = Field(default=0)


class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    text: str = Field(index=True)


class QuestionCreate(SQLModel, table=False):
    text: str = Field()


class AnswerCreate(SQLModel, table=False):
    text: str = Field(index=True)


class QuestionsResponse(SQLModel, table=False):
    count: int
    results: list["Question"]


class QuestionResponse(SQLModel, table=False):
    id: int
    text: str


class AnswerResponse(SQLModel, table=False):
    id: int
    text: str


class AnswersResponse(SQLModel, table=False):
    count: int
    results: list["Answer"]


class EventCreate(SQLModel, table=False):
    object: str
    id: int


class StatsResponse(SQLModel, table=False):
    visits: int
