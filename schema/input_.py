from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserInputRegister(BaseModel):
    username: Optional[str]=None
    email: Optional[str]=None
    passwd: Optional[str]=None
    token: Optional[str]=None
    expire_in: Optional[datetime] = Field(None, description="Expiration datetime in format 'YYYY-MM-DD HH:MM:SS'")
    transfer_enable: Optional[int]=None

class UserUpdate(BaseModel):
    expire_in: Optional[datetime] = Field(None, description="Expiration datetime in format 'YYYY-MM-DD HH:MM:SS'")
    transfer_enable: Optional[int]=None
