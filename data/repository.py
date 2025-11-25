from sqlalchemy.orm import Session
from core import entities, repositories
from . import models

class SQLLeadRepository(repositories.LeadRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_external_id(self, external_id: str) -> entities.Lead:
        db_lead = self.db.query(models.LeadModel).filter(
            models.LeadModel.external_id == external_id
        ).first()
        if db_lead:
            return entities.Lead(
                id=db_lead.id,
                external_id=db_lead.external_id,
                email=db_lead.email,
                phone=db_lead.phone,
                created_at=db_lead.created_at
            )
        return None
    
    def create(self, lead: entities.Lead) -> entities.Lead:
        db_lead = models.LeadModel(
            external_id=lead.external_id,
            email=lead.email,
            phone=lead.phone
        )
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        lead.id = db_lead.id
        lead.created_at = db_lead.created_at
        return lead

class SQLOperatorRepository(repositories.OperatorRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_active_operators(self) -> list[entities.Operator]:
        db_operators = self.db.query(models.OperatorModel).filter(
            models.OperatorModel.status == "active"
        ).all()
        return [
            entities.Operator(
                id=op.id,
                name=op.name,
                status=entities.OperatorStatus(op.status),
                max_active_leads=op.max_active_leads,
                created_at=op.created_at
            ) for op in db_operators
        ]
    
    def get_by_id(self, operator_id: int) -> entities.Operator:
        db_op = self.db.query(models.OperatorModel).filter(
            models.OperatorModel.id == operator_id
        ).first()
        if db_op:
            return entities.Operator(
                id=db_op.id,
                name=db_op.name,
                status=entities.OperatorStatus(db_op.status),
                max_active_leads=db_op.max_active_leads,
                created_at=db_op.created_at
            )
        return None
    
    def update(self, operator: entities.Operator) -> entities.Operator:
        db_op = self.db.query(models.OperatorModel).filter(
            models.OperatorModel.id == operator.id
        ).first()
        if db_op:
            db_op.name = operator.name
            db_op.status = operator.status.value
            db_op.max_active_leads = operator.max_active_leads
            self.db.commit()
            self.db.refresh(db_op)
        return operator

class SQLSourceRepository(repositories.SourceRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, source_id: int) -> entities.Source:
        db_source = self.db.query(models.SourceModel).filter(
            models.SourceModel.id == source_id
        ).first()
        if db_source:
            return entities.Source(
                id=db_source.id,
                name=db_source.name,
                description=db_source.description,
                created_at=db_source.created_at
            )
        return None
    
    def get_all(self) -> list[entities.Source]:
        db_sources = self.db.query(models.SourceModel).all()
        return [
            entities.Source(
                id=source.id,
                name=source.name,
                description=source.description,
                created_at=source.created_at
            ) for source in db_sources
        ]

class SQLOperatorSourceWeightRepository(repositories.OperatorSourceWeightRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_weights_for_source(self, source_id: int) -> list[entities.OperatorSourceWeight]:
        db_weights = self.db.query(models.OperatorSourceWeightModel).filter(
            models.OperatorSourceWeightModel.source_id == source_id
        ).all()
        return [
            entities.OperatorSourceWeight(
                id=weight.id,
                operator_id=weight.operator_id,
                source_id=weight.source_id,
                weight=weight.weight,
                created_at=weight.created_at
            ) for weight in db_weights
        ]
    
    def update_weights(self, source_id: int, weights: list[entities.OperatorSourceWeight]) -> list[entities.OperatorSourceWeight]:
        self.db.query(models.OperatorSourceWeightModel).filter(
            models.OperatorSourceWeightModel.source_id == source_id
        ).delete()
        
        for weight in weights:
            db_weight = models.OperatorSourceWeightModel(
                operator_id=weight.operator_id,
                source_id=source_id,
                weight=weight.weight
            )
            self.db.add(db_weight)
        
        self.db.commit()
        return weights

class SQLContactRepository(repositories.ContactRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, contact: entities.Contact) -> entities.Contact:
        db_contact = models.ContactModel(
            lead_id=contact.lead_id,
            source_id=contact.source_id,
            operator_id=contact.operator_id,
            message=contact.message,
            status=contact.status.value
        )
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        contact.id = db_contact.id
        contact.created_at = db_contact.created_at
        return contact
    
    def get_operator_active_contacts_count(self, operator_id: int) -> int:
        return self.db.query(models.ContactModel).filter(
            models.ContactModel.operator_id == operator_id,
            models.ContactModel.status.in_(["new", "in_progress"])
        ).count()
    
    def get_contacts_by_lead(self, lead_id: int) -> list[entities.Contact]:
        db_contacts = self.db.query(models.ContactModel).filter(
            models.ContactModel.lead_id == lead_id
        ).all()
        return [
            entities.Contact(
                id=contact.id,
                lead_id=contact.lead_id,
                source_id=contact.source_id,
                operator_id=contact.operator_id,
                message=contact.message,
                status=entities.ContactStatus(contact.status),
                created_at=contact.created_at
            ) for contact in db_contacts
        ]