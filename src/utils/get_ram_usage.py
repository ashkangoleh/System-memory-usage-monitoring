'''
SystemUsage
'''
import threading
from typing import Any, Dict
import psutil
from sqlalchemy import insert
from src.db.database import get_db
from src.model import RamUsage
from .decorators import unit_convertor


class SystemUsage:
    """
    A class that provides information about the CPU and RAM usage of the system.

    Attributes:
    ----------
    cpu_percent : float
        The percentage of CPU usage of the system.
    ram_usage : dict
        A dictionary containing the RAM usage information of the system.

    Methods:
    -------
    __init__():
        Initializes the SystemUsage object and retrieves the initial values for cpu_percent and ram_usage.
    get_ram_usage(unit:str='gb') -> dict:
        Returns a dictionary containing the RAM usage information of the system in the specified unit.
    get_cpu_percent() -> float:
        Returns the percentage of CPU usage of the system.
    """

    def __init__(self, unit: str = 'gb') -> None:
        self.unit = unit

    def __enter__(self):
        '''
        Enter magic method for open Class as context manager to handling memory usage
        '''
        self.ram_usage = self.get_ram_usage()
        return self.ram_usage  # , self.cpu_percent

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_val, exc_tb, exc_type

    @unit_convertor(unit_name="GB", unit_calc=1024 * 1024 * 1024)
    @property
    def gb_convertor(self) -> Dict[str, Any]:
        '''
        Converting incoming values to GigaByte 
        Returns unit_name and unit_calc
        '''
        pass

    @unit_convertor(unit_name="MB", unit_calc=1024 * 1024)
    @property
    def mb_convertor(self) -> Dict[str, Any]:
        '''
        Converting incoming values to MegaByte 
        Returns unit_name and unit_calc
        '''
        pass

    def get_ram_usage(self):
        mem = psutil.virtual_memory()
        unit_name, unit_calc = None, None
        match self.unit.lower():
            case 'gb':
                unit_name, unit_calc = self.gb_convertor()
            case 'mb':
                unit_name, unit_calc = self.mb_convertor()
            case _:
                return {
                    "status": "failed",
                    "message": f"Current unit(\'{self.unit}\') does not exists!"
                    }

        total = mem.total / unit_calc
        free = mem.available / unit_calc
        used = mem.used / unit_calc
        return {
            'unit': unit_name,
            'total': round(total, 1),
            'free': round(free, 1),
            'used': round(used, 1)
            }


def system_usage_scheduler(stop: int = 1):
    """
    Local system usage scheduler 
    depends on built-in and not using any
    task manager or scheduler like celery
    """
    thread = threading.Timer(60.0, system_usage_scheduler)  # 60.0 seconds
    thread.start()
    if stop == 0:
        thread.cancel()
    with SystemUsage() as system_usage:
        for db in get_db():
            data = {
                "total": system_usage['total'],
                "free": system_usage['free'],
                "used": system_usage['used'],
                }
            query = insert(RamUsage)
            db.execute(query, data)
            db.commit()
