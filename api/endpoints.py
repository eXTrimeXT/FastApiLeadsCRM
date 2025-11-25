from fastapi import APIRouter, Depends, HTTPException
from app import dtos
from app.use_cases import LeadDistributionUseCase, OperatorManagementUseCase, SourceManagementUseCase
from core import entities
from api.dependencies import get_lead_distribution_use_case, get_operator_management_use_case, get_source_management_use_case

router = APIRouter()

@router.post("/contacts/", response_model=dtos.ContactResponse)
def create_contact(
    contact_data: dtos.ContactCreate,
    use_case: LeadDistributionUseCase = Depends(get_lead_distribution_use_case)
):
    try:
        contact = use_case.create_contact(
            lead_external_id=contact_data.lead_external_id,
            source_id=contact_data.source_id,
            message=contact_data.message
        )
        return dtos.ContactResponse(
            id=contact.id,
            lead_id=contact.lead_id,
            source_id=contact.source_id,
            operator_id=contact.operator_id,
            message=contact.message,
            status=contact.status.value,
            created_at=contact.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/operators/")
def create_operator(
    operator_data: dtos.OperatorCreate,
    use_case: OperatorManagementUseCase = Depends(get_operator_management_use_case)
):
    operator = use_case.create_operator(
        name=operator_data.name,
        max_active_leads=operator_data.max_active_leads
    )
    return {"id": operator.id, "name": operator.name}

@router.put("/operators/{operator_id}/status")
def update_operator_status(
    operator_id: int,
    status: str,
    use_case: OperatorManagementUseCase = Depends(get_operator_management_use_case)
):
    try:
        operator_status = entities.OperatorStatus(status)
        operator = use_case.update_operator_status(operator_id, operator_status)
        if operator:
            return {"status": "updated"}
        raise HTTPException(status_code=404, detail="Operator not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

@router.put("/sources/{source_id}/weights")
def update_source_weights(
    source_id: int,
    weights_data: dtos.SourceWeightsUpdate,
    use_case: SourceManagementUseCase = Depends(get_source_management_use_case)
):
    weights = [
        entities.OperatorSourceWeight(
            operator_id=weight.operator_id,
            source_id=source_id,
            weight=weight.weight
        ) for weight in weights_data.weights
    ]
    
    updated_weights = use_case.update_source_weights(source_id, weights)
    return {"updated_weights": len(updated_weights)}