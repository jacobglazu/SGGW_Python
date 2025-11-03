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
    #expr = Experiment(id=1,title = "Wood", created_at = datetime(2022,11,11), type = 3, finished= False)
    session.add_all([
                Experiment(title = "Wood", created_at = datetime(2022,11,11), type = 3, finished= False,),
                Experiment(title = "Fire", created_at = datetime(2025,8,11), type = 4, finished= False,),
                DataPoint(real_value = 55, target_value = 60,),
                DataPoint(real_value = 58, target_value = 60,),
                DataPoint(real_value = 92, target_value = 90,),
                DataPoint(real_value = 54, target_value = 50,),
                DataPoint(real_value = 45, target_value = 50,),
                DataPoint(real_value = 75, target_value = 80,),
                DataPoint(real_value = 82, target_value = 80,),
                DataPoint(real_value = 93, target_value = 100,),
                DataPoint(real_value = 13, target_value = 15,),
                DataPoint(real_value = 15, target_value = 20,),
                ])
                
            
    #session.flush()
    session.commit()
    session.close()