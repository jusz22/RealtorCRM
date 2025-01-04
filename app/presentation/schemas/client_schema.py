from pydantic import UUID4, BaseModel, EmailStr

class ClientIn(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr

class ClientDB(ClientIn):
    id: UUID4