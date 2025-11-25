from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import *

class LeadRepository(ABC):
    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Optional[Lead]:
        pass
    
    @abstractmethod
    def create(self, lead: Lead) -> Lead:
        pass

class OperatorRepository(ABC):
    @abstractmethod
    def get_active_operators(self) -> List[Operator]:
        pass
    
    @abstractmethod
    def get_by_id(self, operator_id: int) -> Optional[Operator]:
        pass
    
    @abstractmethod
    def update(self, operator: Operator) -> Operator:
        pass

class SourceRepository(ABC):
    @abstractmethod
    def get_by_id(self, source_id: int) -> Optional[Source]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Source]:
        pass

class OperatorSourceWeightRepository(ABC):
    @abstractmethod
    def get_weights_for_source(self, source_id: int) -> List[OperatorSourceWeight]:
        pass
    
    @abstractmethod
    def update_weights(self, source_id: int, weights: List[OperatorSourceWeight]) -> List[OperatorSourceWeight]:
        pass

class ContactRepository(ABC):
    @abstractmethod
    def create(self, contact: Contact) -> Contact:
        pass
    
    @abstractmethod
    def get_operator_active_contacts_count(self, operator_id: int) -> int:
        pass
    
    @abstractmethod
    def get_contacts_by_lead(self, lead_id: int) -> List[Contact]:
        pass