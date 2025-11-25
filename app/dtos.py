from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LeadCreate(BaseModel):
    external_id: str
    email: Optional[str] = None
    phone: Optional[str] = None

class OperatorCreate(BaseModel):
    name: str
    max_active_leads: int = 10

class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    max_active_leads: Optional[int] = None

class SourceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ContactCreate(BaseModel):
    lead_external_id: str
    source_id: int
    message: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: Optional[int]
    message: Optional[str]
    status: str
    created_at: datetime

class LeadResponse(BaseModel):
    id: int
    external_id: str
    email: Optional[str]
    phone: Optional[str]
    created_at: datetime
    contacts: List[ContactResponse] = []

class OperatorWeightUpdate(BaseModel):
    operator_id: int
    weight: int

class SourceWeightsUpdate(BaseModel):
    weights: List[OperatorWeightUpdate]