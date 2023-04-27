'''
Unit Convertor Decorator usable for convert into MB or GB
'''
from typing import Tuple, Any, Callable

def unit_convertor(unit_name: str, unit_calc: int) -> Callable[[Any], Tuple[str, Any]]:
    """
    A decorator that takes a unit name and unit conversion factor as arguments and returns a decorator function.

    Parameters:
    ----------
    unit_name : str
        The name of the unit to which the value will be converted.
    unit_calc : int
        The conversion factor to convert the value to the desired unit.

    Returns:
    -------
    Callable[[Any], Tuple[str, Any]]
        A decorator function that takes a function as argument and returns a tuple containing the unit name and unit calc.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Tuple[str, Any]]:
        def wrapper(*args, **kwargs) -> Tuple[str, Any]:
            return  unit_name, unit_calc
        return wrapper
    return decorator


