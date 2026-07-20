from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.responses.api import SuccessResponse
from app.modules.loans.models import Loan
from app.modules.loans.schemas import LoanAmortizationItem, LoanCreate, LoanListResponse, LoanOut, LoanUpdate

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("/", response_model=SuccessResponse[LoanListResponse])
def list_loans(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    query = db.query(Loan)
    total = query.count()
    items = query.offset(offset).limit(page_size).all()
    
    result = []
    for item in items:
        # Calculate remaining installments
        remaining = 0
        if item.total_installments is not None and item.paid_installments is not None:
            remaining = max(0, item.total_installments - item.paid_installments)
        
        result.append({
            "id": item.id,
            "name": item.name,
            "loan_type": item.loan_type,
            "original_amount": float(item.original_amount),
            "current_balance": float(item.current_balance),
            "interest_rate": float(item.interest_rate) if item.interest_rate is not None else None,
            "total_installments": item.total_installments,
            "paid_installments": item.paid_installments,
            "remaining_installments": remaining
        })
        
    return {"success": True, "data": {"items": result, "page": page, "page_size": page_size, "total": total}}


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanCreate, db: Session = Depends(get_db)):
    loan = Loan(
        name=payload.name,
        loan_type=payload.loan_type,
        original_amount=payload.original_amount,
        current_balance=payload.current_balance,
        interest_rate=payload.interest_rate,
        total_installments=payload.total_installments,
        paid_installments=payload.paid_installments
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return {"success": True, "data": loan}


@router.get("/{loan_id}", response_model=SuccessResponse[LoanOut])
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    remaining = 0
    if loan.total_installments is not None and loan.paid_installments is not None:
        remaining = max(0, loan.total_installments - loan.paid_installments)
        
    return {
        "success": True,
        "data": {
            "id": loan.id,
            "name": loan.name,
            "loan_type": loan.loan_type,
            "original_amount": float(loan.original_amount),
            "current_balance": float(loan.current_balance),
            "interest_rate": float(loan.interest_rate) if loan.interest_rate is not None else None,
            "total_installments": loan.total_installments,
            "paid_installments": loan.paid_installments,
            "remaining_installments": remaining
        }
    }


@router.put("/{loan_id}", response_model=SuccessResponse)
def update_loan(loan_id: int, payload: LoanUpdate, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(loan, k, v)
        
    db.commit()
    db.refresh(loan)
    return {"success": True, "data": loan}


@router.delete("/{loan_id}", response_model=SuccessResponse)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    db.delete(loan)
    db.commit()
    return {"success": True, "data": {}}


@router.get("/{loan_id}/amortization", response_model=SuccessResponse[list[LoanAmortizationItem]])
def get_loan_amortization(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    total = loan.total_installments or 12
    paid = loan.paid_installments or 0
    remaining = max(0, total - paid)
    
    # Simple SAC calculator
    # monthly_rate = annual_rate / 12
    annual_rate = float(loan.interest_rate or Decimal("0.10"))
    monthly_rate = annual_rate / 12
    
    # SAC: Constant Amortization
    # principal = original_amount / total_installments
    original = float(loan.original_amount)
    principal = original / total
    
    current_balance = float(loan.current_balance)
    
    data = []
    # Cap at 24 entries to prevent rendering hundreds of rows in frontend
    entries = min(remaining, 24)
    for i in range(entries):
        month_idx = paid + i + 1
        # In SAC, balance decreases by 'principal' every month
        # For month M_i, the starting balance is current_balance - (i * principal)
        bal = current_balance - (i * principal)
        if bal < 0:
            bal = 0.0
            
        interest = bal * monthly_rate
        new_balance = bal - principal
        if new_balance < 0:
            new_balance = 0.0
            
        data.append({
            "month": f"M{month_idx}",
            "interest": round(interest, 2),
            "principal": round(principal, 2),
            "balance": round(new_balance, 2)
        })
        
    return {"success": True, "data": data}
