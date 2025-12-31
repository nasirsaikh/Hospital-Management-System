import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_migrate import Migrate

db = SQLAlchemy()
engine = None
Session = None
migrate = None

def init_db(app):
    global engine, Session, migrate
    
    db.init_app(app)

    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    engine = create_engine(db_uri, future=True)

    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), 'migrations'))

    with app.app_context():
        db.create_all()
        from models import User, UserRole
        from werkzeug.security import generate_password_hash

        session = Session()

        default_admin_email = "admin@hospital.com"

        existing_admin = session.query(User).filter_by(email=default_admin_email).first()

        if not existing_admin:
            admin = User(
                name="Super Admin",
                email=default_admin_email,
                password=generate_password_hash("admin123"),
                role=UserRole.ADMIN
            )
            session.add(admin)
            session.commit()
            print("✨ Default Admin Created → admin@hospital.com / admin123")
        else:
            print("✔ Default admin already exists")
    print(f"Database initialized and alembic migrations environment ready at {migrate.directory}")

def get_db_session():
    global Session
    
    if not Session:
        raise Exception("Database session is not initialized. Call init_db(app) first.")
    return Session()

def close_db_session(session):
    try:
        session.close()
    except Exception:
        pass
