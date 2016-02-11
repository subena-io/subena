# -*- coding: utf-8-sig -*-
from eve_sqlalchemy.decorators import registerSchema
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String, Float

from base import Base

class Setting(Base):
        __tablename__ = 'setting'
        
        id = Column('id',Integer,primary_key=True)
        numberOfLastMeasures = Column('numberOfLastMeasures',Integer, nullable=False)
   
@registerSchema('stats')     
class Stats(Base):
    __tablename__ = 'stats'
    
    id = Column('id',Integer,primary_key=True,autoincrement=True)
    association = Column('association',String(255),nullable=False)
    parent = Column('parent',String(255),nullable=True)
    children = Column('children',String(255),nullable=True)
    value = Column('value',String(255),nullable=False)
    proba = Column('proba',Float,nullable=True)
    
@registerSchema('alerts')     
class Alerts(Base):
    __tablename__ = 'alerts'
    
    id = Column('id',Integer,primary_key=True,autoincrement=True)
    timestamp = Column('t',Integer,nullable=False)
    source = Column('source',String(255),nullable=False)
    action = Column('action',String(255),nullable=True)
    risk = Column('riskValue',Float,nullable=True)

@registerSchema('family')
class Family(Base):
    __tablename__ = 'family'
    
    id = Column('id',Integer,primary_key=True)
    parent_id = Column('idParent',Integer, ForeignKey('family.id'),nullable=False)
    label = Column('label',String(255), nullable=False)
    parent = relationship("Family")
            
    def __repr__(self):
        return "Family id({}) label({}) parent({})".format(self.id,self.label,self.parent)

criterion_dependencies = Table("dependency", Base.metadata,
    Column("idParent", Integer, ForeignKey("criterion.id"), primary_key=True),
    Column("idChild", Integer, ForeignKey("criterion.id"), primary_key=True)
)

@registerSchema('criterion')
class Criterion(Base):
    __tablename__ = 'criterion'
    
    id = Column('id',Integer,primary_key=True)
    family_id = Column('idFamily',Integer, ForeignKey("family.id"), nullable=False)
    label = Column('label',String(255), nullable=False)
    shortLabel = Column('shortLabel',String(50), nullable=True)
    description = Column('description',String(255), nullable=True)

    children = relationship("Criterion",
                        secondary=criterion_dependencies,
                        primaryjoin=id==criterion_dependencies.c.idParent,
                        secondaryjoin=id==criterion_dependencies.c.idChild,
                        backref="parents"
    )
    family = relationship(Family)
        
    def __repr__(self):
        return "Criterion id({}) label({}) values({})".format(self.id,self.label,self.values)

@registerSchema('value')
class Value(Base):
    __tablename__ = 'value'
    
    id = Column('id',Integer, primary_key=True)
    criterion_id = Column('idCriterion',Integer,ForeignKey("criterion.id"), nullable=False)
    category = Column('category',String(255), nullable=False)
    value = Column('value',String(255), nullable=False)
    timestamp = Column('t',Integer, nullable=False)
    
    criterion = relationship("Criterion",backref="values")
    
    def __repr__(self):
        return "Value id({}) category({}) value({})".format(self.id,self.category,self.value)