from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class CreateCreditCardRequest(BaseModel):
    label: str
    card_no: str
    status: str = "ACTIVE"


class DeleteCreditCardRequest(BaseModel):
    card_no: str


class PatchCreditCardRequest(BaseModel):
    card_no: str
    label: str
    status: str
