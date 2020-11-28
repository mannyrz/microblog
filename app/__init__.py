from flask import Flask, render_template, Response, request 
from flask_caching import Cache
from flask_session.__init__ import Session

from config import Config

app = Flask(__name__)
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#SESSION_TYPE = 'redis'

app.config.from_object(Config)

#cache = Cache(app, config={'CACHE_TYPE': 'simple'})
#Session(app)

from app import routes
