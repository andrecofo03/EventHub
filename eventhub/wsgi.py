import os
import sys
import shutil
from django.core.wsgi import get_wsgi_application

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

db_src = os.path.join(os.path.dirname(current_dir), 'db.sqlite3')
db_dest = '/tmp/db.sqlite3'
if os.path.exists(db_src) and not os.path.exists(db_dest):
    try:
        shutil.copy2(db_src, db_dest)
        print("Successfully copied db.sqlite3 to /tmp/db.sqlite3")
    except Exception as e:
        print("Failed to copy database:", e)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventhub.settings')

application = get_wsgi_application()
app = application

try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print("Error running migrations:", e)   