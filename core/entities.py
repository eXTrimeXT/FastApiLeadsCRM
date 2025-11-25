from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class OperatorStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class ContactStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

@dataclass
class Lead:
    id: Optional[int] = None
    external_id: str = None
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Operator:
    id: Optional[int] = None
    name: str = None
    status: OperatorStatus = OperatorStatus.ACTIVE
    max_active_leads: int = 10
    created_at: Optional[datetime] = None

@dataclass
class Source:
    id: Optional[int] = None
    name: str = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class OperatorSourceWeight:
    id: Optional[int] = None
    operator_id: int = None
    source_id: int = None
    weight: int = 1
    created_at: Optional[datetime] = None

@dataclass
class Contact:
    id: Optional[int] = None
    lead_id: int = None
    source_id: int = None
    operator_id: Optional[int] = None
    message: Optional[str] = None
    status: ContactStatus = ContactStatus.NEW
    created_at: Optional[datetime] = None