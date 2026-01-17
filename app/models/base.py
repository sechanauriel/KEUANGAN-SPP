# app/models/base.py
from flask_sqlalchemy import SQLAlchemy

# Single instance untuk semua models
db = SQLAlchemy()
