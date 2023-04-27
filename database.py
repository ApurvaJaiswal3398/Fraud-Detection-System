from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer    
from sqlalchemy import create_engine

Base=declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    id=Column(Integer, primary_key=True)
    type=Column(String(10),nullable=True)
    amount=Column(Float,nullable=True)
    nameOrig=Column(String(15),nullable=True)
    oldbalanceOrig=Column(Float,nullable=True)
    newbalanceOrig=Column(Float,nullable=True)
    nameDest=Column(String(15),nullable=True)
    oldbalanceDest=Column(Float,nullable=True)
    newbalanceDest=Column(Float,nullable=True)  

    def __str__(self):
        return self.type

engine=create_engine('sqlite:///project.sqlite')
Base.metadata.create_all(engine)

