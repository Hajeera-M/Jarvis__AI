import os, sys
os.environ["DATABASE_URL"] = "sqlite:///jarvis_memory.db"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from jarvis.memory.postgres_db import init_db
from jarvis.agents.controller import MasterController

init_db()
output, context = MasterController.handle_user_input('Who is your owner?', {}, 'test')
print(output)

