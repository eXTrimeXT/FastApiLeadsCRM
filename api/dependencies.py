from data.database import get_db
from data.repository import *
from app.use_cases import LeadDistributionUseCase, OperatorManagementUseCase, SourceManagementUseCase

def get_lead_distribution_use_case():
    db = next(get_db())
    return LeadDistributionUseCase(
        lead_repo=SQLLeadRepository(db),
        operator_repo=SQLOperatorRepository(db),
        source_repo=SQLSourceRepository(db),
        weight_repo=SQLOperatorSourceWeightRepository(db),
        contact_repo=SQLContactRepository(db)
    )

def get_operator_management_use_case():
    db = next(get_db())
    return OperatorManagementUseCase(
        operator_repo=SQLOperatorRepository(db)
    )

def get_source_management_use_case():
    db = next(get_db())
    return SourceManagementUseCase(
        source_repo=SQLSourceRepository(db),
        weight_repo=SQLOperatorSourceWeightRepository(db)
    )