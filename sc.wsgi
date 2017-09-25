import sys
import os
sys.path.insert(0, '/var/www/shared-clipboard/')
os.environ['SC_PATH'] = '/var/www/shared-clipboard/'
from sc.main import app as application
