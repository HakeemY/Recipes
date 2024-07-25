# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "franktaylor"

#replace the name once a proper database is created
DB = "recipe_share"