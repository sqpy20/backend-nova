from app import create_app, db
from app.model import User, Admin, Student_data

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created.")