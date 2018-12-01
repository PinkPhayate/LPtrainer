from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
db_uri = "sqlite:///" + os.path.join(app.root_path, 'sqlite.db') # 追加
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

from line_botr import lp_bot
from line_botr import repository
