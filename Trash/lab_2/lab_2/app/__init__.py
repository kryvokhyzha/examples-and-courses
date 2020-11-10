from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_compress import Compress

app = Flask(__name__)
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'application/json']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500

bootstrap = Bootstrap(app)
app.config.from_object(Config)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Compress(app)

from app import routes, errors
