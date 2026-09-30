from pydantic import BaseModel, Field

class paymentrequest(BaseModel):
    card_id : int
    amount : float = Field(gt=0)