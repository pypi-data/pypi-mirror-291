import os
from plyer import notification
from functools import wraps
from typing import Callable


def notify() -> Callable:
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        
        def wrapper(*args, **kwargs) -> None:
            """
            This wrapper notifies the user when
            the function has finished running.
            """
            
            func(*args, **kwargs)
            
            notification.notify(
                title='\U0001F40D',
                message=f'{func.__name__} finished',
                timeout=5  
            )
            
        return wrapper
    
    return decorator
