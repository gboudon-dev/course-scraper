import os
from database.db_manager import DbManager
from tasks.tasks import TASKS

db_manager = DbManager()

task = os.getenv("TASK")

if task in TASKS:
    TASKS[task](db_manager)
else:
    print(f"Invalid TASK value: {task}")

db_manager.close()
        
    
      

