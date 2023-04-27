
from pydantic import BaseModel


class RamUsageBaseSchema(BaseModel):
    '''
    RAM usage Base model
    '''
    total: float
    free: float
    used: float
    created_at: str


class GetRamUsage(RamUsageBaseSchema):
    class Config:
        orm_mode = True
        
