from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Database URL - use absolute path
db_path = os.path.join(BACKEND_DIR, "SKUMT_NGO.db")
DATABASE_URL = f"sqlite:///{db_path}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def migrate_db():
    """Add missing columns to existing SQLite tables without data loss."""
    from sqlalchemy import inspect
    inspector = inspect(engine)
    
    # Contacts: add phone if missing
    if inspector.has_table("contacts"):
        cols = [c['name'] for c in inspector.get_columns('contacts')]
        if 'phone' not in cols:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE contacts ADD COLUMN phone VARCHAR(20)"))
                conn.commit()
    
    # Volunteers: add new columns if missing
    if inspector.has_table("volunteers"):
        cols = [c['name'] for c in inspector.get_columns('volunteers')]
        new_cols = {
            'date_of_birth': 'VARCHAR',
            'address': 'TEXT',
            'education': 'VARCHAR',
            'preferred_area': 'VARCHAR',
            'motivation': 'TEXT',
        }
        for col_name, col_type in new_cols.items():
            if col_name not in cols:
                with engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE volunteers ADD COLUMN {col_name} {col_type}"))
                    conn.commit()

# Run migration on import
migrate_db()
