import os
import sys
import time
# here import sqlalchemy to illustrate the issue
import sqlalchemy
from sqlalchemy.orm import mapped_column

def print_dummy():
    print("=========>>>>>>>>>> Sleep here in side handler")
    print(f"Python version: {sys.version}")
    print("sys.path:", sys.path)
    print("PYTHONPATH (from environment):", os.environ.get('PYTHONPATH'))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'current dir = {current_dir}')
    print(f'sqlalchemy version = {sqlalchemy.__version__}')
    time.sleep(10)
    print("Sleep here in side handler <<<<<<<<<<<<<<===========")
