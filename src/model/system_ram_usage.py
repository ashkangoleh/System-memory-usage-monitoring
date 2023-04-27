'''
Memory usage Model
'''
import sqlalchemy as sa
from src.db.database import Base


class RamUsage(Base):
    """
    A SQLAlchemy declarative model representing RAM usage information.

    Attributes:
        id (int): The unique ID of the RAM usage record.
        total (float): The total amount of RAM available.
        free (float): The amount of RAM currently free.
        used (float): The amount of RAM currently in use.
        created (datetime): The datetime when the RAM usage record was created.
    """
    __tablename__ = "ram_usage"
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    total = sa.Column(sa.FLOAT, nullable=False)
    free = sa.Column(sa.FLOAT, nullable=False)
    used = sa.Column(sa.FLOAT, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    
    
    def __str__(self):
        return {
            "total":self.total,
            "free":self.free,
            "used":self.used,
            "created_at":self.created_at,
        }