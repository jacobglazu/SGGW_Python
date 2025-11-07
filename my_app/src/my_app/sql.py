from typing import Optional, List
import os
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, Float, select, delete, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, Session, relationship

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

with Session(engine) as session:
    
    stmt = select('*').select_from(Experiment)
    result = session.execute(stmt).fetchall()
    print(result)

    stmt_2 = select('*').select_from(DataPoint)
    res = session.execute(stmt_2).fetchall()
    print(res)

    exp = session.get(Experiment, 1)
    
    if exp is not None:
        exp.finished = True
    else:
        print(f"Nie można znaleźć eksperymetnu on id = 1")
    exp = session.get(Experiment, 2)
    exp.finished = True
    session.commit()
    session.close()

with Session(engine) as session:
    session.execute(delete(Experiment))
    session.commit()
    session.close()
with Session(engine) as session:
    session.execute(delete(DataPoint))
    session.commit()
    session.close()

    # Usunięcie pliku bazy
    engine.dispose()
    if os.path.isfile('test.db'):
        os.remove('test.db')
        print(f"Plik test.db został usunięty")
    else:
        print(f"Nie znaleziono pliku")

    # relacje 1 do wielu
engine = create_engine("sqlite:///test.db", echo=True)
print(engine.connect())

class Experiment2(Base):
    __tablename__ = 'experiment2'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(DateTime(),default=datetime.utcnow)
    type: Mapped[int] = mapped_column(String(30))
    finished: Mapped[Boolean] = mapped_column(Boolean, default=False)

  
    datapoints: Mapped[List["DataPoints"]] = relationship(back_populates="experiment2", cascade= "all, delete-orphan",)
class DataPoints(Base):
    __tablename__ = 'datapoints'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    experiment_id: Mapped[int] = mapped_column(Integer, ForeignKey(Experiment2.id), nullable= False)
    real_value: Mapped[float] = mapped_column(Float(50))
    target_value: Mapped[float] = mapped_column(Float(50))  

    experiment2 : Mapped[Experiment2] = relationship(back_populates="datapoints")

    def __repr__(self) -> str:
        return(
            f"<Data(id={self.id})," f"experimetn_id= {self.experiment_id}, "
            f"real_value= {self.real_value}," f"target_value= {self.target_value},")


Base.metadata.create_all(engine)

with Session(engine) as session:
    exp = Experiment2(title="Wood", type=3, finished=False)
    dp1 = DataPoints(real_value=1.23, target_value=2.34, experiment2= exp)
    dp2 = DataPoints(real_value= 2.1, target_value= 3.3, experiment2 = exp)
    dp3 = DataPoints(real_value= 2.2, target_value= 3.5, experiment2 = exp)
    dp4 = DataPoints(real_value= 2.5, target_value= 3.6, experiment2 = exp)
    dp5 = DataPoints(real_value= 2.4, target_value= 3.7, experiment2 = exp)
    dp6 = DataPoints(real_value= 2.6, target_value= 3.8, experiment2 = exp)
    dp7 = DataPoints(real_value= 2.3, target_value= 3.23, experiment2 = exp)
    dp8 = DataPoints(real_value= 2.8, target_value= 3.44, experiment2 = exp)
    dp9 = DataPoints(real_value= 2.33, target_value= 3.55, experiment2 = exp)
    dp10 = DataPoints(real_value= 2.44, target_value= 3.15, experiment2 = exp)


    session.add(exp)   # dp1 zostanie dodany automatycznie dzięki cascade
    session.commit()
    session.close()

with Session(engine) as session:   
    exp2 = Experiment2(title="Fire", type=2, finished=False)
    dp1 = DataPoints(real_value=1.23, target_value=2.34, experiment2= exp2)
    dp2 = DataPoints(real_value= 2.1, target_value= 3.3, experiment2 = exp2)
    dp3 = DataPoints(real_value= 2.2, target_value= 3.5, experiment2 = exp2)
    dp4 = DataPoints(real_value= 2.5, target_value= 3.6, experiment2 = exp2)
    dp5 = DataPoints(real_value= 2.4, target_value= 3.7, experiment2 = exp2)
    dp6 = DataPoints(real_value= 2.6, target_value= 3.8, experiment2 = exp2)
    dp7 = DataPoints(real_value= 2.3, target_value= 3.23, experiment2 = exp2)
    dp8 = DataPoints(real_value= 2.8, target_value= 3.44, experiment2 = exp2)
    dp9 = DataPoints(real_value= 2.33, target_value= 3.55, experiment2 = exp2)
    dp10 = DataPoints(real_value= 2.44, target_value= 3.15, experiment2 = exp2) 

    session.add(exp2)
    session.commit()
    session.close()

class Association(Base):
    __tablename__ = "association_table"

    subject_id: Mapped[int] = mapped_column(Integer,ForeignKey("subject.id"), primary_key=True)
    experiment_id: Mapped[int] = mapped_column(Integer,
        ForeignKey("experiment3.id"), primary_key=True
    )
    extra_data: Mapped[Optional[str]] = mapped_column(String(100), nullable= False)
# association between Assocation -> Child
    exp: Mapped["Experiment3"] = relationship(back_populates="parent_associations")

    # association between Assocation -> Parent
    sub: Mapped["Subject"] = relationship(back_populates="child_associations")

    def __repr__(self) -> str:
        return (
            f"<Association subject_id={self.subject_id!r} "
            f"experiment_id={self.experiment_id!r} extra_data={self.extra_data!r}>"
        )


# child
class Experiment3(Base):
    __tablename__ = "experiment3"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(DateTime(),default=datetime.utcnow)
    type: Mapped[int] = mapped_column(String(30))
    finished: Mapped[Boolean] = mapped_column(Boolean, default=False)
    
    # association between Child -> Association -> Parent
    parent_associations: Mapped[List["Association"]] = relationship(
        back_populates="exp"
    )
    subjects : Mapped[List["Subject"]] = relationship("Subject",secondary="association_table",viewonly=True, back_populates="experiments",)

    def __repr__(self) -> str:
        return f"<Experiment3 id={self.id!r} title={self.title!r}>"

# Parent
class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int]= mapped_column(Integer, primary_key= True)
    gdpr_advanced: Mapped[Boolean]= mapped_column(Boolean, default= False)
    

    # association between Parent -> Association -> Child
    child_associations: Mapped[List["Association"]] = relationship(
        back_populates="sub"
    )
    experiments : Mapped[List["Experiment3"]] = relationship("Experiment3",secondary="association_table",viewonly= True, back_populates="subjects",)

    def __repr__(self) -> str:
        return (
            f"<Subject id={self.id!r} gdpr_advanced={self.gdpr_advanced!r}>"
        )


engine = create_engine("sqlite:///test.db", echo=True)
print(engine.connect())

Base.metadata.create_all(engine)
with Session(engine) as session:
    s1 = Subject(gdpr_advanced = True)
    e1 = Experiment3(title = "Buy", created_at =datetime(2022,11,11), type =5)
    assoc = Association(extra_data= "first link")
    assoc.sub = s1
    assoc.exp = e1
    
    session.add_all([s1, e1, assoc])
    session.commit()
    session.close()
