import random
from typing import List, Optional
from core import entities, repositories

class LeadDistributionUseCase:
    def __init__(
        self,
        lead_repo: repositories.LeadRepository,
        operator_repo: repositories.OperatorRepository,
        source_repo: repositories.SourceRepository,
        weight_repo: repositories.OperatorSourceWeightRepository,
        contact_repo: repositories.ContactRepository
    ):
        self.lead_repo = lead_repo
        self.operator_repo = operator_repo
        self.source_repo = source_repo
        self.weight_repo = weight_repo
        self.contact_repo = contact_repo
    
    def create_contact(self, lead_external_id: str, source_id: int, message: str = None) -> entities.Contact:
        lead = self.lead_repo.get_by_external_id(lead_external_id)
        if not lead:
            lead = entities.Lead(external_id=lead_external_id)
            lead = self.lead_repo.create(lead)
        
        available_operators = self._get_available_operators(source_id)
        operator_id = self._select_operator(available_operators, source_id)
        
        contact = entities.Contact(
            lead_id=lead.id,
            source_id=source_id,
            operator_id=operator_id,
            message=message
        )
        return self.contact_repo.create(contact)
    
    def _get_available_operators(self, source_id: int) -> List[entities.Operator]:
        weights = self.weight_repo.get_weights_for_source(source_id)
        operator_ids_with_weights = {w.operator_id for w in weights}
        
        active_operators = self.operator_repo.get_active_operators()
        
        available_operators = []
        for operator in active_operators:
            if operator.id in operator_ids_with_weights:
                active_contacts = self.contact_repo.get_operator_active_contacts_count(operator.id)
                if active_contacts < operator.max_active_leads:
                    available_operators.append(operator)
        
        return available_operators
    
    def _select_operator(self, available_operators: List[entities.Operator], source_id: int) -> Optional[int]:
        if not available_operators:
            return None
        
        all_weights = self.weight_repo.get_weights_for_source(source_id)
        available_operator_ids = {op.id for op in available_operators}
        available_weights = [w for w in all_weights if w.operator_id in available_operator_ids]
        
        if not available_weights:
            return None
        
        weighted_operators = []
        for weight in available_weights:
            weighted_operators.extend([weight.operator_id] * weight.weight)
        
        return random.choice(weighted_operators)

class OperatorManagementUseCase:
    def __init__(self, operator_repo: repositories.OperatorRepository):
        self.operator_repo = operator_repo
    
    def create_operator(self, name: str, max_active_leads: int = 10) -> entities.Operator:
        operator = entities.Operator(
            name=name,
            max_active_leads=max_active_leads
        )
        return operator
    
    def update_operator_status(self, operator_id: int, status: entities.OperatorStatus) -> entities.Operator:
        operator = self.operator_repo.get_by_id(operator_id)
        if operator:
            operator.status = status
            return self.operator_repo.update(operator)
        return None

class SourceManagementUseCase:
    def __init__(
        self,
        source_repo: repositories.SourceRepository,
        weight_repo: repositories.OperatorSourceWeightRepository
    ):
        self.source_repo = source_repo
        self.weight_repo = weight_repo
    
    def update_source_weights(self, source_id: int, weights: List[entities.OperatorSourceWeight]) -> List[entities.OperatorSourceWeight]:
        return self.weight_repo.update_weights(source_id, weights)