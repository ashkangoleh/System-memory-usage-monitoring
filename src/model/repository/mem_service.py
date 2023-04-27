'''
Memory Service
'''
from typing import List, Dict
from src.model import RamUsage
from src.db import Session
from sqlalchemy import select


class RamUsageService:
    """Ram usage service
        cleaning queries with class
    Args:
        db_session: calling sessionmaker which generating by get_db
    
    Returns:
        rows: list of objects from query
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        
    #get all ram usage
    def get_all_ram_usage(self)->List[Dict]:
        '''
        get all ram usage
        '''
        query = select(RamUsage)
        result = self.db_session.execute(query)
        rows = result.scalars().all()
        return rows

    #get all ram usage descending with limitation
    def get_ram_usage_order_by_with_limit(self, limit: int)->List[Dict]:
        '''
        get ram usage with order_by and desc include limitation
        '''
        query = select(RamUsage).order_by(RamUsage.created_at.desc()).limit(limit)
        result = self.db_session.execute(query)
        rows = result.scalars().all()
        return rows
