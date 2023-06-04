import os
import sys
import logging
from typing import Optional

class Logger:
    """Logs an info, warning and error message
    
       Arg:
         - name of the logger
    """
    if not os.path.exists("./logs/"):
        os.makedirs("./logs/")
    
    def __init__(self, name: Optional[str] = __name__) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        s_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(
            "./logs/milkroad_logs.log", mode="w"
        )

        s_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        fmt = logging.Formatter(
            "%(name)s:%(levelname)s - %(message)s"
        )

        s_handler.setFormatter(fmt)
        f_handler.setFormatter(fmt)

        self.logger.addHandler(s_handler)
        self.logger.addHandler(f_handler)

    def info(self, message: str) -> None:
        """Logs an info message showing progress of the script
        
           Arg:
             - message: the messaged to be logged
        """
        self.logger.info(message)
    
    def warn(self, message: str) -> None:
        """Logs a warning message for non-critical errors
        
           Arg:
             - message: the message to be logged
        """
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Logs a critical error that causes the script to crash
        
           Arg:
             - message: the error to be logged
        """
        self.logger.error(message, exc_info=True)
        sys.exit(1)