from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username : str

class UserIn(UserBase):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class UserDB(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)