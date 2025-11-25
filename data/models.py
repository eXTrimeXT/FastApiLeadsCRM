from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class LeadModel(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    contacts = relationship("ContactModel", back_populates="lead")

class OperatorModel(Base):
    __tablename__ = "operators"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    max_active_leads = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    contacts = relationship("ContactModel", back_populates="operator")
    source_weights = relationship("OperatorSourceWeightModel", back_populates="operator")

class SourceModel(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    contacts = relationship("ContactModel", back_populates="source")
    operator_weights = relationship("OperatorSourceWeightModel", back_populates="source")

class OperatorSourceWeightModel(Base):
    __tablename__ = "operator_source_weights"
    
    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    weight = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    operator = relationship("OperatorModel", back_populates="source_weights")
    source = relationship("SourceModel", back_populates="operator_weights")

class ContactModel(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    lead = relationship("LeadModel", back_populates="contacts")
    source = relationship("SourceModel", back_populates="contacts")
    operator = relationship("OperatorModel", back_populates="contacts")