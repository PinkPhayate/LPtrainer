from flask import Flask
app = Flask(__name__)

from line_botr import lp_bot
from line_botr import repository
repository.create_table()
