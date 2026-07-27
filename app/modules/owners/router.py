from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.owners import schemas, service
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/owners", tags=["owners"])


@router.post(
    "/",
    response_model=SuccessResponse[schemas.OwnerOut],
    status_code=status.HTTP_201_CREATED,
)
def create_owner(
    payload: schemas.OwnerCreate, db: Session = Depends(get_db)
) -> dict[str, object]:
    owner = service.OwnerService(db).get_or_create(payload.phone)
    return {"success": True, "data": owner}


@router.get("/{phone}", response_model=SuccessResponse[schemas.OwnerOut])
def get_owner(phone: str, db: Session = Depends(get_db)) -> dict[str, object]:
    owner = service.OwnerService(db).get(phone)
    return {"success": True, "data": owner}


@router.get(
    "/{phone}/defaults",
    response_model=SuccessResponse[schemas.OwnerDefaultsOut],
)
def get_owner_defaults(
    phone: str, db: Session = Depends(get_db)
) -> dict[str, object]:
    owner, account, credit_card = service.OwnerService(db).get_defaults(phone)
    return {
        "success": True,
        "data": {
            "phone": owner.phone,
            "account": account,
            "credit_card": credit_card,
        },
    }


@router.put(
    "/{phone}/accounts/{account_id}",
    response_model=SuccessResponse[schemas.OwnerOut],
)
def associate_account(
    phone: str,
    account_id: int,
    payload: schemas.AssociationUpdate,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    owner = service.OwnerService(db).associate_account(
        phone, account_id, payload.is_default
    )
    return {"success": True, "data": owner}


@router.delete(
    "/{phone}/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_account(
    phone: str, account_id: int, db: Session = Depends(get_db)
) -> Response:
    service.OwnerService(db).remove_account(phone, account_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{phone}/credit-cards/{credit_card_id}",
    response_model=SuccessResponse[schemas.OwnerOut],
)
def associate_credit_card(
    phone: str,
    credit_card_id: int,
    payload: schemas.AssociationUpdate,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    owner = service.OwnerService(db).associate_credit_card(
        phone, credit_card_id, payload.is_default
    )
    return {"success": True, "data": owner}


@router.delete(
    "/{phone}/credit-cards/{credit_card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_credit_card(
    phone: str, credit_card_id: int, db: Session = Depends(get_db)
) -> Response:
    service.OwnerService(db).remove_credit_card(phone, credit_card_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
