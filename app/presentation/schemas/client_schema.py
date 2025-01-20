from pydantic import UUID4, BaseModel, ConfigDict, EmailStr

class ClientIn(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr

class ClientDB(ClientIn):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)