from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, Session

engine = create_engine("sqlite:///test.db", echo=True)
print(engine.connect())

Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiment'

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(DateTime(),default=datetime.utcnow)
    type: Mapped[int] = mapped_column(String(30))
    finished: Mapped[Boolean] = mapped_column(Boolean, default=False)

class DataPoint(Base):

    __tablename__ = 'datapoint'

    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    real_value: Mapped[float] = mapped_column(Float(50))
    target_value: Mapped[float] = mapped_column(Float(50))

Base.metadata.create_all(engine)

with Session(engine) as session:
    expr = Experiment(id=1,title = "Wood", created_at = datetime(2022,11,11), type = 3, finished= False)
    session.add(expr)
    session.flush()
    print(expr.id)
    session.commit()