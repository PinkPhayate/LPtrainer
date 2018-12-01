from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
# DB_PASSWORD = os.environ["DB_PASSWORD"]
db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/lptrainer"
# db_uri = "sqlite:///" + os.path.join(app.root_path, 'sqlite.db') # 追加
# db_uri = "postgres://localhost/lptrainer"
# db_uri = "postgres://kjmkebbsftguwy:{password}@ec2-54-227-240-7.compute-1.amazonaws.com:5432/df4ukoqg07j3ga"\
.format(password=DB_PASSWORD)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

from line_botr import lp_bot
from line_botr import repository
