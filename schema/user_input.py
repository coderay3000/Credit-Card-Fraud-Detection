import math
from pydantic import BaseModel,Field,computed_field,model_validator
from typing import Literal,Annotated

# pydantic model
class UserInput(BaseModel):
     
    step: Annotated[int, Field(..., ge=1, le=743, description="Time step in hours")]
    type: Annotated[Literal["CASH_OUT", "TRANSFER", "PAYMENT", "CASH_IN", "DEBIT"], Field(..., description="Transaction type")]
    amount: Annotated[float, Field(..., ge=0.0, description="Transaction amount")]
    nameOrig: Annotated[str, Field(..., description="Origin account ID")]
    oldbalanceOrg: Annotated[float, Field(..., ge=0.0, description="Initial balance of sender")]
    newbalanceOrig: Annotated[float, Field(..., ge=0.0, description="New balance of sender")]
    nameDest: Annotated[str, Field(..., description="Destination account ID")]
    oldbalanceDest: Annotated[float, Field(..., ge=0.0, description="Initial balance of receiver")]
    newbalanceDest: Annotated[float, Field(..., ge=0.0, description="New balance of receiver")]

    @computed_field
    @property
    def dest_is_merchant(self) -> int:
        return 1 if self.nameDest.startswith("M") else 0
    
    @computed_field
    @property
    def errorBalanceOrig(self)->float:
        return self.newbalanceOrig + self.amount - self.oldbalanceOrg
    
    @computed_field
    @property
    def errorBalanceDest(self)->float:
        return self.oldbalanceDest + self.amount - self.newbalanceDest
    
    @computed_field
    @property
    def hour_of_day(self)->int:
        return self.step%24
    
    @computed_field
    @property
    def day_of_week(self)->int:
        return (self.step // 24)%7
    
    @computed_field
    @property
    def is_round_amount(self)->int:
        return 1 if (self.amount % 1000 == 0 and self.amount>0) else 0
    
    @computed_field
    @property
    def log_amount(self)->float:
        return math.log1p(self.amount)
        
     # for one hot encoded columns
    @computed_field
    @property
    def type_CASH_OUT(self) -> int:
        return 1 if self.type == "CASH_OUT" else 0

    @computed_field
    @property
    def type_DEBIT(self) -> int:
        return 1 if self.type == "DEBIT" else 0

    @computed_field
    @property
    def type_PAYMENT(self) -> int:
        return 1 if self.type == "PAYMENT" else 0

    @computed_field
    @property
    def type_TRANSFER(self) -> int:
        return 1 if self.type == "TRANSFER" else 0
     
    