from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username : str

class UserCreate(UserBase):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)