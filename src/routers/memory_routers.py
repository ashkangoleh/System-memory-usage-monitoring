'''
Memory Usage main route
'''
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from src.model import RamUsageService
from src.db import get_db, Session



mem = APIRouter(
    prefix='/mem'
)




@mem.get('/ram_usage/')
async def get_last_ram_usage_info(n:int, db:Session = Depends(get_db)) -> None:
    """
    Retrieves the RAM usage history from the database

    Args:
        n (int): The maximum number of entries to retrieve (must be greater than 0).
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).

    Returns:
        A list of RAM usage entries,\
            sorted in descending order by timestamp and limited to the specified number

    Raises:
        HTTPException: If the specified limit is less than or equal to 0, or if an error occurs while retrieving the
        RAM usage history.
    """
    try:
        if n <= 0:
                raise HTTPException(
                status_code=400,
                detail={
                    "status": "failed",
                    "message": "require parameter must be greater equal 0"
                }
                )
        result = RamUsageService(db_session=db)
        return result.get_ram_usage_order_by_with_limit(limit=n)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "failed",
                "message": f"{e}"
            }
        )