from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username : str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)